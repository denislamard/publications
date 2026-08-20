# Publications — mode d'emploi du dépôt

Ce dépôt contient les guides PDF et la page qui les présente,
[denislamard.github.io/publications](https://denislamard.github.io/publications/).

Ce fichier décrit une seule chose : **la procédure complète pour ajouter un
document.** Elle prend une vingtaine de minutes, dont quinze de rédaction.

---

## Sommaire

1. [L'installation, une seule fois](#1-linstallation-une-seule-fois)
2. [Les conventions du dépôt](#2-les-conventions-du-dépôt)
3. [La procédure, étape par étape](#3-la-procédure-étape-par-étape)
4. [Le bloc de cahier à copier](#4-le-bloc-de-cahier-à-copier)
5. [Écrire les cinq textes](#5-écrire-les-cinq-textes)
6. [Retirer ou renommer un document](#6-retirer-ou-renommer-un-document)
7. [Dépannage](#7-dépannage)

---

## 1. L'installation, une seule fois

Le rendu des vignettes passe par poppler, un binaire système :

```sh
sudo apt install poppler-utils
```

`outils/vignettes.py` porte un en-tête PEP 723, donc `uv` construit son
environnement au premier appel et le met en cache ensuite. Rien à installer côté
Python, rien à activer.

Vérification :

```sh
pdftoppm -v && uv run outils/vignettes.py --help | head -3
```

---

## 2. Les conventions du dépôt

```
guide-agent-ia.pdf              le PDF, à la racine
index.html                      la page, un <article class="cahier"> par document
assets/css/style.css            feuille unique
assets/fonts/                   6 woff2, Source Serif 4 et IBM Plex
assets/img/hero-document-agent.svg   le visuel de tête
assets/img/og-image.png         l'image de partage
assets/img/01/                  les visuels du cahier 01
assets/img/02/                  les visuels du cahier 02
outils/vignettes.py             génère couverture et aperçus
```

| Élément | Règle | Exemple |
|---|---|---|
| Nom du PDF | stable pour un guide versionné, daté pour un article | `guide-agent-ia.pdf`, `2026-09-relance.pdf` |
| Numéro de cahier | deux chiffres, ordre de parution, jamais réattribué | `03` |
| Dossier d'images | `assets/img/<numéro>/` | `assets/img/03/` |
| Nom des visuels | `cover-<nom du PDF>.webp`, `apercu-<nom du PDF>-1..3.webp` | `cover-guide-agent-ia.webp` |
| Ancre HTML | `id="c<numéro>"`, identique au numéro affiché | `id="c03"` |

Le numéro apparaît à quatre endroits pour un même document : le dossier
d'images, l'ancre `id`, le `<span class="numero">` et la ligne de la table
« La collection ». Ils doivent porter la même valeur.

---

## 3. La procédure, étape par étape

### Étape 1 — Déposer le PDF

À la racine du dépôt, sous son nom définitif. Le renommer ensuite casse les
liens déjà partagés.

```sh
cp ~/documents/mon-guide.pdf guide-supervision.pdf
```

### Étape 2 — Choisir les trois pages d'aperçu

Ouvrez le PDF et repérez **trois pages qui montrent de la matière** : un
tableau, un schéma, une grille. Une page de texte courant ne donne rien à voir
en vignette.

Attention au décalage : les numéros à passer au script sont ceux du **fichier**,
pas ceux imprimés en pied de page. Sur un guide dont la couverture n'est pas
numérotée, la page imprimée 7 est la page 8 du fichier. Le script rappelle la
correspondance à la fin de son exécution.

### Étape 3 — Générer les visuels

Une commande, qui crée le dossier au passage :

```sh
uv run outils/vignettes.py guide-supervision.pdf --pages 8 11 13 --dossier 03
```

Elle écrit quatre fichiers dans `assets/img/03/` et affiche ce qu'il faut
recopier à l'étape suivante :

```
guide-supervision.pdf — 21 pages dans le fichier, 480 Ko

Couverture
  assets/img/03/cover-guide-supervision.webp  500×707  11 Ko
Aperçus
  assets/img/03/apercu-guide-supervision-1.webp  340×481  12 Ko
  ...

À recopier dans index.html
  poids du fichier   : 480 Ko
  pages imprimées    : 20 (si la couverture n'est pas numérotée)
  aperçu 1           : ...  (page 8 du fichier, imprimée 7)
```

Contrôlez les vignettes avant d'aller plus loin :

```sh
xdg-open assets/img/03/cover-guide-supervision.webp
```

### Étape 4 — Ajouter la ligne dans la table « La collection »

Dans `index.html`, section `<section class="collection">`, à la fin du
`<tbody>` :

```html
        <tr>
          <td class="n">03</td>
          <td class="t"><a href="#c03">Superviser un agent en production</a></td>
          <td>Guide d'exploitation</td>
          <td class="r">v1.0 · 2026</td>
        </tr>
```

La colonne « Nature » reprend le mot qui figure dans le `<span class="genre">`
du cahier. Les trois valeurs en usage : *Guide de mise en œuvre*, *Guide de
conception*, *Article*.

### Étape 5 — Ajouter le cahier

Copiez le bloc de la [section 4](#4-le-bloc-de-cahier-à-copier) dans `<main>`,
**après le dernier `</article>`**, juste avant la balise `</main>`. Remplissez
les champs entre crochets. Aucun crochet ne doit subsister.

### Étape 6 — Déclarer le document dans le JSON-LD

Dans le `<head>`, tableau `hasPart`, ajoutez un objet :

```json
    {
      "@type": "DigitalDocument",
      "name": "Superviser un agent en production",
      "version": "1.0",
      "datePublished": "2026",
      "encodingFormat": "application/pdf",
      "url": "https://denislamard.github.io/publications/guide-supervision.pdf",
      "inLanguage": "fr"
    }
```

La virgule qui sépare les objets se place avant le nouveau bloc, pas après. Un
JSON-LD invalide passe inaperçu à l'œil et fait échouer la lecture par les
moteurs.

### Étape 7 — Vérifier en local

```sh
python3 -m http.server 8000
```

Ouvrez `http://localhost:8000` et contrôlez ces sept points :

- [ ] Les titres s'affichent en Source Serif, un serif à empattements fins.
      Un rendu Times ou Georgia signale que les woff2 ne se chargent pas.
- [ ] La couverture et les trois aperçus du nouveau cahier apparaissent.
- [ ] Le lien de la table « La collection » saute bien au nouveau cahier.
- [ ] Le bouton « Ouvrir le PDF » ouvre le bon fichier.
- [ ] La fiche technique affiche le bon nombre de pages et le bon poids.
- [ ] Aucun crochet `[ ]` ne reste visible.
- [ ] La console du navigateur ne signale aucune ressource en 404.

Ouvrir `index.html` en `file://` ne suffit pas : le navigateur bloque le
chargement des polices en cross-origin sur ce protocole, et la page tombe en
Georgia. Passez toujours par le serveur local.

### Étape 8 — Publier

```sh
git add .
git status                  # relire la liste, elle doit contenir le PDF,
                            # index.html et les 4 fichiers de assets/img/03/
git commit -m "add guide supervision"
git push
```

GitHub Pages met une à deux minutes à reconstruire. Vérifiez ensuite l'URL
publique et, si vous comptez partager le lien sur LinkedIn, repassez-le au
[Post Inspector](https://www.linkedin.com/post-inspector/) pour forcer le
rafraîchissement de l'aperçu.

### Étape 9 — Mettre à jour l'image de partage

`assets/img/og-image.png` affiche le nombre de titres et de pages de la
collection. Elle se régénère depuis `outils/og-image.html` : corrigez les
chiffres dans ce fichier, ouvrez-le dans un navigateur et capturez le bloc
`.og` en 1200 × 630. Cette étape peut attendre un lot de deux ou trois
publications.

---

## 4. Le bloc de cahier à copier

```html
<!-- ═══ CAHIER 03 ═══ -->
<article class="cahier" id="c03">
  <div class="large">

    <div class="entete">
      <span class="numero">03</span>
      <span class="genre">[Guide d'exploitation]</span>
      <span class="paru">[Version 1.0 · ]2026</span>
    </div>

    <div class="corps">

      <div class="texte">
        <h3><a href="[guide-supervision.pdf]">[Titre du document]</a></h3>
        <p class="sous">[Sous-titre : ce que le document couvre, une ligne.]</p>

        <p class="pitch">[Quatre à six lignes. Voir la section 5.]</p>

        <blockquote class="extrait">
          <p>«&#8239;[La phrase prélevée dans le document.]&#8239;»</p>
          <cite>§ [N] · [Titre de la section]</cite>
        </blockquote>

        <p class="titre-liste">Ce que vous y trouverez</p>
        <ul class="points">
          <li><strong>[Accroche]</strong> [suite de la ligne, avec un chiffre.]</li>
          <li><strong>[Accroche]</strong> [suite de la ligne.]</li>
          <li><strong>[Accroche]</strong> [suite de la ligne.]</li>
          <li><strong>[Accroche]</strong> [suite de la ligne.]</li>
        </ul>
      </div>

      <div class="fiche">
        <div class="socle">
          <img src="assets/img/03/cover-[nom-du-pdf].webp" alt="Couverture du guide [titre]" width="500" height="707" loading="lazy">
        </div>
        <dl class="specs">
          <div><dt>Format</dt><dd>PDF A4</dd></div>
          <div><dt>Pages</dt><dd>[N]</dd></div>
          <div><dt>Version</dt><dd class="v">[1.0]</dd></div>
          <div><dt>Lecture</dt><dd>[N]&nbsp;min</dd></div>
          <div><dt>Langue</dt><dd>Français</dd></div>
        </dl>
        <a class="bouton" href="[guide-supervision.pdf]">Ouvrir le PDF <span class="poids">[N]&nbsp;Ko</span></a>
      </div>

      <div class="apercus">
        <h4>Aperçu</h4>
        <div class="planche">
          <figure>
            <img src="assets/img/03/apercu-[nom-du-pdf]-1.webp" alt="Page [N] du guide : [contenu]" width="340" height="481" loading="lazy">
            <figcaption><b>Page [N]</b>[Ce que la page montre]</figcaption>
          </figure>
          <figure>
            <img src="assets/img/03/apercu-[nom-du-pdf]-2.webp" alt="Page [N] du guide : [contenu]" width="340" height="481" loading="lazy">
            <figcaption><b>Page [N]</b>[Ce que la page montre]</figcaption>
          </figure>
          <figure>
            <img src="assets/img/03/apercu-[nom-du-pdf]-3.webp" alt="Page [N] du guide : [contenu]" width="340" height="481" loading="lazy">
            <figcaption><b>Page [N]</b>[Ce que la page montre]</figcaption>
          </figure>
        </div>
      </div>

    </div>
  </div>
</article>
```

**Variantes**

- *Article court, sans aperçu* : supprimer le bloc `<div class="apercus">…</div>`
  et la ligne `Version` de la fiche technique.
- *Document sans couverture rendue* : remplacer le contenu de
  `<div class="socle">` par le carton typographique.

  ```html
  <div class="carton" role="img" aria-label="Couverture du document [titre]">
    <hr>
    <b>[Titre du document]</b>
    <span>Article · 2026</span>
  </div>
  ```

**Typographie**

La page emploie l'espace fine insécable `&#8239;` avant `? ! ; :` et à
l'intérieur des guillemets, et l'espace insécable `&nbsp;` entre un nombre et
son unité. Les deux sont déjà en place dans le gabarit ci-dessus, à conserver
dans le texte que vous écrivez.

---

## 5. Écrire les cinq textes

Un cahier porte cinq champs rédigés. Ce sont eux qui décident si le PDF est
ouvert ou non.

**Le sous-titre** (`<p class="sous">`) — une ligne, le champ couvert par le
document. Reprendre le sous-titre de la couverture du PDF.

**Le pitch** (`<p class="pitch">`) — quatre à six lignes. Ouvrir sur le problème
du lecteur plutôt que sur le sujet du document, dire ce que la lecture lui
donne, nommer le cas ou le fil conducteur employé. C'est le seul endroit où le
document se vend.

**L'extrait** (`<blockquote class="extrait">`) — une phrase prélevée telle
quelle dans le PDF, avec le numéro et le titre de sa section. Choisir celle qui
contredit une intuition courante plutôt que celle qui résume. Vérifier au
copier-coller que la phrase est exacte, elle est présentée comme une citation.

**Les quatre points** (`<ul class="points">`) — une accroche en gras, puis la
suite de la phrase. Mettre un chiffre vérifiable dans deux points sur quatre au
minimum. Les points annoncent ce que le lecteur trouvera, pas ce que le document
prétend être.

**Les légendes d'aperçu** (`<figcaption>`) — le numéro de page **imprimé**, puis
ce que la page montre, en quatre à six mots.

Trois règles valent pour l'ensemble de la page, et elles ont été gagnées une
fois : jamais de formulation en négatif, jamais de motif « X, pas Y », jamais
d'adjectif qui s'auto-évalue du type « complet » ou « éprouvé ».

---

## 6. Retirer ou renommer un document

**Retirer.** Supprimer le `<article>`, la ligne de la table, l'objet du JSON-LD
et le dossier `assets/img/<numéro>/`. Laisser le PDF en place si le lien a
circulé. Le numéro retiré ne se réattribue pas, la collection saute simplement
un cran.

**Renommer un PDF.** Le lien public change, donc à éviter. Si c'est nécessaire,
répercuter le nouveau nom sur les deux `href` du cahier, sur l'`url` du JSON-LD
et sur le README.

**Publier une nouvelle version d'un guide.** Remplacer le PDF sous le même nom,
regénérer les vignettes avec le même `--dossier`, puis mettre à jour trois
valeurs : le `<span class="paru">`, la ligne `Version` de la fiche technique et
la colonne « Format » de la table. Vérifier au passage que les pages d'aperçu
n'ont pas bougé de numéro.

---

## 7. Dépannage

| Symptôme | Cause | Correctif |
|---|---|---|
| La page s'affiche en Times ou Georgia | les six `woff2` de `assets/fonts/` ne sont pas dans le dépôt | `git status --ignored assets/fonts` puis vérifier la liste blanche du `.gitignore` |
| Un carré vide à la place d'une image | le fichier n'est pas parti dans le commit | `git check-ignore -v assets/img/03/cover-*.webp` |
| Aucun style, page en texte brut | `assets/css/style.css` absent ou 404 | même vérification |
| Une image manque en ligne mais pas en local | casse du nom de fichier | GitHub Pages distingue les majuscules, contrairement à certains systèmes de fichiers locaux |
| Le lien de la table ne saute nulle part | l'ancre `href="#cNN"` et l'`id="cNN"` divergent | aligner les deux sur le numéro du cahier |
| L'aperçu LinkedIn reste l'ancien | cache du réseau | repasser l'URL au Post Inspector |
| Le script échoue sur `pdftoppm` | poppler absent | `sudo apt install poppler-utils` |
| Le script échoue sur `PIL` | script lancé sans `uv` | `uv run outils/vignettes.py …` |

### La liste blanche du `.gitignore`

Ce dépôt ignore tout par défaut et n'autorise que ce qui est publié. Une
extension non déclarée est donc silencieusement absente du site, sans erreur ni
avertissement. Après avoir ajouté un type de fichier, contrôlez :

```sh
git add -An .        # ce qui serait ajouté
git check-ignore -v <fichier>   # pourquoi un fichier est écarté
```

---

**Denis Lamard** — concepteur et intégrateur d'agents IA
Le socle d'orchestration : [github.com/denislamard/loom](https://github.com/denislamard/loom)
Le détail technique et les cas d'usage : [denislamard.github.io](https://denislamard.github.io)
