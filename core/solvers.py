"""
Pure PuLP solver functions — no Streamlit imports here.
Each function returns a dict with status, variables, objective, and sensitivity info.
"""

from pulp import (
    LpProblem, LpVariable, LpMaximize, LpMinimize,
    lpSum, value, PULP_CBC_CMD, LpStatus,
)
import math


def _solve(prob: LpProblem) -> str:
    prob.solve(PULP_CBC_CMD(msg=0))
    return LpStatus[prob.status]


# ──────────────────────────────────────────────
# TP1 — Simple LP  (max 2x1 + 3x2)
# ──────────────────────────────────────────────
def solve_tp1_simple():
    prob = LpProblem("TP1_Simple", LpMaximize)
    x1 = LpVariable("x1", lowBound=0)
    x2 = LpVariable("x2", lowBound=0)

    prob += 2 * x1 + 3 * x2, "Objective"
    prob += x1 + 6 * x2 <= 30, "R1"
    prob += 2 * x1 + 2 * x2 <= 15, "R2"
    prob += 4 * x1 + x2 <= 24, "R3"

    status = _solve(prob)
    return {
        "status": status,
        "x1": value(x1),
        "x2": value(x2),
        "objective": value(prob.objective),
        "constraints": {
            "R1": {"lhs": value(x1 + 6 * x2), "rhs": 30},
            "R2": {"lhs": value(2 * x1 + 2 * x2), "rhs": 15},
            "R3": {"lhs": value(4 * x1 + x2), "rhs": 24},
        },
    }


# ──────────────────────────────────────────────
# TP1 — KS Confection (3 products, 3 machines)
# ──────────────────────────────────────────────
def solve_tp1_ks():
    prob = LpProblem("KS_Confection", LpMaximize)
    laine = LpVariable("Laine", lowBound=0)
    coton = LpVariable("Coton", lowBound=0)
    soie  = LpVariable("Soie",  lowBound=0)

    # Objective: max profit
    prob += 7 * laine + 10 * coton + 12 * soie, "Profit"

    # Machine constraints
    prob += 3 * laine + 2 * coton + 4 * soie <= 120, "Filature"
    prob += 8 * laine + 7 * coton + 4 * soie <= 150, "Tissage"
    prob += 0.7 * laine + 0.6 * coton + 0.3 * soie <= 100, "Ennoblissement"

    # Filature type constraints (NB from TP)
    prob += coton <= 40, "Filature_coton_max"
    prob += laine <= 80, "Filature_laine_max"

    status = _solve(prob)
    return {
        "status": status,
        "Laine": value(laine),
        "Coton": value(coton),
        "Soie":  value(soie),
        "objective": value(prob.objective),
        "constraints": {
            "Filature (≤120h)":       value(3*laine + 2*coton + 4*soie),
            "Tissage (≤150h)":        value(8*laine + 7*coton + 4*soie),
            "Ennoblissement (≤100h)": value(0.7*laine + 0.6*coton + 0.3*soie),
        },
    }


# ──────────────────────────────────────────────
# TP2 — Poterie / Émaux (max 20x + 60y)
# ──────────────────────────────────────────────
def solve_tp2_poterie():
    prob = LpProblem("Poterie_Emaux", LpMaximize)
    x = LpVariable("Poterie", lowBound=0)   # poterie
    y = LpVariable("Emaux",   lowBound=0)   # émaux

    prob += 20 * x + 60 * y, "Benefice"

    # 4y - x <= 160  (charge émaux ≤ poterie + 160)
    prob += 4 * y - x <= 160, "Charge_travail"
    # x - y <= 30  (poterie ≤ émaux + 30)
    prob += x - y <= 30, "Ecart_production"
    # x + y <= 80
    prob += x + y <= 80, "Total_articles"

    status = _solve(prob)
    return {
        "status": status,
        "Poterie": value(x),
        "Emaux":   value(y),
        "objective": value(prob.objective),
        "constraints": {
            "4y - x ≤ 160": value(4*y - x),
            "x - y ≤ 30":   value(x - y),
            "x + y ≤ 80":   value(x + y),
        },
    }


# ──────────────────────────────────────────────
# TP2 — Coussinets / Paliers (min cost)
# ──────────────────────────────────────────────
def solve_tp2_coussinets():
    prob = LpProblem("Coussinets_Paliers", LpMinimize)
    x = LpVariable("Coussinets", lowBound=0)
    y = LpVariable("Paliers",    lowBound=0)

    # Total transport cost = (4x+6y) + (3x+4y) = 7x + 10y
    prob += 7 * x + 10 * y, "Cout_transport"

    prob += x >= 4000, "Min_coussinets"
    prob += y >= 5000, "Min_paliers"
    prob += 2 * x + 3 * y >= 36000, "Min_matiere"
    prob += x + 0.5 * y <= 10000, "Max_MOeuvre"

    status = _solve(prob)
    return {
        "status": status,
        "Coussinets": value(x),
        "Paliers":    value(y),
        "objective":  value(prob.objective),
        "constraints": {
            "Coussinets ≥ 4000":        value(x),
            "Paliers ≥ 5000":           value(y),
            "2x + 3y ≥ 36000 (MP)":    value(2*x + 3*y),
            "x + 0.5y ≤ 10000 (MO)":   value(x + 0.5*y),
        },
    }


# ──────────────────────────────────────────────
# TP3 — CARCO (voitures & camions)
# ──────────────────────────────────────────────
def solve_tp3_carco():
    prob = LpProblem("CARCO", LpMaximize)
    v  = LpVariable("Voitures",  lowBound=0)
    c  = LpVariable("Camions",   lowBound=0)
    m1 = LpVariable("Machines1", lowBound=0)

    # Profit = 300v + 400c - 50*m1 (location coût)
    prob += 300 * v + 400 * c - 50 * m1, "Profit"

    prob += 0.8 * v + 1.0 * c <= m1, "Machine1_usage"
    prob += m1 <= 98,                 "Machine1_max"
    prob += 0.6 * v + 0.7 * c <= 73, "Machine2"
    prob += 2   * v + 3.0 * c <= 260,"Acier"
    prob += v >= 88,                  "Min_voitures"
    prob += c >= 26,                  "Min_camions"

    status = _solve(prob)
    return {
        "status": status,
        "Voitures":  value(v),
        "Camions":   value(c),
        "Machines1": value(m1),
        "objective": value(prob.objective),
        "constraints": {
            "Machine type 1 (≤98)":  value(m1),
            "Machine type 2 (≤73)":  value(0.6*v + 0.7*c),
            "Acier (≤260t)":         value(2*v + 3*c),
            "Voitures (≥88)":        value(v),
            "Camions (≥26)":         value(c),
        },
    }


# ──────────────────────────────────────────────
# TP3 — Transport problem (3x4 matrix)
# ──────────────────────────────────────────────
def solve_tp3_transport():
    """
    3 origins, 4 destinations.
    Supply: [9, 17, 9], Demand: [10, 14, 7, 4]
    """
    costs = [
        [264, 130, 139, 160],
        [279, 244, 146, 307],
        [200, 166,  66, 278],
    ]
    supply  = [9, 17, 9]
    demand  = [10, 14, 7, 4]
    origins = ["O1", "O2", "O3"]
    dests   = ["D1", "D2", "D3", "D4"]

    prob = LpProblem("Transport", LpMinimize)
    x = {
        (i, j): LpVariable(f"x{i+1}{j+1}", lowBound=0)
        for i in range(3) for j in range(4)
    }

    prob += lpSum(costs[i][j] * x[i, j] for i in range(3) for j in range(4))

    for i in range(3):
        prob += lpSum(x[i, j] for j in range(4)) == supply[i], f"Supply_{i}"
    for j in range(4):
        prob += lpSum(x[i, j] for i in range(3)) == demand[j], f"Demand_{j}"

    status = _solve(prob)

    matrix = [[value(x[i, j]) for j in range(4)] for i in range(3)]
    return {
        "status":   status,
        "matrix":   matrix,
        "origins":  origins,
        "dests":    dests,
        "supply":   supply,
        "demand":   demand,
        "costs":    costs,
        "objective": value(prob.objective),
    }