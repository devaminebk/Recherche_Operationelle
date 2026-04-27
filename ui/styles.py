"""
Global CSS + Streamlit style helpers.
"""
import streamlit as st

THEME_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;800&display=swap');

  :root {
    --bg:      #0D1117;
    --surface: #161B22;
    --border:  #30363D;
    --a1:      #58A6FF;
    --a2:      #3FB950;
    --a3:      #F78166;
    --a4:      #D2A8FF;
    --a5:      #FFA657;
    --text:    #E6EDF3;
    --muted:   #8B949E;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace;
  }

  [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }

  h1, h2, h3 { font-family: 'Syne', sans-serif; letter-spacing: -0.02em; }

  /* metric cards */
  [data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px !important;
  }
  [data-testid="metric-container"] label { color: var(--muted) !important; font-size: 0.78rem; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--a1) !important; font-size: 1.6rem; font-weight: 700; }

  /* buttons */
  .stButton > button {
    background: var(--a1) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: opacity .2s;
  }
  .stButton > button:hover { opacity: .85; }

  /* code block */
  .lp-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--a1);
    border-radius: 6px;
    padding: 18px 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre;
    overflow-x: auto;
  }

  /* result card */
  .result-card {
    background: linear-gradient(135deg, var(--surface) 0%, #1C2333 100%);
    border: 1px solid var(--a2);
    border-radius: 10px;
    padding: 20px 24px;
    margin: 12px 0;
  }
  .result-card .label { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: .08em; }
  .result-card .value { color: var(--a2); font-size: 1.9rem; font-weight: 700; }

  /* status badge */
  .badge-ok  { display:inline-block; background:rgba(63,185,80,.18); color:var(--a2); border:1px solid var(--a2); border-radius:20px; padding:3px 14px; font-size:.8rem; font-weight:600; }
  .badge-err { display:inline-block; background:rgba(247,129,102,.18); color:var(--a3); border:1px solid var(--a3); border-radius:20px; padding:3px 14px; font-size:.8rem; }

  /* section header */
  .section-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: 6px 18px;
    font-size: .78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 8px;
  }

  /* tabs */
  [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 8px; gap: 4px; }
  [data-baseweb="tab"] { color: var(--muted) !important; }
  [aria-selected="true"] { color: var(--a1) !important; }

  /* dataframe */
  [data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 8px; }

  /* sidebar nav links */
  [data-testid="stSidebarNav"] a { color: var(--text) !important; }
  [data-testid="stSidebarNav"] a:hover { color: var(--a1) !important; }

  /* expander */
  [data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 8px !important; }

  /* page title bar */
  .page-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 32px;
  }
  .page-header h1 { margin: 0; font-size: 2.2rem; }
  .page-header .subtitle { color: var(--muted); font-size: .88rem; margin-top: 6px; }

  div[data-testid="column"] { gap: 0; }

  hr { border-color: var(--border) !important; }
</style>
"""


def inject_styles():
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(
        f"""<div class="page-header">
          <h1>{icon} {title}</h1>
          {'<p class="subtitle">' + subtitle + '</p>' if subtitle else ''}
        </div>""",
        unsafe_allow_html=True,
    )


def lp_block(text: str):
    st.markdown(f'<div class="lp-block">{text}</div>', unsafe_allow_html=True)


def result_card(label: str, value: str, col=None):
    html = f'<div class="result-card"><div class="label">{label}</div><div class="value">{value}</div></div>'
    if col:
        col.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)


def status_badge(status: str):
    ok = status == "Optimal"
    cls = "badge-ok" if ok else "badge-err"
    st.markdown(f'<span class="{cls}">{"✓ " if ok else "✗ "}{status}</span>', unsafe_allow_html=True)


def section_pill(text: str, dot_color: str = "#58A6FF"):
    st.markdown(
        f'<div class="section-pill"><span style="width:7px;height:7px;border-radius:50%;background:{dot_color};display:inline-block"></span>{text}</div>',
        unsafe_allow_html=True,
    )