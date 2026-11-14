#!/usr/bin/env python3
"""Image à la une francepremiumtv.fr — identité visuelle du site (blanc, bleu nuit, rouge, bleu).

Usage :
    python3 make_featured.py "TITRE EXACT DE L'ARTICLE" "CATEGORIE" sortie.webp

Seuls le titre et la catégorie changent. Le fond (background.png : salon, TV,
box, smartphone, ruban bleu-blanc-rouge) et les polices sont fixes.
Sortie : WebP 1200x675.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "background.png")          # 1672x941
BOLD = os.path.join(HERE, "fonts", "Poppins-ExtraBold.ttf")
SEMI = os.path.join(HERE, "fonts", "Poppins-SemiBold.ttf")

NAVY = (11, 18, 32)       # #0B1220
RED = (229, 9, 20)        # #E50914
BLUE = (29, 78, 216)      # #1D4ED8
MUTED = (107, 118, 148)   # #6b7694

X, MAXW = 90, 610         # zone de texte à gauche
BADGE_Y, BADGE_H = 120, 64
TITLE_BOTTOM = 650
FOOT_Y = 893              # centre vertical de la bande blanche du bas


def words_of(text):
    for p in (" :", " ?", " !", " ;"):
        text = text.replace(p, " " + p[1:])
    return [w for w in text.split(" ") if w]


def wrap(draw, words, font, maxw):
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main(title, category, out):
    img = Image.open(BG).convert("RGB")
    d = ImageDraw.Draw(img)

    # badge catégorie rouge
    fb = ImageFont.truetype(SEMI, 30)
    cat = category.upper()
    bw = int(d.textlength(cat, font=fb) + 64)
    d.rounded_rectangle((X, BADGE_Y, X + bw, BADGE_Y + BADGE_H), radius=BADGE_H // 2, fill=RED)
    d.text((X + 32, BADGE_Y + BADGE_H // 2 + 1), cat, font=fb, fill="white", anchor="lm")

    # titre bleu nuit, taille adaptée (5 lignes max)
    top = BADGE_Y + BADGE_H + 40
    words = words_of(title)
    for size in range(88, 40, -2):
        f = ImageFont.truetype(BOLD, size)
        lines = wrap(d, words, f, MAXW)
        lh = int(size * 1.14)
        if len(lines) <= 5 and lh * len(lines) <= TITLE_BOTTOM - top and all(d.textlength(l, font=f) <= MAXW for l in lines):
            break
    y = top
    for line in lines:
        d.text((X, y), line, font=f, fill=NAVY)
        y += lh
    # petit soulignement rouge sous le titre
    d.rounded_rectangle((X, y + 30, X + 90, y + 38), radius=4, fill=RED)

    # pied de page
    ff = ImageFont.truetype(BOLD, 40)
    d.ellipse((X, FOOT_Y - 9, X + 18, FOOT_Y + 9), fill=RED)
    d.text((X + 34, FOOT_Y + 2), "francepremiumtv.fr", font=ff, fill=NAVY, anchor="lm")
    fr = ImageFont.truetype(SEMI, 30)
    d.text((1672 - X, FOOT_Y + 2), "Guide IPTV France · 2026", font=fr, fill=MUTED, anchor="rm")

    img.resize((1200, 675), Image.LANCZOS).save(out, "WEBP", quality=82, method=6)
    print(f"{out} ({os.path.getsize(out)} octets, police {size}px, {len(lines)} lignes)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('usage: make_featured.py "TITRE" "CATEGORIE" sortie.webp')
    main(*sys.argv[1:])
