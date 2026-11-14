#!/usr/bin/env python3
"""Image à la une iptvsmartrespro.fr — modèle validé le 2026-11-10.

Usage :
    python3 make_featured.py "TITRE EXACT DE L'ARTICLE" "CATEGORIE" sortie.webp

Seuls le titre et la catégorie changent. Le fond (background.png : TV, PC,
smartphone, pied de page iptvsmartrespro.fr) et la police sont fixes.
Sortie : WebP 1200x675.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "background.png")
BOLD = os.path.join(HERE, "fonts", "Poppins-ExtraBold.ttf")
GRAD = [(24, 199, 245), (45, 107, 255), (110, 63, 245)]  # cyan -> bleu -> violet

X, MAXW = 85, 600          # zone de texte à gauche (coordonnées du fond 1671x941)
BADGE_Y, BADGE_H = 135, 78
TITLE_BOTTOM = 640


def grad(t):
    a, b, u = (GRAD[0], GRAD[1], t * 2) if t < .5 else (GRAD[1], GRAD[2], (t - .5) * 2)
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))


def words_of(text):
    # espace insécable devant : ? ! ; pour ne jamais isoler la ponctuation en début de ligne
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

    # badge catégorie (dégradé)
    fb = ImageFont.truetype(BOLD, 46)
    cat = category.upper()
    bw = int(d.textlength(cat, font=fb) + 92)
    pill = Image.new("RGB", (bw, BADGE_H))
    pd = ImageDraw.Draw(pill)
    for i in range(bw):
        pd.line((i, 0, i, BADGE_H), fill=grad(i / bw))
    mask = Image.new("L", (bw, BADGE_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, BADGE_H - 1), radius=BADGE_H // 2, fill=255)
    img.paste(pill, (X, BADGE_Y), mask)
    d.text((X + 46, BADGE_Y + BADGE_H // 2 + 2), cat, font=fb, fill="white", anchor="lm")

    # titre : la taille s'adapte à la longueur (5 lignes max)
    top = BADGE_Y + BADGE_H + 45
    words = words_of(title)
    for size in range(92, 40, -2):
        f = ImageFont.truetype(BOLD, size)
        lines = wrap(d, words, f, MAXW)
        lh = int(size * 1.13)
        if len(lines) <= 5 and lh * len(lines) <= TITLE_BOTTOM - top and all(d.textlength(l, font=f) <= MAXW for l in lines):
            break
    y = top
    for line in lines:
        d.text((X, y), line, font=f, fill="white")
        y += lh

    img.resize((1200, 675), Image.LANCZOS).save(out, "WEBP", quality=82, method=6)
    print(f"{out} ({os.path.getsize(out)} octets, police {size}px, {len(lines)} lignes)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit('usage: make_featured.py "TITRE" "CATEGORIE" sortie.webp')
    main(*sys.argv[1:])
