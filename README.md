# RO · Recherche Opérationnelle

Visualisation interactive des Travaux Pratiques de Recherche Opérationnelle utilisant Python, Streamlit, PuLP et Plotly.

## Description

Cette application Streamlit permet de résoudre et visualiser interactivement les problèmes de programmation linéaire et de transport issus des TPs de Recherche Opérationnelle.

### Fonctionnalités

- **TP1 — Programmation Linéaire**
  - Exercice 1 : LP simple (max 2x₁ + 3x₂)
  - Exercice 2 : KS Confection (3 produits, 3 machines)

- **TP2 — Modélisation PL**
  - Problème 1 : Poterie & Émaux (maximisation)
  - Problème 2 : Coussinets & Paliers (minimisation)

- **TP3 — Transport & Production**
  - Problème 1 : CARCO (production voitures/camions)
  - Problème 2 : Problème de transport (matrice 3×4)

### Technologies utilisées

- **PuLP** : Solveur de programmation linéaire (CBC)
- **Streamlit** : Interface web interactive
- **Plotly** : Graphiques et visualisations
- **Pandas** : Manipulation de données
- **NumPy** : Calculs numériques

## Installation

1. Cloner le repository :
   ```bash
   git clone <url>
   cd RO_TP
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancer l'application :
   ```bash
   streamlit run app.py
   ```

## Structure du projet

```
RO_TP/
├── app.py                 # Point d'entrée principal
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── core/                 # Solveurs PuLP
│   ├── __init__.py
│   └── solvers.py        # Fonctions de résolution
├── pages/                # Pages Streamlit
│   ├── __init__.py
│   ├── tp1.py            # TP1 - PL
│   ├── tp2.py            # TP2 - Modélisation
│   └── tp3.py            # TP3 - Transport
├── plots/                # Graphiques Plotly
│   ├── __init__.py
│   └── charts.py         # Fonctions de visualisation
└── ui/                   # Interface utilisateur
    ├── __init__.py
    └── styles.py         # Styles CSS et helpers
```

## Utilisation

Après avoir lancé l'application, naviguez dans la sidebar pour accéder aux différents TPs. Chaque page contient :

- L'énoncé du problème
- La formulation mathématique
- Un bouton de résolution
- Les résultats optimaux
- Des graphiques interactifs

## Contributeurs

Développé pour les cours de Recherche Opérationnelle.

## Licence

MIT