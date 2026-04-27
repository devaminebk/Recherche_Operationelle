"""
All Plotly figures — pure functions, no Streamlit.
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Palette ────────────────────────────────────────────────────────────────
C = {
    "bg":      "#0D1117",
    "surface": "#161B22",
    "border":  "#30363D",
    "accent1": "#58A6FF",
    "accent2": "#3FB950",
    "accent3": "#F78166",
    "accent4": "#D2A8FF",
    "accent5": "#FFA657",
    "text":    "#E6EDF3",
    "muted":   "#8B949E",
}

_LAYOUT = dict(
    paper_bgcolor=C["bg"],
    plot_bgcolor=C["surface"],
    font=dict(family="JetBrains Mono, monospace", color=C["text"], size=12),
    margin=dict(l=50, r=30, t=60, b=50),
    xaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"]),
    yaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"]),
)


def _fig(**kw):
    fig = go.Figure()
    fig.update_layout(**_LAYOUT, **kw)
    return fig


# ──────────────────────────────────────────────
# Feasible region for 2-variable LP
# ──────────────────────────────────────────────
def plot_feasible_region_simple(result):
    """Feasible region for TP1 simple LP."""
    fig = _fig(title="Région réalisable — max 2x₁ + 3x₂")

    xs = np.linspace(0, 20, 400)

    # Constraints
    constraints = {
        "R1: x₁ + 6x₂ ≤ 30":  (30 - xs) / 6,
        "R2: 2x₁ + 2x₂ ≤ 15": (15 - 2*xs) / 2,
        "R3: 4x₁ + x₂ ≤ 24":  24 - 4*xs,
    }
    colors = [C["accent1"], C["accent2"], C["accent3"]]

    for (label, ys), col in zip(constraints.items(), colors):
        fig.add_trace(go.Scatter(
            x=xs, y=np.clip(ys, 0, 20),
            mode="lines", name=label,
            line=dict(color=col, width=2),
        ))

    # Shade feasible region
    y_feas = np.minimum.reduce([
        np.clip((30 - xs) / 6, 0, 20),
        np.clip((15 - 2*xs) / 2, 0, 20),
        np.clip(24 - 4*xs, 0, 20),
    ])
    fig.add_trace(go.Scatter(
        x=np.concatenate([xs, xs[::-1]]),
        y=np.concatenate([y_feas, np.zeros(len(xs))]),
        fill="toself", fillcolor="rgba(88,166,255,0.10)",
        line=dict(width=0), name="Zone réalisable", showlegend=True,
    ))

    # Optimal objective line
    z = result["objective"]
    obj_x = np.array([0, z / 2])
    obj_y = np.array([z / 3, 0])
    fig.add_trace(go.Scatter(
        x=obj_x, y=obj_y,
        mode="lines", name=f"Objectif Z={z:.2f}",
        line=dict(color=C["accent5"], width=2, dash="dot"),
    ))

    # Optimal point
    fig.add_trace(go.Scatter(
        x=[result["x1"]], y=[result["x2"]],
        mode="markers+text",
        marker=dict(color=C["accent5"], size=14, symbol="star"),
        text=[f"  ({result['x1']:.2f}, {result['x2']:.2f})"],
        textfont=dict(color=C["accent5"]),
        name="Optimum",
    ))

    fig.update_layout(
        xaxis=dict(**_LAYOUT["xaxis"], title="x₁", range=[0, 16]),
        yaxis=dict(**_LAYOUT["yaxis"], title="x₂", range=[0, 10]),
        legend=dict(bgcolor=C["surface"], bordercolor=C["border"], borderwidth=1),
    )
    return fig


def plot_feasible_region_poterie(result):
    """Feasible region for TP2 poterie/émaux."""
    fig = _fig(title="Région réalisable — Poterie & Émaux")

    xs = np.linspace(0, 120, 600)

    lines = {
        "4y - x ≤ 160  →  y = (x+160)/4": (xs + 160) / 4,
        "x - y ≤ 30    →  y = x - 30":     xs - 30,
        "x + y ≤ 80    →  y = 80 - x":     80 - xs,
    }
    colors = [C["accent1"], C["accent2"], C["accent3"]]
    for (label, ys), col in zip(lines.items(), colors):
        fig.add_trace(go.Scatter(
            x=xs, y=np.clip(ys, 0, 100),
            mode="lines", name=label,
            line=dict(color=col, width=2),
        ))

    x_opt, y_opt = result["Poterie"], result["Emaux"]
    fig.add_trace(go.Scatter(
        x=[x_opt], y=[y_opt],
        mode="markers+text",
        marker=dict(color=C["accent5"], size=14, symbol="star"),
        text=[f"  ({x_opt:.1f}, {y_opt:.1f})"],
        textfont=dict(color=C["accent5"]),
        name=f"Optimum Z={result['objective']:.0f}",
    ))
    fig.update_layout(
        xaxis=dict(**_LAYOUT["xaxis"], title="Poterie (x)", range=[0, 100]),
        yaxis=dict(**_LAYOUT["yaxis"], title="Émaux (y)", range=[0, 80]),
    )
    return fig


# ──────────────────────────────────────────────
# Bar chart for multi-product LP results
# ──────────────────────────────────────────────
def plot_production_bars(variables: dict, title: str, unit="unités"):
    """Generic bar chart for production quantities."""
    names  = list(variables.keys())
    values = [max(0, v or 0) for v in variables.values()]
    colors = [C["accent1"], C["accent2"], C["accent3"], C["accent4"], C["accent5"]]

    fig = _fig(title=title)
    fig.add_trace(go.Bar(
        x=names, y=values,
        marker_color=colors[:len(names)],
        text=[f"{v:.2f}" for v in values],
        textposition="outside",
        textfont=dict(color=C["text"]),
    ))
    fig.update_layout(
        yaxis=dict(**_LAYOUT["yaxis"], title=unit),
        xaxis=dict(**_LAYOUT["xaxis"]),
        showlegend=False,
        bargap=0.35,
    )
    return fig


# ──────────────────────────────────────────────
# Constraint utilisation gauge bars
# ──────────────────────────────────────────────
def plot_constraint_usage(constraints: dict, title="Utilisation des contraintes"):
    """Horizontal bar chart showing % usage of each constraint."""
    labels, pcts, absolutes = [], [], []
    for name, data in constraints.items():
        if isinstance(data, dict):
            lhs, rhs = data["lhs"], data["rhs"]
        else:
            # data is just the lhs value — skip if no rhs context
            continue
        pct = min((lhs / rhs * 100) if rhs else 0, 100)
        labels.append(name)
        pcts.append(pct)
        absolutes.append(f"{lhs:.2f} / {rhs}")

    if not labels:
        return None

    colors = [C["accent2"] if p < 90 else C["accent3"] for p in pcts]

    fig = _fig(title=title)
    fig.add_trace(go.Bar(
        x=pcts, y=labels,
        orientation="h",
        marker_color=colors,
        text=[f"{p:.1f}%" for p in pcts],
        textposition="outside",
        textfont=dict(color=C["text"]),
        customdata=absolutes,
        hovertemplate="%{y}: %{customdata}<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(**_LAYOUT["xaxis"], title="Utilisation (%)", range=[0, 115]),
        yaxis=dict(**_LAYOUT["yaxis"]),
        showlegend=False,
        height=300,
    )
    return fig


# ──────────────────────────────────────────────
# Transport heatmap
# ──────────────────────────────────────────────
def plot_transport_heatmap(result):
    matrix = result["matrix"]
    costs  = result["costs"]
    origins = result["origins"]
    dests   = result["dests"]

    text_vals = [
        [f"<b>{matrix[i][j]:.0f}</b><br><sub>coût:{costs[i][j]}</sub>"
         for j in range(4)]
        for i in range(3)
    ]

    fig = go.Figure(go.Heatmap(
        z=matrix,
        x=dests, y=origins,
        text=text_vals,
        texttemplate="%{text}",
        colorscale=[
            [0,   C["surface"]],
            [0.01, "#1B3A5C"],
            [1,   C["accent1"]],
        ],
        showscale=True,
        colorbar=dict(title="Qté", tickfont=dict(color=C["text"])),
    ))
    fig.update_layout(
        paper_bgcolor=C["bg"],
        plot_bgcolor=C["surface"],
        font=dict(family="JetBrains Mono, monospace", color=C["text"], size=12),
        margin=dict(l=50, r=30, t=60, b=50),
        title="Plan de transport optimal",
        xaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"], title="Destinations"),
        yaxis=dict(gridcolor=C["border"], zerolinecolor=C["border"], title="Origines"),
        height=320,
    )
    return fig


def plot_transport_flow(result):
    """Sankey diagram for transport flows."""
    matrix  = result["matrix"]
    origins = result["origins"]
    dests   = result["dests"]
    supply  = result["supply"]
    demand  = result["demand"]

    node_labels = origins + dests
    src, tgt, val, lbl = [], [], [], []

    for i in range(3):
        for j in range(4):
            q = matrix[i][j]
            if q and q > 0:
                src.append(i)
                tgt.append(3 + j)
                val.append(q)
                lbl.append(f"{q:.0f} u.")

    palette = [C["accent1"], C["accent2"], C["accent3"], C["accent4"],
               C["accent5"], "#79C0FF", "#56D364", "#FF7B72"]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20, thickness=20,
            label=node_labels,
            color=palette[:len(node_labels)],
            line=dict(color=C["border"], width=0.5),
        ),
        link=dict(
            source=src, target=tgt, value=val,
            label=lbl,
            color="rgba(88,166,255,0.25)",
        ),
    ))
    fig.update_layout(
        **_LAYOUT,
        title="Flux de transport (Sankey)",
        height=380,
    )
    return fig


# ──────────────────────────────────────────────
# KS Confection radar
# ──────────────────────────────────────────────
def plot_ks_radar(result):
    categories = list(result["constraints"].keys()) + [list(result["constraints"].keys())[0]]
    capacities = [120, 150, 100, 120]  # close the loop
    used = [result["constraints"][k] for k in list(result["constraints"].keys())]
    used_closed = used + [used[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=capacities,
        theta=categories,
        fill="toself",
        name="Capacité",
        fillcolor="rgba(88,166,255,0.12)",
        line=dict(color=C["accent1"], width=2),
    ))
    fig.add_trace(go.Scatterpolar(
        r=used_closed,
        theta=categories,
        fill="toself",
        name="Utilisé",
        fillcolor="rgba(63,185,80,0.25)",
        line=dict(color=C["accent2"], width=2, dash="dash"),
    ))
    fig.update_layout(
        **_LAYOUT,
        polar=dict(
            bgcolor=C["surface"],
            radialaxis=dict(visible=True, gridcolor=C["border"], color=C["muted"]),
            angularaxis=dict(gridcolor=C["border"], color=C["text"]),
        ),
        showlegend=True,
        title="Utilisation des machines (KS Confection)",
        height=400,
    )
    return fig


# ──────────────────────────────────────────────
# CARCO profit pie chart
# ──────────────────────────────────────────────
def plot_carco_profit_pie(result):
    """Pie chart for CARCO profit decomposition."""
    rev_v = 300 * result["Voitures"]
    rev_c = 400 * result["Camions"]
    cost_m = 50 * result["Machines1"]

    fig = go.Figure(go.Pie(
        labels=["Revenu Voitures", "Revenu Camions", "Coût Machines"],
        values=[rev_v, rev_c, cost_m],
        hole=0.45,
        marker=dict(colors=[C["accent1"], C["accent2"], C["accent3"]]),
        textfont=dict(family="IBM Plex Mono"),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Répartition du compte de résultat", font=dict(color=C["text"])),
        showlegend=True,
        legend=dict(bgcolor=C["surface"], bordercolor=C["border"]),
    )
    return fig


# ──────────────────────────────────────────────
# CARCO feasible region
# ──────────────────────────────────────────────
def plot_carco_feasible_region(result):
    """Feasible region for CARCO (Voitures vs Camions)."""
    fig = _fig(title="Région réalisable — CARCO (Voitures vs Camions)")

    v_range = np.linspace(80, 130, 400)

    # Constraints
    def c_acier_c(v): return (260 - 2*v) / 3
    def c_m2_c(v):    return (73 - 0.6*v) / 0.7

    fig.add_trace(go.Scatter(x=v_range, y=c_acier_c(v_range),
        mode='lines', name='Acier ≤ 260',
        line=dict(color=C["accent1"], width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=v_range, y=c_m2_c(v_range),
        mode='lines', name='Machine type 2 ≤ 73',
        line=dict(color=C["accent2"], width=2, dash='solid')))

    # Min lines
    fig.add_vline(x=88, line=dict(color=C["accent3"], width=1.5, dash='dash'),
                  annotation_text="Voitures ≥ 88", annotation_font_color=C["accent3"])
    fig.add_hline(y=26, line=dict(color=C["accent4"], width=1.5, dash='dash'),
                  annotation_text="Camions ≥ 26", annotation_font_color=C["accent4"])

    # Solution optimale
    fig.add_trace(go.Scatter(x=[result["Voitures"]], y=[result["Camions"]],
        mode='markers', name='Solution optimale',
        marker=dict(size=14, color=C["accent5"], symbol='star')))

    fig.update_layout(
        xaxis=dict(**_LAYOUT["xaxis"], title="Voitures/jour"),
        yaxis=dict(**_LAYOUT["yaxis"], title="Camions/jour"),
        legend=dict(bgcolor=C["surface"], bordercolor=C["border"]),
        yaxis_range=[0, 100],
        xaxis_range=[80, 130],
    )
    return fig


# ──────────────────────────────────────────────
# Transport cost heatmaps
# ──────────────────────────────────────────────
def plot_transport_cost_heatmaps(result):
    """Heatmap for transport cost matrix."""
    costs = result["costs"]
    origins = result["origins"]
    dests = result["dests"]

    fig = go.Figure(go.Heatmap(
        z=costs,
        x=dests, y=origins,
        colorscale=[[0, "#1a3a28"], [0.5, "#3a2e0d"], [1, "#5a1a1a"]],
        text=costs,
        texttemplate="%{text} DA",
        textfont=dict(family="IBM Plex Mono", size=13),
        showscale=True,
        hovertemplate="<b>%{y} → %{x}</b><br>Coût: %{z} DA<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT,
        title="Matrice des coûts de transport",
        height=320,
    )
    return fig


# ──────────────────────────────────────────────
# Transport Sankey
# ──────────────────────────────────────────────
def plot_transport_sankey(result):
    """Sankey diagram for transport flows."""
    matrix = result["matrix"]
    origins = result["origins"]
    dests = result["dests"]
    costs = result["costs"]

    labels = origins + dests
    src, tgt, val, lbl = [], [], [], []

    for i in range(3):
        for j in range(4):
            q = matrix[i][j]
            if q > 1e-6:
                src.append(i)
                tgt.append(3 + j)
                val.append(q)
                lbl.append(f"{costs[i][j]} DA/u")

    palette = [C["accent1"], C["accent2"], C["accent3"], C["accent4"],
               C["accent5"], "#79C0FF", "#56D364", "#FF7B72"]

    fig = go.Figure(go.Sankey(
        node=dict(
            label=labels,
            color=palette[:len(labels)],
            pad=20, thickness=25,
            line=dict(color=C["border"], width=0.5),
        ),
        link=dict(
            source=src, target=tgt, value=val,
            label=lbl,
            color="rgba(88,166,255,0.3)",
        ),
    ))
    fig.update_layout(
        **_LAYOUT,
        title="Flux de transport (Sankey)",
        height=380,
    )
    return fig


# ──────────────────────────────────────────────
# Transport cost bars
# ──────────────────────────────────────────────
def plot_transport_cost_bars(result, mode="source"):
    """Bar chart for transport costs by source or destination."""
    matrix = result["matrix"]
    costs = result["costs"]
    origins = result["origins"]
    dests = result["dests"]

    if mode == "source":
        contrib = [float(np.sum(np.array(costs[i]) * np.array(matrix[i]))) for i in range(3)]
        labels = origins
        title = "Coût par source"
    else:
        contrib = [float(np.sum(np.array(costs)[:, j] * np.array(matrix)[:, j])) for j in range(4)]
        labels = dests
        title = "Coût par destination"

    colors = [C["accent1"], C["accent2"], C["accent3"], C["accent4"]]

    fig = _fig(title=title)
    fig.add_trace(go.Bar(
        x=labels, y=contrib,
        marker_color=colors[:len(labels)],
        text=[f"{v:,.0f} DA" for v in contrib],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono"),
    ))
    fig.update_layout(
        yaxis=dict(**_LAYOUT["yaxis"], title="Coût (DA)"),
        xaxis=dict(**_LAYOUT["xaxis"]),
        showlegend=False,
        bargap=0.35,
    )
    return fig