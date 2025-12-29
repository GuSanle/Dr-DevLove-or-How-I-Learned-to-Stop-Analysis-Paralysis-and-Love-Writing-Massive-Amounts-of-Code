# Dr. DevLove
### *ou : Comment j'ai appris à cesser de m'inquiéter et à aimer écrire énormément de code*

[![GitHub license](https://img.shields.io/github/license/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code)](https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code/blob/main/LICENSE)

> "Messieurs, vous ne pouvez pas vous battre ici ! C'est la salle de guerre !" — *Dr. Folamour*
>
> "Développeurs, vous ne pouvez pas trop réfléchir ici ! C'est l'IDE !" — *Dr. DevLove*

Êtes-vous fatigué de fixer un curseur vide ? Souffrez-vous de *Paralysie par l'Analyse* chronique ? Passez-vous plus de temps à planifier votre code qu'à l'écrire ?

**Dr. DevLove** (alias `gh-stats`) est votre ordonnance. C'est un outil CLI qui prouve que vous *travaillez* vraiment. Il valide votre existence en suivant vos contributions quotidiennes de code à travers l'univers GitHub, sans avoir besoin de clones locaux car qui a de l'espace disque pour ça ?

---

[English](./README.md) | [🇨🇳 中文](./README.zh-CN.md) | [🇪🇸 Español](./README.es.md) | [🇸🇦 العربية](./README.ar.md) | [🇮🇳 हिन्दी](./README.hi.md)

---

## 💊 L'Ordonnance (Fonctionnalités)

*   **Diagnostic à Distance**: Scanne votre activité GitHub directement via API. Aucun dépôt local requis.
*   **Signes Vitaux**: Magnifique sortie terminal colorée avec des barres de progression qui tournent plus vite que votre syndrome de l'imposteur.
*   **Traitement Évolutif**: Fonctionne aussi bien pour les projets personnels que pour les organisations massives.
*   **Voyage dans le Temps**: Vérifiez vos statistiques pour `today` (aujourd'hui), `week` (semaine), `month` (mois) ou `year` (année).

## 📥 Prise (Installation)

```bash
brew install gh
gh auth login
gh auth refresh -s read:org  # Requis pour les organisations
```

Clonez ce dépôt massif et installez avec Poetry :

```bash
git clone https://github.com/forestsheep911/Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code.git
cd Dr-DevLove-or-How-I-Learned-to-Stop-Analysis-Paralysis-and-Love-Writing-Massive-Amounts-of-Code
poetry install
```

## 📋 Dosage (Utilisation)

```bash
# Vérifiez que vous avez fait quelque chose aujourd'hui
poetry run gh-stats --range today

# Prouvez à votre patron que vous avez travaillé ce mois-ci
poetry run gh-stats --range month --orgs VOTRE_ORG
```

## 📄 Licence

MIT. Faites ce que vous voulez, écrivez juste du code.
