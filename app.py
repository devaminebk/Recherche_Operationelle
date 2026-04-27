"""
app.py — Point d'entrée principal de l'application Streamlit.
Lance la page d'accueil et configure la navigation multi-pages.
"""

import streamlit as st
from ui.styles import inject_styles, page_header, section_pill

st.set_page_config(
    page_title="RO · Recherche Opérationnelle",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 RO — Navigation")
    st.markdown("---")
    st.markdown("""
- [📐 TP1 — Programmation Linéaire](./tp1)
- [⚙️ TP2 — Modélisation PL](./tp2)
- [🚚 TP3 — Problème de Transport](./tp3)
""")
    st.markdown("---")
    st.caption("Solveur : PuLP · CBC · Plotly · Streamlit")

# ── Hero ───────────────────────────────────────────────────────
page_header(
    "Recherche Opérationnelle",
    "Visualisation interactive des TPs — résolution via PuLP (équivalent Solveur Excel)",
    "🔬",
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    section_pill("TP1 — Programmation Linéaire", "#58A6FF")
    st.markdown("""
**Deux exercices de PL :**
- LP simple : `max 2x₁ + 3x₂` avec 3 contraintes
- KS Confection : 3 tissus, 3 machines

→ Région réalisable, point optimal, saturation des contraintes.
""")
    st.page_link("pages/tp1.py", label="Ouvrir TP1 →", icon="📐")

with col2:
    section_pill("TP2 — Modélisation PL", "#FFA657")
    st.markdown("""
**Deux problèmes de modélisation :**
- Poterie & Émaux : maximisation du bénéfice
- Coussinets & Paliers : minimisation du coût

→ Formulation, résolution, visualisation graphique.
""")
    st.page_link("pages/tp2.py", label="Ouvrir TP2 →", icon="⚙️")

with col3:
    section_pill("TP3 — Transport & Production", "#3FB950")
    st.markdown("""
**Deux modèles avancés :**
- CARCO : production voitures & camions
- Transport : matrice 3×4, minimisation du coût

→ Heatmap, flux Sankey, plan optimal.
""")
    st.page_link("pages/tp3.py", label="Ouvrir TP3 →", icon="🚚")

st.markdown("---")
st.caption("Projet RO · Python 3 · PuLP · Streamlit · Plotly")
