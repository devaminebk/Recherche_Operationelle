"""
core package — expose all solver functions at the package level.
"""
from .solvers import (
    solve_tp1_simple,
    solve_tp1_ks,
    solve_tp2_poterie,
    solve_tp2_coussinets,
    solve_tp3_carco,
    solve_tp3_transport,
)

__all__ = [
    "solve_tp1_simple",
    "solve_tp1_ks",
    "solve_tp2_poterie",
    "solve_tp2_coussinets",
    "solve_tp3_carco",
    "solve_tp3_transport",
]
