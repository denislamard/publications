# Publications

Guides et articles sur la conception et l'exploitation d'agents IA dans des
processus métier. Chaque document est publié en PDF et se lit directement dans
GitHub.

**Denis Lamard** — concepteur et intégrateur d'agents IA
Le socle d'orchestration : [github.com/denislamard/loom](https://github.com/denislamard/loom)
Le détail technique et les cas d'usage : [denislamard.github.io](https://denislamard.github.io)

---

## Les documents

### [Intégrer un agent IA dans un processus métier](guide-agent-ia.pdf)

*Guide de mise en œuvre · version 1.3, 2026 · 18 pages*

Écrit pour la personne qui décide de brancher un agent et qui portera la
responsabilité du résultat : direction technique, responsable des opérations,
dirigeant de PME ou d'ETI. Le guide présente une méthode plutôt qu'une
technologie, et se déroule sur une boîte mail partagée, un cas que toutes les
organisations connaissent et qui se transpose à la relance commerciale, au
traitement de commandes ou au tri de tickets ou autres cas métier.

**Ce qu'il contient**

- Le test qui tranche entre un agent et un workflow : peut-on énumérer les
  branches du processus ?
- Une grille d'éligibilité scorée sur quatre critères : volume, valeur unitaire,
  réversibilité, mesurabilité.
- Les 3 principes d'architecture qui confinent le non-déterminisme :
  orchestrateur déterministe, règles métier dans le code, écritures idempotentes
- La vérification de sortie sur deux niveaux, contrat structurel puis juge
  sémantique, avec le coût du contrôle chiffré
- Un déploiement en quatre marches, du mode shadow à l'autonomie, avec les
  seuils de passage
- La baseline à relever avant le branchement, l'instrumentation à émettre et les
  deux plafonds à poser
- Les points de conformité RGPD à traiter en amont plutôt qu'à la mise en
  production
- Les sept défaillances les plus fréquentes en production, avec leur parade
- Le périmètre à laisser hors automatisation, et pourquoi
- Une checklist de seize points avant ouverture sur le flux réel

---

