"""
TP1 — Programmation Linéaire
  • Simple LP : max 2x1 + 3x2
  • KS Confection : 3 tissus, 3 machines
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ui.styles import inject_styles, page_header, lp_block, result_card, status_badge, section_pill
from core.solvers import solve_tp1_simple, solve_tp1_ks
from plots.charts import (
    plot_feasible_region_simple,
    plot_production_bars,
    plot_ks_radar,
)

st.set_page_config(page_title="TP1 · Programmation Linéaire", page_icon="📐", layout="wide")
inject_styles()

page_header(
    "TP1 — Programmation Linéaire",
    "Résolution via PuLP (équivalent Solveur Excel)",
    "📐",
)

# Sidebar selection
with st.sidebar:
    st.markdown("## 📐 TP1 — Navigation")
    st.markdown("---")
    problem = st.radio(
        "Choisir l'exercice",
        ["Exercice 1 — LP Simple", "Exercice 2 — KS Confection"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Solveur : PuLP · CBC · Plotly · Streamlit")

# ══════════════════════════════════════════════════════════════════════════════
# EXERCICE 1 — LP Simple
# ══════════════════════════════════════════════════════════════════════════════
if problem == "Exercice 1 — LP Simple":
    col_form, col_res = st.columns([1, 1], gap="large")

    with col_form:
        section_pill("Formulation mathématique", "#58A6FF")
        lp_block("""\
max  Z = 2·x₁ + 3·x₂

s.c.   x₁  + 6·x₂  ≤  30    (R1)
       2·x₁ + 2·x₂  ≤  15    (R2)
       4·x₁ +   x₂  ≤  24    (R3)
       x₁ ≥ 0,  x₂ ≥ 0""")

        st.markdown("---")
        if st.button("▶  Résoudre", key="btn_simple"):
            st.session_state["simple_result"] = solve_tp1_simple()

    with col_res:
        r = st.session_state.get("simple_result")
        if r:
            section_pill("Résultat optimal", "#3FB950")
            status_badge(r["status"])
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("x₁", f"{r['x1']:.4f}")
            c2.metric("x₂", f"{r['x2']:.4f}")
            c3.metric("Z*  (max)", f"{r['objective']:.4f}")

            st.markdown("##### Saturation des contraintes")
            for name, data in r["constraints"].items():
                slack = data["rhs"] - data["lhs"]
                icon = "🔴" if slack < 1e-6 else "🟢"
                st.markdown(
                    f"**{name}** &nbsp;&nbsp; `{data['lhs']:.4f}` / `{data['rhs']}` &nbsp; {icon} slack = `{slack:.4f}`"
                )
        else:
            st.info("Appuyez sur **▶ Résoudre** pour lancer le solveur.", icon="💡")

    # Graph always visible after solve
    r = st.session_state.get("simple_result")
    if r:
        st.plotly_chart(plot_feasible_region_simple(r), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# EXERCICE 2 — KS Confection
# ══════════════════════════════════════════════════════════════════════════════
elif problem == "Exercice 2 — KS Confection":
    col_form2, col_res2 = st.columns([1, 1], gap="large")

    with col_form2:
        section_pill("Contexte & données", "#D2A8FF")
        st.markdown("""
**KS Confection** fabrique 3 tissus : **Laine**, **Coton**, **Soie**.

| | Laine | Coton | Soie | Dispo |
|---|---|---|---|---|
| Filature (h) | 3 | 2 | 4 | 120 |
| Tissage (h) | 8 | 7 | 4 | 150 |
| Ennoblissement (h) | 0.7 | 0.6 | 0.3 | 100 |
| **Profit (DTN)** | **7** | **10** | **12** | |

*NB : filature cotonnière ≤ 40 m ; filature laine ≤ 80 m.*
""")

        section_pill("Formulation PL", "#58A6FF")
        lp_block("""\
Variables : x₁=Laine, x₂=Coton, x₃=Soie

max  Z = 7·x₁ + 10·x₂ + 12·x₃

s.c.   3·x₁ + 2·x₂ + 4·x₃  ≤ 120   (Filature)
       8·x₁ + 7·x₂ + 4·x₃  ≤ 150   (Tissage)
     0.7·x₁+ 0.6·x₂+ 0.3·x₃≤ 100   (Ennoblissement)
       x₂ ≤ 40,  x₁ ≤ 80
       x₁, x₂, x₃ ≥ 0""")

        st.markdown("---")
        if st.button("▶  Résoudre KS Confection", key="btn_ks"):
            st.session_state["ks_result"] = solve_tp1_ks()

    with col_res2:
        r2 = st.session_state.get("ks_result")
        if r2:
            section_pill("Plan de production optimal", "#3FB950")
            status_badge(r2["status"])
            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Laine (m)", f"{r2['Laine']:.1f}")
            c2.metric("Coton (m)", f"{r2['Coton']:.1f}")
            c3.metric("Soie (m)",  f"{r2['Soie']:.1f}")
            c4.metric("Profit Z*", f"{r2['objective']:.2f} DTN")

            st.markdown("##### Utilisation des machines")
            caps = {"Filature (≤120h)": 120, "Tissage (≤150h)": 150, "Ennoblissement (≤100h)": 100}
            for key, used in r2["constraints"].items():
                cap = caps[key]
                pct = used / cap * 100
                bar = "█" * int(pct // 5) + "░" * (20 - int(pct // 5))
                icon = "🔴" if pct > 99 else ("🟡" if pct > 80 else "🟢")
                st.markdown(f"`{key}` {icon}  `{bar}` {pct:.1f}%")
        else:
            st.info("Appuyez sur **▶ Résoudre KS Confection** pour démarrer.", icon="💡")

    r2 = st.session_state.get("ks_result")
    if r2:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_bar = plot_production_bars(
                {"Laine": r2["Laine"], "Coton": r2["Coton"], "Soie": r2["Soie"]},
                "Quantités produites",
                unit="mètres"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        with col_b:
            st.plotly_chart(plot_ks_radar(r2), use_container_width=True)