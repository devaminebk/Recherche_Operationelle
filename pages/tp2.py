"""
TP2 — Modélisation sous forme de programme linéaire
  • Problème 1 : Poterie / Émaux (maximisation)
  • Problème 2 : Coussinets / Paliers (minimisation)
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ui.styles import inject_styles, page_header, lp_block, status_badge, section_pill
from core.solvers import solve_tp2_poterie, solve_tp2_coussinets
from plots.charts import plot_feasible_region_poterie, plot_production_bars

st.set_page_config(page_title="TP2 · Modélisation PL", page_icon="⚙️", layout="wide")
inject_styles()

page_header(
    "TP2 — Modélisation & Résolution",
    "Formulation et résolution de deux programmes linéaires",
    "⚙️",
)

# Sidebar selection
with st.sidebar:
    st.markdown("## ⚙️ TP2 — Navigation")
    st.markdown("---")
    problem = st.radio(
        "Choisir le problème",
        ["Problème 1 — Poterie & Émaux", "Problème 2 — Coussinets & Paliers"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Solveur : PuLP · CBC · Plotly · Streamlit")

# ══════════════════════════════════════════════════════════════════════════════
# PROBLÈME 1 — Poterie / Émaux
# ══════════════════════════════════════════════════════════════════════════════
if problem == "Problème 1 — Poterie & Émaux":
    col_enonce, col_form = st.columns([1, 1], gap="large")

    with col_enonce:
        section_pill("Énoncé & contraintes", "#FFA657")
        st.markdown("""
**Variables de décision :**
- `x` → nombre de **poteries**
- `y` → nombre d'**émaux sur cuivre**

**Données :**
- 1 h / poterie · 4 h / émail
- Charge émaux ≤ charge poterie + 160 h
- Production poterie ≤ production émaux + 30 u
- Total articles ≤ 80 u/jour
- Profit : 20 D / poterie · 60 D / émail
""")

    with col_form:
        section_pill("Formulation PL", "#58A6FF")
        lp_block("""\
max  Z = 20·x + 60·y

s.c.   4y − x     ≤ 160   (charge travail)
        x − y     ≤  30   (écart production)
        x + y     ≤  80   (total articles)
        x ≥ 0,  y ≥ 0""")

    st.markdown("---")
    if st.button("▶  Résoudre Poterie/Émaux", key="btn_pot"):
        st.session_state["pot_result"] = solve_tp2_poterie()

    r = st.session_state.get("pot_result")
    if r:
        section_pill("Résultat optimal", "#3FB950")
        status_badge(r["status"])
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Poteries (x)", f"{r['Poterie']:.2f}")
        c2.metric("Émaux (y)",    f"{r['Emaux']:.2f}")
        c3.metric("Bénéfice Z*",  f"{r['objective']:.2f} D")

        st.markdown("##### Saturation des contraintes")
        rhs_map = {"4y - x ≤ 160": 160, "x - y ≤ 30": 30, "x + y ≤ 80": 80}
        for key, lhs in r["constraints"].items():
            rhs = rhs_map[key]
            slack = rhs - lhs
            icon = "🔴" if abs(slack) < 1e-4 else "🟢"
            st.markdown(f"**{key}** → `{lhs:.2f}` / `{rhs}` &nbsp; {icon} slack = `{slack:.4f}`")

        col_a, col_b = st.columns(2)
        with col_a:
            st.plotly_chart(plot_feasible_region_poterie(r), use_container_width=True)
        with col_b:
            st.plotly_chart(
                plot_production_bars(
                    {"Poterie": r["Poterie"], "Émaux": r["Emaux"]},
                    "Quantités produites / jour", "unités"
                ),
                use_container_width=True,
            )
    else:
        st.info("Cliquez sur **▶ Résoudre** pour obtenir la solution optimale.", icon="💡")


# ══════════════════════════════════════════════════════════════════════════════
# PROBLÈME 2 — Coussinets & Paliers
# ══════════════════════════════════════════════════════════════════════════════
elif problem == "Problème 2 — Coussinets & Paliers":
    col_enonce2, col_form2 = st.columns([1, 1], gap="large")

    with col_enonce2:
        section_pill("Énoncé & contraintes", "#FFA657")
        st.markdown("""
**Variables de décision :**
- `x` → **Coussinets (A)**
- `y` → **Paliers (B)**

**Données :**
- x ≥ 4 000 · y ≥ 5 000
- Matière première : 2x + 3y ≥ 36 000 kg
- Main d'œuvre : x + 0.5y ≤ 10 000 h
- Coût transport = (4x+6y) + (3x+4y) = **7x + 10y**
""")

    with col_form2:
        section_pill("Formulation PL", "#58A6FF")
        lp_block("""\
min  Z = 7·x + 10·y

s.c.   x           ≥  4 000   (min coussinets)
        y           ≥  5 000   (min paliers)
       2x + 3y      ≥ 36 000   (matière 1ère)
        x + 0.5y   ≤ 10 000   (main d'œuvre)
        x ≥ 0,  y ≥ 0""")

    st.markdown("---")
    if st.button("▶  Résoudre Coussinets/Paliers", key="btn_cous"):
        st.session_state["cous_result"] = solve_tp2_coussinets()

    r2 = st.session_state.get("cous_result")
    if r2:
        section_pill("Résultat optimal", "#3FB950")
        status_badge(r2["status"])
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Coussinets (x)", f"{r2['Coussinets']:.0f}")
        c2.metric("Paliers (y)",    f"{r2['Paliers']:.0f}")
        c3.metric("Coût min Z*",    f"{r2['objective']:.2f} D")

        st.markdown("##### Vérification des contraintes")
        bounds = {
            "Coussinets ≥ 4000":        ("≥", 4000),
            "Paliers ≥ 5000":           ("≥", 5000),
            "2x + 3y ≥ 36000 (MP)":    ("≥", 36000),
            "x + 0.5y ≤ 10000 (MO)":   ("≤", 10000),
        }
        for key, (op, bound) in bounds.items():
            val = r2["constraints"][key]
            ok = (val >= bound - 1e-4) if op == "≥" else (val <= bound + 1e-4)
            icon = "✅" if ok else "❌"
            st.markdown(f"{icon} **{key}** → `{val:.0f}` {op} `{bound}`")

        st.plotly_chart(
            plot_production_bars(
                {"Coussinets": r2["Coussinets"], "Paliers": r2["Paliers"]},
                "Plan de production optimal", "unités"
            ),
            use_container_width=True,
        )
    else:
        st.info("Cliquez sur **▶ Résoudre** pour obtenir la solution optimale.", icon="💡")