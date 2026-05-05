# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app serves on http://localhost:8501 by default.

## Architecture

This is a French-language educational Streamlit app for Operations Research (Recherche Opérationnelle) practical work (TPs). It teaches Linear Programming through interactive visualization.

**Layer separation is strict:**

- `core/solvers.py` — Pure Python solver functions using PuLP. No Streamlit imports. Each function takes parameters and returns a dict with `status`, variable values, objective, and constraint data.
- `plots/charts.py` — Stateless Plotly visualization functions. Take solver result dicts, return Plotly figures. No Streamlit imports.
- `ui/styles.py` — CSS injection and Streamlit helper functions for consistent UI components.
- `pages/tp1.py`, `pages/tp2.py`, `pages/tp3.py` — Page controllers that wire together solvers and charts using Streamlit widgets. They cache results in `st.session_state` and compute solutions only on button click.
- `app.py` — Entry point: injects styles and renders the home/navigation page.

**Data flow:** User triggers solve → page calls solver → solver returns dict → page passes dict to chart functions → Streamlit renders figures.

## Key conventions

- Solver results are cached in `st.session_state` using problem-specific keys to avoid recomputation on widget interaction.
- All solver functions are stateless and return dicts; never modify global state.
- PuLP uses the CBC solver backend (bundled with PuLP).
- The UI language is French throughout (variable names in Python may be French or abbreviated).
