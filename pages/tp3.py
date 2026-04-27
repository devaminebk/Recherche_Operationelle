"""
TP3 — Problème de Transport & Production CARCO
  • CARCO : maximisation du profit (voitures & camions)
  • Transport : minimisation du coût (matrice 3x4)
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ui.styles import inject_styles, page_header, lp_block, result_card, status_badge, section_pill
from core.solvers import solve_tp3_carco, solve_tp3_transport
from plots.charts import (
    plot_production_bars,
    plot_transport_heatmap,
    plot_transport_flow,
    plot_carco_profit_pie,
    plot_carco_feasible_region,
    plot_transport_cost_heatmaps,
    plot_transport_sankey,
    plot_transport_cost_bars,
)
import pandas as pd
import numpy as np

st.set_page_config(page_title="TP3 · Transport & Production", page_icon="🚚", layout="wide")
inject_styles()

page_header(
    "TP3 — Transport & Production",
    "Modèles de production (CARCO) et de transport (matrice 3×4)",
    "🚚",
)

# Sidebar selection
with st.sidebar:
    st.markdown("## 🚚 TP3 — Navigation")
    st.markdown("---")
    problem = st.radio(
        "Choisir le problème",
        ["Problème 1 — CARCO", "Problème 2 — Transport"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Solveur : PuLP · CBC · Plotly · Streamlit")

# ══════════════════════════════════════════════════════════════════════════════
# PROBLÈME 1 — CARCO
# ══════════════════════════════════════════════════════════════════════════════
if problem == "Problème 1 — CARCO":

    st.markdown("## Problème 1 — CARCO")
    st.markdown('<span style="display:inline-block; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(88,166,255,.18); color:#58A6FF; border:1px solid rgba(88,166,255,.3);">Programmation Linéaire</span> '
                '<span style="display:inline-block; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(63,185,80,.18); color:#3FB950; border:1px solid rgba(63,185,80,.3);">Maximisation</span>', unsafe_allow_html=True)
    st.markdown("")

    # ── Énoncé & Modèle ───────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Énoncé & Modèle", "⚙️ Résolution", "📊 Analyse", "📈 Visualisation"])

    with tab1:
        col1, col2 = st.columns([1.1, 1])

        with col1:
            st.markdown("""
            <div style="background:#161B22; border:1px solid #30363D; border-radius:8px; padding:1.4rem 1.6rem; margin-bottom:1rem;">
            <b>Contexte</b><br><br>
            CARCO fabrique des <b>voitures</b> et des <b>camions</b>.<br>
            Contribution au profit : <b>300 DA/voiture</b>, <b>400 DA/camion</b>.<br>
            Les machines de type 1 sont louées à <b>50 DA/machine/jour</b>.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Tableau des ressources")
            df_res = pd.DataFrame({
                "Ressource": ["Machine type 1 (jours)", "Machine type 2 (jours)", "Acier (tonnes)"],
                "Voiture": [0.8, 0.6, 2],
                "Camion": [1.0, 0.7, 3],
                "Disponible": ["≤ 98 (louées)", "≤ 73", "≤ 260"],
            })
            st.dataframe(df_res, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("#### Formulation LP")
            lp_block("""\
Variables de décision
Voitures  : nb voitures/jour
Camions   : nb camions/jour
Machines1 : nb machines type 1 louées

MAX Z = 300·Voitures + 400·Camions - 50·Machines1

S.T.
  // Machine type 1
  0.8·Voitures + 1·Camions ≤ Machines1
  Machines1 ≤ 98

  // Machine type 2
  0.6·Voitures + 0.7·Camions ≤ 73

  // Acier
  2·Voitures + 3·Camions ≤ 260

  // Marketing
  Voitures  ≥ 88
  Camions   ≥ 26

  // Non-négativité
  Voitures, Camions, Machines1 ≥ 0""")

    # ── Résolution ───────────────────────────────────────────────────────
    result = solve_tp3_carco()

    with tab2:
        st.markdown(f"#### Statut : {status_badge(result['status'])}", unsafe_allow_html=True)
        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🚗 Voitures/jour", f"{result['Voitures']:.1f}")
        col2.metric("🚛 Camions/jour",  f"{result['Camions']:.1f}")
        col3.metric("🔧 Machines louées", f"{result['Machines1']:.1f}")
        col4.metric("💰 Profit optimal", f"{result['objective']:,.0f} DA")

        st.markdown("---")
        st.markdown("#### Vérification des contraintes")

        constraints_data = {
            "Contrainte": [
                "Machine type 1 (usage ≤ Machines1)",
                "Machines1 ≤ 98",
                "Machine type 2 (≤ 73)",
                "Acier (≤ 260)",
                "Voitures ≥ 88",
                "Camions ≥ 26",
            ],
            "LHS": [
                f"{0.8*result['Voitures'] + result['Camions']:.2f}",
                f"{result['Machines1']:.2f}",
                f"{0.6*result['Voitures'] + 0.7*result['Camions']:.2f}",
                f"{2*result['Voitures'] + 3*result['Camions']:.2f}",
                f"{result['Voitures']:.2f}",
                f"{result['Camions']:.2f}",
            ],
            "Opérateur": ["≤ Machines1", "≤ 98", "≤ 73", "≤ 260", "≥ 88", "≥ 26"],
            "Slack": [
                f"{result['Machines1'] - (0.8*result['Voitures'] + result['Camions']):.2f}",
                f"{98 - result['Machines1']:.2f}",
                f"{73 - (0.6*result['Voitures'] + 0.7*result['Camions']):.2f}",
                f"{260 - (2*result['Voitures'] + 3*result['Camions']):.2f}",
                f"{result['Voitures'] - 88:.2f}",
                f"{result['Camions'] - 26:.2f}",
            ],
            "Saturée ?": [
                "✓" if abs(result['Machines1'] - (0.8*result['Voitures'] + result['Camions'])) < 1e-4 else "—",
                "✓" if abs(98 - result['Machines1']) < 1e-4 else "—",
                "✓" if abs(73 - (0.6*result['Voitures'] + 0.7*result['Camions'])) < 1e-4 else "—",
                "✓" if abs(260 - (2*result['Voitures'] + 3*result['Camions'])) < 1e-4 else "—",
                "✓" if abs(result['Voitures'] - 88) < 1e-4 else "—",
                "✓" if abs(result['Camions'] - 26) < 1e-4 else "—",
            ],
        }
        st.dataframe(pd.DataFrame(constraints_data), hide_index=True, use_container_width=True)

    with tab3:
        st.markdown("#### Décomposition du profit")
        rev_v = 300 * result['Voitures']
        rev_c = 400 * result['Camions']
        cost_m = 50 * result['Machines1']

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_carco_profit_pie(result), use_container_width=True)

        with col2:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #161B22 0%, #1C2333 100%); border:1px solid #3FB950; border-radius:10px; padding:20px 24px; margin:12px 0;">
            <div style="color:#8B949E; font-size:0.78rem; text-transform:uppercase; letter-spacing:.08em;">Décomposition du profit optimal</div><br>
            Revenu voitures&nbsp;&nbsp;&nbsp;: <b>{rev_v:,.0f} DA</b><br>
            Revenu camions&nbsp;&nbsp;&nbsp;&nbsp;: <b>{rev_c:,.0f} DA</b><br>
            Coût machines&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: <b>- {cost_m:,.0f} DA</b><br>
            <hr style="border-color:#30363D; margin: 0.8rem 0">
            <span style="font-size:1.1rem">Profit net&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: <b style="color:#3FB950">{result['objective']:,.0f} DA</b></span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#161B22; border:1px solid #30363D; border-radius:8px; padding:1.4rem 1.6rem;">
            <b>Utilisation des ressources</b><br><br>
            Machine type 1 : {0.8*result['Voitures'] + result['Camions']:.1f} / {result['Machines1']:.1f} louées<br>
            Machine type 2 : {0.6*result['Voitures'] + 0.7*result['Camions']:.1f} / 73 disponibles<br>
            Acier&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: {2*result['Voitures'] + 3*result['Camions']:.1f} / 260 tonnes
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("#### Région réalisable (Voitures vs Camions)")
        st.markdown('<div style="font-size:0.82rem; color:#8B949E">Projection 2D en fixant Machines1 à sa valeur optimale</div>', unsafe_allow_html=True)

        st.plotly_chart(plot_carco_feasible_region(result), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROBLÈME 2 — TRANSPORT
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("## Problème 2 — Problème de Transport")
    st.markdown('<span style="display:inline-block; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(88,166,255,.18); color:#58A6FF; border:1px solid rgba(88,166,255,.3);">Programmation Linéaire</span> '
                '<span style="display:inline-block; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(247,129,102,.18); color:#F78166; border:1px solid rgba(247,129,102,.3);">Minimisation</span>', unsafe_allow_html=True)
    st.markdown("")

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Énoncé & Modèle", "⚙️ Résolution", "📊 Matrices", "📈 Visualisation"])

    # Données
    costs = [
        [264, 130, 139, 160],
        [279, 244, 146, 307],
        [200, 166,  66, 278],
    ]
    supply = [9, 17, 9]       # offres (sources)
    demand = [10, 14, 7, 4]   # demandes (destinations)
    sources = ["Source 1", "Source 2", "Source 3"]
    dests   = ["Dest 1",  "Dest 2",  "Dest 3",  "Dest 4"]

    with tab1:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("""
            <div style="background:#161B22; border:1px solid #30363D; border-radius:8px; padding:1.4rem 1.6rem;">
            <b>Problème de transport</b><br><br>
            Minimiser le coût total d'acheminement de marchandises
            depuis <b>3 sources</b> vers <b>4 destinations</b>.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Matrice des coûts")
            df_costs = pd.DataFrame(costs, index=sources, columns=dests)
            df_costs["Offre"] = supply
            st.dataframe(df_costs, use_container_width=True)

            df_dem = pd.DataFrame([demand], columns=dests, index=["Demande"])
            st.dataframe(df_dem, use_container_width=True)

            total_supply = sum(supply)
            total_demand = sum(demand)
            bal = "✓ Équilibré" if total_supply == total_demand else f"⚠ Déséquilibré (offre={total_supply}, demande={total_demand})"
            st.markdown(f'<span style="display:inline-block; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(63,185,80,.18); color:#3FB950; border:1px solid rgba(63,185,80,.3);">{bal}</span>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### Formulation LP")
            lp_block("""\
MIN Z = 264x₁₁ + 130x₁₂ + 139x₁₃ + 160x₁₄
     + 279x₂₁ + 244x₂₂ + 146x₂₃ + 307x₂₄
     + 200x₃₁ + 166x₃₂ + 66x₃₃  + 278x₃₄

S.T.
  // Contraintes d'offre
  x₁₁ + x₁₂ + x₁₃ + x₁₄  = 9
  x₂₁ + x₂₂ + x₂₃ + x₂₄  = 17
  x₃₁ + x₃₂ + x₃₃ + x₃₄  = 9

  // Contraintes de demande
  x₁₁ + x₂₁ + x₃₁ = 10
  x₁₂ + x₂₂ + x₃₂ = 14
  x₁₃ + x₂₃ + x₃₃ = 7
  x₁₄ + x₂₄ + x₃₄ = 4

  // Non-négativité
  xᵢⱼ ≥ 0  ∀ i,j""")

    # ── Résolution ───────────────────────────────────────────────────────
    result2 = solve_tp3_transport()

    with tab2:
        st.markdown(f"#### Statut : {status_badge(result2['status'])}", unsafe_allow_html=True)
        st.markdown("")

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Coût minimal", f"{result2['objective']:,.0f} DA")
        col2.metric("📦 Offre totale", f"{sum(supply)}")
        col3.metric("📍 Destinations", f"{len(dests)}")

        st.markdown("---")
        st.markdown("#### Plan de transport optimal (xᵢⱼ)")

        df_sol = pd.DataFrame(result2['matrix'], index=sources, columns=dests)
        df_sol["Total envoyé"] = df_sol.sum(axis=1)
        df_sol.loc["Total reçu"] = df_sol.sum()
        st.dataframe(df_sol.style.format("{:.1f}"), use_container_width=True)

        st.markdown("#### Coûts par route")
        rows = []
        for i in range(3):
            for j in range(4):
                qty = result2['matrix'][i][j]
                if qty > 1e-6:
                    rows.append({
                        "Route": f"S{i+1} → D{j+1}",
                        "Quantité": f"{qty:.1f}",
                        "Coût unit.": f"{costs[i][j]} DA",
                        "Coût total": f"{costs[i][j] * qty:,.0f} DA",
                    })
        df_routes = pd.DataFrame(rows)
        st.dataframe(df_routes, hide_index=True, use_container_width=True)

    with tab3:
        st.markdown("#### Matrices de transport")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_transport_heatmap(result2), use_container_width=True)
        with col2:
            st.plotly_chart(plot_transport_cost_heatmaps(result2), use_container_width=True)

    with tab4:
        st.markdown("#### Flux de transport (diagramme Sankey)")
        st.plotly_chart(plot_transport_sankey(result2), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_transport_cost_bars(result2, "source"), use_container_width=True)
        with col2:
            st.plotly_chart(plot_transport_cost_bars(result2, "dest"), use_container_width=True)