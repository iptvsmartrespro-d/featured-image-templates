# featured-image-templates

Modèles d'images à la une utilisés par les tâches automatiques de rédaction d'articles.

## iptvsmartrespro.fr

Modèle validé le 2026-11-10 : fond bleu nuit, TV + PC + smartphone à droite, badge de catégorie et titre de l'article à gauche, pied de page « iptvsmartrespro.fr · Guide IPTV Smarters Pro · 2026 ».

```bash
pip install pillow --break-system-packages   # si Pillow manque
python3 iptvsmartrespro/make_featured.py "Titre exact de l'article" "Dépannage" /tmp/featured.webp
```

- Seuls le **titre** et la **catégorie** changent ; le fond (`background.png`) et la police sont fixes.
- Sortie : WebP 1200×675. La taille du titre s'adapte à sa longueur (5 lignes max).
- Police : Poppins ExtraBold (SIL Open Font License, voir `fonts/OFL.txt`).

Ne pas modifier `background.png` sans valider le nouveau rendu avec le propriétaire du site.

## francepremiumtv.fr

Modèle validé le 2026-11-14 : salon clair, TV + box + smartphone à droite, ruban bleu-blanc-rouge, badge de catégorie rouge et titre bleu nuit à gauche, pied de page « francepremiumtv.fr · Guide IPTV France · 2026 ».

```bash
python3 francepremiumtv/make_featured.py "Titre exact de l'article" "Usages" /tmp/featured.webp
```
