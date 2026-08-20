#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow>=11"]
# ///
"""Génère la couverture et les aperçus d'un PDF pour la page des publications.

Le rendu PDF passe par poppler, qui est un binaire système :

    sudo apt install poppler-utils

Les dépendances Python sont déclarées dans l'en-tête PEP 723 ci-dessus, donc
uv construit l'environnement tout seul au premier appel et le met en cache :

    uv run outils/vignettes.py guide-agent-ia.pdf --pages 8 11 13 --dossier 01

Le script est exécutable directement si le bit +x est posé :

    chmod +x outils/vignettes.py
    ./outils/vignettes.py guide-agent-ia.pdf --pages 8 11 13 --dossier 01

Les numéros de --pages sont ceux du fichier PDF, pas ceux imprimés en pied de
page. Un guide dont la couverture n'est pas numérotée a un décalage de 1.

Sortie, dans assets/img/<dossier>/ si --dossier est donné, sinon assets/img/ :
    cover-<cle>.webp        la page 1, 500 px de large
    motif-<cle>.webp        le bandeau graphique de la couverture, détouré
    apercu-<cle>-1..3.webp  les pages demandées, 340 px de large

La clé vaut par défaut le nom du PDF sans extension, ce qui donne des noms de
fichiers lisibles dans le dépôt : cover-guide-agent-ia.webp.

Le script affiche ensuite les valeurs à recopier dans index.html.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageChops
except ImportError:  # pragma: no cover
    sys.exit(
        "Pillow est absent de l'environnement.\n"
        "Lancez le script avec uv, qui lit l'en-tête PEP 723 :\n"
        "    uv run outils/vignettes.py …"
    )

RACINE = Path(__file__).resolve().parent.parent
IMAGES = RACINE / "assets" / "img"

LARGEUR_COUVERTURE = 500
LARGEUR_APERCU = 340
LARGEUR_MOTIF = 1000


def verifier_outils() -> None:
    for outil in ("pdftoppm", "pdfinfo"):
        if shutil.which(outil) is None:
            sys.exit(f"{outil} est introuvable : sudo apt install poppler-utils")


def nombre_de_pages(pdf: Path) -> int:
    sortie = subprocess.run(
        ["pdfinfo", str(pdf)], capture_output=True, text=True, check=True
    ).stdout
    for ligne in sortie.splitlines():
        if ligne.startswith("Pages:"):
            return int(ligne.split(":")[1])
    return 0


def rendre(pdf: Path, page: int, dossier: Path, resolution: int) -> Path:
    prefixe = dossier / f"p{page}"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(resolution),
         "-f", str(page), "-l", str(page), str(pdf), str(prefixe)],
        check=True,
    )
    rendus = sorted(dossier.glob(f"p{page}-*.png"))
    if not rendus:
        sys.exit(f"Le rendu de la page {page} a échoué.")
    return rendus[0]


def enregistrer(source: Path, cible: Path, largeur: int, qualite: int) -> None:
    image = Image.open(source).convert("RGB")
    hauteur = round(image.height * largeur / image.width)
    cible.parent.mkdir(parents=True, exist_ok=True)
    image.resize((largeur, hauteur), Image.LANCZOS).save(
        cible, "WEBP", quality=qualite, method=6
    )
    poids = cible.stat().st_size // 1024
    print(f"  {cible.relative_to(RACINE)}  {largeur}×{hauteur}  {poids} Ko")


def extraire_motif(couverture: Path, cible: Path) -> bool:
    """Détoure le bandeau graphique situé dans le tiers supérieur de la page."""
    image = Image.open(couverture).convert("RGB")
    haut = image.crop((0, 0, image.width, int(image.height * 0.35)))
    blanc = Image.new("RGB", haut.size, (255, 255, 255))
    cadre = ImageChops.difference(haut, blanc).getbbox()
    if cadre is None:
        return False
    marge = 24
    motif = haut.crop((
        max(0, cadre[0] - marge),
        max(0, cadre[1] - marge),
        min(haut.width, cadre[2] + marge),
        min(haut.height, cadre[3] + marge),
    ))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as fichier:
        motif.save(fichier.name)
        enregistrer(Path(fichier.name), cible, LARGEUR_MOTIF, 86)
    return True


def main() -> None:
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument("pdf", type=Path)
    analyseur.add_argument("--pages", type=int, nargs="*", default=[],
                           help="pages du PDF à rendre en aperçu, trois de préférence")
    analyseur.add_argument("--cle", default=None,
                           help="suffixe des fichiers produits, par défaut le nom du PDF")
    analyseur.add_argument("--dossier", default=None,
                           help="sous-dossier de assets/img/ où écrire, par exemple 03")
    analyseur.add_argument("--motif", action="store_true",
                           help="extraire aussi le bandeau graphique de la couverture")
    arguments = analyseur.parse_args()

    verifier_outils()
    pdf = arguments.pdf
    if not pdf.is_file():
        sys.exit(f"Fichier introuvable : {pdf}")

    cle = arguments.cle or pdf.stem
    sortie = IMAGES / arguments.dossier if arguments.dossier else IMAGES
    total = nombre_de_pages(pdf)
    poids = pdf.stat().st_size // 1024

    print(f"\n{pdf.name} — {total} pages dans le fichier, {poids} Ko\n")

    with tempfile.TemporaryDirectory() as temporaire:
        dossier = Path(temporaire)

        print("Couverture")
        page_un = rendre(pdf, 1, dossier, 150)
        enregistrer(page_un, sortie / f"cover-{cle}.webp", LARGEUR_COUVERTURE, 82)

        if arguments.motif:
            print("Motif")
            if not extraire_motif(page_un, sortie / f"motif-{cle}.webp"):
                print("  aucun motif détecté sur le tiers supérieur")

        if arguments.pages:
            print("Aperçus")
            for rang, page in enumerate(arguments.pages, 1):
                if page < 1 or page > total:
                    print(f"  page {page} hors du document, ignorée")
                    continue
                rendu = rendre(pdf, page, dossier, 110)
                enregistrer(rendu, sortie / f"apercu-{cle}-{rang}.webp",
                            LARGEUR_APERCU, 74)

    relatif = sortie.relative_to(RACINE).as_posix()
    print("\nÀ recopier dans index.html")
    print(f"  poids du fichier   : {poids} Ko")
    print(f"  pages imprimées    : {total - 1} (si la couverture n'est pas numérotée)")
    print(f"  couverture         : {relatif}/cover-{cle}.webp")
    for rang, page in enumerate(arguments.pages, 1):
        print(f"  aperçu {rang}           : {relatif}/apercu-{cle}-{rang}.webp"
              f"   (page {page} du fichier, imprimée {page - 1})")
    print()


if __name__ == "__main__":
    main()
