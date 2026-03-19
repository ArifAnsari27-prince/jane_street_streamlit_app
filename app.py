
import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Jane Street India — Forensic Microstructure Lab",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

@st.cache_data
def load_data():
    imp = pd.read_csv(DATA / "impugned_days.csv")
    ent = pd.read_csv(DATA / "entities_profit_loss.csv")
    timeline = pd.read_csv(DATA / "case_timeline.csv")
    jan17 = pd.read_csv(DATA / "jan17_2024_sample_day.csv")
    metrics = pd.read_csv(DATA / "market_structure_metrics.csv")
    imp2 = pd.read_csv(DATA / "impugned_days_illegal_gains.csv") if (DATA / "impugned_days_illegal_gains.csv").exists() else None
    prof2 = pd.read_csv(DATA / "profit_summary_by_entity.csv") if (DATA / "profit_summary_by_entity.csv").exists() else None
    return imp, ent, timeline, jan17, metrics, imp2, prof2

imp, ent, timeline, jan17, metrics, imp2, prof2 = load_data()

# --- Theme ---
st.markdown(
    """
    <style>
        :root {
            --bg: #0f1117;
            --panel: #151924;
            --panel-2: #1a2030;
            --text: #ecf0f8;
            --muted: #8d96aa;
            --line: rgba(255,255,255,0.08);
            --accent: #e8590c;
            --accent-2: #4dabf7;
            --accent-3: #51cf66;
            --warn: #ffd43b;
            --danger: #ff6b6b;
        }
        .stApp {
            background: radial-gradient(1200px 600px at 10% -10%, rgba(232,89,12,0.10), transparent 40%),
                        radial-gradient(1200px 600px at 100% 0%, rgba(77,171,247,0.10), transparent 40%),
                        var(--bg);
            color: var(--text);
        }
        div.block-container {max-width: 1320px; padding-top: 1.2rem; padding-bottom: 2rem;}
        #MainMenu, footer, header {visibility: hidden;}
        .hero {
            padding: 1.2rem 1.25rem 1rem 1.25rem;
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.00));
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 20px 40px rgba(0,0,0,.25);
            margin-bottom: 1rem;
        }
        .eyebrow {font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); font-weight: 700;}
        .hero h1 {margin: 0.2rem 0 0.4rem 0; font-size: 2.15rem; line-height: 1.1;}
        .hero p {margin: 0; color: var(--muted); max-width: 980px;}
        .stat-card, .panel-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 16px 32px rgba(0,0,0,.18);
            height: 100%;
        }
        .stat-label {font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.12em;}
        .stat-value {font-size: 1.9rem; font-weight: 800; color: var(--text); margin-top: 0.15rem;}
        .stat-sub {font-size: 12px; color: var(--accent); margin-top: 0.1rem;}
        .section-title {font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: .65rem;}
        .insight-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--line);
            border-left: 3px solid var(--accent);
            border-radius: 14px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.75rem;
        }
        .insight-card.blue {border-left-color: var(--accent-2);} 
        .insight-card.green {border-left-color: var(--accent-3);} 
        .insight-card.yellow {border-left-color: var(--warn);} 
        .insight-card h4 {margin:0 0 .25rem 0; font-size:1rem;}
        .insight-card p {margin:0; color:var(--muted); font-size:.92rem; line-height:1.55;}
        .badge {
            display:inline-block; padding: 0.18rem 0.55rem; border-radius: 999px; font-size: .76rem; 
            border: 1px solid var(--line); background: rgba(255,255,255,0.03); color: var(--text);
        }
        .micro-note {color: var(--muted); font-size: .9rem; line-height: 1.6;}
        .timeline-item {padding: .45rem 0 .45rem 1rem; border-left: 2px solid var(--line); margin-left: .4rem;}
        .timeline-date {font-size: .78rem; color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace;}
        .timeline-text {font-size: .95rem; color: var(--text);}
        .footline {margin-top:1rem; color: var(--muted); font-size: .83rem;}
        div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p {font-size: 0.96rem;}
        div[data-testid="stTabs"] button {border-radius: 12px 12px 0 0;}
        div[data-testid="stMetricValue"] {color: var(--text);}
        div[data-testid="stMetricLabel"] {color: var(--muted);}
        .smallcaps {text-transform: uppercase; letter-spacing: .1em; font-size: .8rem; color: var(--muted);} 
    </style>
    """,
    unsafe_allow_html=True,
)

# --- helpers ---
def money_fmt(x):
    return f"₹{x:,.2f} Cr"

def style_header():
    st.markdown(
        """
        <div class='hero'>
          <div class='eyebrow'>Forensic microstructure reconstruction</div>
          <h1>Jane Street India — Streamlit Research Dashboard</h1>
          <p>
            A case-driven analytical surface for trade-pattern reconstruction, option-cash interaction analysis, footprint scoring,
            and market microstructure research in India-like environments, with extension paths for South Korea block-trade regimes
            and crypto venues.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_cards():
    total_gains = metrics.loc[metrics.metric == 'total_illegal_gains_all_days', 'value'].iloc[0]
    top_day = imp.sort_values('profit_crore', ascending=False).iloc[0]
    exam_days = (imp['examination_period'].str.lower() == 'yes').sum()
    post_days = len(imp) - exam_days
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, 'Alleged gains', money_fmt(total_gains), '~$570M equivalent scale'),
        (c2, 'Impugned days', f"{len(imp)}", f"{exam_days} exam-period + {post_days} post-caution"),
        (c3, 'Entities / PANs', f"{ent[ent.entity_id != 'TOTAL'].shape[0]}", '2 FPI + 2 domestic vehicles'),
        (c4, 'Peak day', money_fmt(top_day['profit_crore']), str(top_day['date'])),
    ]
    for col, label, value, sub in cards:
        with col:
            st.markdown(
                f"<div class='stat-card'><div class='stat-label'>{label}</div><div class='stat-value'>{value}</div><div class='stat-sub'>{sub}</div></div>",
                unsafe_allow_html=True,
            )

def render_landing_page():
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='section-title'>Start here</div>
        <div class='insight-card'>
          <h4>What this app does</h4>
          <p>
            This platform reconstructs the Jane Street India case as a market microstructure research surface.
            It combines case chronology, impugned-day analysis, a January 17 session reconstruction,
            entity/PAN-level economics, a mechanistic simulator, a footprint scoring framework,
            and a research extension layer for comparable patterns in other markets.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.2, 1], gap="large")

    with c1:
        st.markdown(
            """
            <div class='insight-card blue'>
              <h4>How to navigate</h4>
              <p>
                Use the top tab bar to move through the app from left to right:
                <br><br>
                <b>Overview</b> — case structure, timeline, and pattern counts
                <br><b>Impugned Days</b> — day-level event table and profit visualization
                <br><b>Jan 17 Reconstruction</b> — reconstructed intraday sequence and event log
                <br><b>Entities & Economics</b> — entity/PAN structure and segment-level contribution
                <br><b>Mechanistic Simulator</b> — stylized delta/gamma/impact model
                <br><b>Footprint Scoring</b> — surveillance-style attribution engine
                <br><b>Microstructure & Frontier Research</b> — why this matters beyond India
                <br><b>Data Room</b> — inspect and download working datasets
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='insight-card green'>
              <h4>How to use the workflow</h4>
              <p>
                A strong reading path is:
                <br>1. Start with <b>Overview</b> to understand the case architecture
                <br>2. Move to <b>Impugned Days</b> to identify recurring patterns
                <br>3. Use <b>Jan 17 Reconstruction</b> to study a concrete session
                <br>4. Review <b>Entities & Economics</b> for organizational and segment context
                <br>5. Use the <b>Mechanistic Simulator</b> to stress the two-leg mechanism
                <br>6. Use <b>Footprint Scoring</b> to evaluate pattern similarity
                <br>7. Finish with <b>Microstructure & Frontier Research</b> for transferability
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class='insight-card yellow'>
              <h4>What is inside the app</h4>
              <p>
                <b>Case reconstruction:</b> timeline, impugned days, and representative-session structure
                <br><b>Economic decomposition:</b> segment-level profit/loss and entity mapping
                <br><b>Mechanism modeling:</b> a stylized simulator for index move, convexity, and impact
                <br><b>Attribution logic:</b> a footprint score built from concentration, timing, and reversal features
                <br><b>Microstructure research:</b> tools for understanding how asymmetric market design can matter
                <br><b>Transferability:</b> research framing for similar patterns in South Korea block-trade settings and crypto
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='insight-card'>
              <h4>Why this matters</h4>
              <p>
                The app is designed to help you study how pressure in a smaller underlying market can interact
                with a much larger derivatives complex, how settlement windows matter, and how repeated execution
                fingerprints can be translated into reusable market-structure research.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class='panel-card' style="margin-top: 1rem;">
            <div class='section-title'>Section map</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    map_cols = st.columns(4)
    section_map = [
        ("Overview", "Case chronology, structure, pattern counts, and high-level asymmetries."),
        ("Impugned Days", "Profit-ranked and strategy-tagged event surface across the identified days."),
        ("Jan 17 Reconstruction", "Representative session reconstruction showing phase transitions."),
        ("Entities & Economics", "PAN-linked entity view and contribution by market segment."),
        ("Mechanistic Simulator", "Stylized educational model for delta/gamma/impact interaction."),
        ("Footprint Scoring", "Pattern attribution layer using concentration and timing-based features."),
        ("Microstructure & Frontier Research", "Transferability to India-like markets, South Korea, and crypto."),
        ("Data Room", "Raw and curated datasets for review, export, and extension."),
    ]

    for i, (title, text) in enumerate(section_map):
        with map_cols[i % 4]:
            st.markdown(
                f"""
                <div class='insight-card' style="min-height: 180px;">
                  <h4>{title}</h4>
                  <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class='insight-card blue'>
          <h4>Navigation note</h4>
          <p>
            This landing page is the first tab in the interface. After reviewing it, navigate using the tab bar above.
            The app is structured so that the research story moves from context → evidence → mechanism → scoring → broader market interpretation.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def make_timeline_chart(df):
    t = df.copy()
    t['event_date'] = pd.to_datetime(t['event_date'])
    type_color = {
        'regulatory': '#e8590c', 'legal': '#4dabf7', 'incorporation': '#51cf66',
        'first_impugned_day': '#51cf66', 'peak_profit_day': '#51cf66', 'us_lawsuit_filed': '#4dabf7',
        'media_reports': '#4dabf7', 'nse_examination': '#e8590c', 'nse_report': '#e8590c',
        'caution_letter': '#e8590c', 'interim_order': '#e8590c', 'sat_hearing': '#4dabf7',
        'examination_start': '#e8590c', 'examination_end': '#e8590c', 'post_exam_day1': '#51cf66',
        'post_exam_day2': '#51cf66', 'post_exam_day3': '#51cf66', 'us_settlement': '#4dabf7', 'last_exam_impugned': '#51cf66',
        'escrow_compliance': '#e8590c', 'appeal_data_dispute': '#4dabf7',
    }
    t['y'] = 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t['event_date'], y=t['y'], mode='markers+text',
        marker=dict(size=14, color=[type_color.get(x, '#9aa5b1') for x in t['event_type']], line=dict(width=2, color='#0f1117')),
        text=t['description'], textposition='top center',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{text}<extra></extra>',
        textfont=dict(color='#d9e1ef', size=11),
    ))
    fig.update_layout(
        height=240, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickfont=dict(color='#8d96aa')),
        yaxis=dict(visible=False, range=[0.8, 1.22]),
    )
    return fig


def make_impugned_chart(df):
    tmp = df.copy()
    tmp['date'] = pd.to_datetime(tmp['date'])
    tmp['strategy_short'] = tmp['strategy'].replace({
        'Intra-day Index Manipulation': 'Intraday',
        'Extended Marking the Close': 'Extended Close',
    })
    colors = {'Intraday': '#e8590c', 'Extended Close': '#4dabf7'}
    fig = px.bar(
        tmp,
        x='date', y='profit_crore', color='strategy_short',
        color_discrete_map=colors,
        custom_data=['index', 'strategy_short'],
    )
    fig.update_traces(
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Profit: ₹%{y:.2f} Cr<br>Index: %{customdata[0]}<br>Strategy: %{customdata[1]}<extra></extra>'
    )
    fig.update_layout(
        height=340, margin=dict(l=8, r=8, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='', xaxis_title='', yaxis_title='Profit (₹ Cr)',
        font=dict(color='#d9e1ef'),
        yaxis=dict(gridcolor='rgba(255,255,255,.08)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0)'),
    )
    return fig


def jan17_path():
    return pd.DataFrame([
        ['09:15', 46072, 'Open'], ['09:16', 46814, 'Patch I'], ['09:17', 46879, 'Patch I'],
        ['09:18', 47015, 'Patch I'], ['09:19', 47060, 'Patch I'], ['09:20', 47107, 'Patch I'],
        ['09:21', 47144, 'Patch I'], ['09:22', 47177, 'Patch I'], ['10:00', 47100, 'Transition'],
        ['11:00', 47050, 'Transition'], ['11:45', 46950, 'Patch II'], ['12:30', 46700, 'Patch II'],
        ['13:30', 46400, 'Patch II'], ['14:30', 46200, 'Patch II'], ['15:29', 46000, 'Close'],
    ], columns=['time', 'index_level', 'phase'])


def make_jan17_chart(df):
    order = {t: i for i, t in enumerate(df['time'])}
    df = df.copy()
    df['order'] = df['time'].map(order)
    colors = {'Open': '#6c757d', 'Patch I': '#e8590c', 'Transition': '#ffd43b', 'Patch II': '#4dabf7', 'Close': '#51cf66'}
    fig = go.Figure()
    fig.add_vrect(x0=0.5, x1=7.5, fillcolor='rgba(232,89,12,0.12)', line_width=0)
    fig.add_vrect(x0=10.2, x1=14.4, fillcolor='rgba(77,171,247,0.12)', line_width=0)
    fig.add_trace(go.Scatter(
        x=df['time'], y=df['index_level'], mode='lines+markers',
        line=dict(color='#e9edf5', width=3),
        marker=dict(size=9, color=[colors[p] for p in df['phase']], line=dict(width=2, color='#0f1117')),
        hovertemplate='Time: %{x}<br>Index: %{y:,.0f}<br>Phase: %{marker.color}<extra></extra>'
    ))
    fig.add_annotation(x='09:19', y=47210, text='Patch I: support / lift', showarrow=False, font=dict(color='#e8590c', size=11))
    fig.add_annotation(x='13:30', y=46620, text='Patch II: unwind / pressure', showarrow=False, font=dict(color='#4dabf7', size=11))
    fig.update_layout(
        height=360, margin=dict(l=8, r=8, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='', yaxis_title='BANKNIFTY level', font=dict(color='#d9e1ef'),
        yaxis=dict(gridcolor='rgba(255,255,255,.08)'),
    )
    return fig


def segment_profit_chart(df):
    total = df[df['entity_id'] == 'TOTAL'].iloc[0]
    seg = pd.DataFrame({
        'segment': ['Index options', 'Stock options', 'Index futures', 'Cash segment', 'Stock futures'],
        'value': [
            total['index_options_crore'], total['stock_options_crore'], total['index_futures_crore'],
            total['cash_segment_crore'], total['stock_futures_crore']
        ]
    })
    seg['abs'] = seg['value'].abs()
    fig = px.bar(seg, x='abs', y='segment', orientation='h', color='value',
                 color_continuous_scale=['#ff6b6b', '#ffd43b', '#51cf66'])
    fig.update_layout(
        height=280, margin=dict(l=8, r=8, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False, xaxis_title='Absolute contribution (₹ Cr)', yaxis_title='', font=dict(color='#d9e1ef')
    )
    fig.update_traces(hovertemplate='%{y}: %{customdata}<extra></extra>', customdata=seg['value'])
    return fig


def simulator(delta, gamma, kappa, move_bps):
    # Educational stylized simulator based on the uploaded note.
    pnl_opt = delta * move_bps + 0.5 * gamma * (move_bps ** 2)
    pnl_cash = -kappa * abs(move_bps)
    pnl_net = pnl_opt + pnl_cash
    return pnl_opt, pnl_cash, pnl_net


def simulator_curve(delta, gamma, kappa, lo=-20, hi=20):
    xs = np.arange(lo, hi + 1)
    rows = []
    for x in xs:
        opt, cash, net = simulator(delta, gamma, kappa, x)
        rows.append((x, opt, cash, net))
    return pd.DataFrame(rows, columns=['move_bps', 'pnl_opt', 'pnl_cash', 'pnl_net'])


def footprint_score(volume_concentration, options_dominance, reversal_intensity, close_concentration, delta_build, timing_cluster):
    raw = (
        1.15 * volume_concentration +
        1.05 * options_dominance +
        1.20 * reversal_intensity +
        0.95 * close_concentration +
        1.10 * delta_build +
        0.85 * timing_cluster - 3.25
    )
    prob = 1 / (1 + math.exp(-raw))
    score = prob * 100
    band = 'Low' if score < 35 else 'Moderate' if score < 65 else 'High' if score < 85 else 'Very High'
    return score, band


def score_preset(name):
    presets = {
        'Jan 17, 2024 — BANKNIFTY intraday': (0.95, 0.98, 0.96, 0.40, 0.92, 0.97),
        'Jul 10, 2024 — BANKNIFTY close concentration': (0.82, 0.88, 0.76, 0.97, 0.87, 0.91),
        'May 15, 2025 — NIFTY post-caution': (0.66, 0.79, 0.52, 0.94, 0.81, 0.86),
        'Generic control day': (0.18, 0.26, 0.17, 0.22, 0.14, 0.19),
    }
    vals = presets[name]
    score, band = footprint_score(*vals)
    return vals, score, band


style_header()
overview_cards()

section_tabs = st.tabs([
    'Start Here','Overview', 'Impugned Days', 'Jan 17 Reconstruction', 'Entities & Economics',
    'Mechanistic Simulator', 'Footprint Scoring', 'Microstructure & Frontier Research', 'Data Room'
])

with section_tabs[0]:
    render_landing_page()

with section_tabs[1]:
    left, right = st.columns([1.15, 1], gap='large')
    with left:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Case timeline</div>", unsafe_allow_html=True)
        st.plotly_chart(make_timeline_chart(timeline), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Case structure</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='insight-card'>
              <h4>Intraday index manipulation</h4>
              <p>Observed on most exam-period days: aggressive support in underlying constituents, derivative positioning during the induced move,
              then reversal pressure into the same session’s close.</p>
            </div>
            <div class='insight-card blue'>
              <h4>Extended marking the close</h4>
              <p>Observed on select BANKNIFTY days and the later NIFTY cases: concentrated intervention in the settlement-critical window,
              aligned with outsized expiring-option exposure.</p>
            </div>
            <div class='insight-card green'>
              <h4>Microstructure asymmetry</h4>
              <p>The core asymmetry comes from a smaller underlying cash/futures market interacting with a much larger options complex.
              On Jan 17, 2024, SEBI’s comparison placed BANKNIFTY options cash-equivalent turnover far above the underlying segments.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap='large')
    with c1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Pattern counts</div>", unsafe_allow_html=True)
        counts = imp.groupby('strategy').size().reset_index(name='days')
        fig = px.pie(counts, names='strategy', values='days', color='strategy',
                     color_discrete_map={
                         'Intra-day Index Manipulation': '#e8590c',
                         'Extended Marking the Close': '#4dabf7'
                     }, hole=0.62)
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#d9e1ef'))
        fig.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Microstructure highlights</div>", unsafe_allow_html=True)
        highlights = [
            ("Options-to-cash turnover", metrics.loc[metrics.metric == 'ratio_options_to_cash', 'value'].iloc[0], 'x'),
            ("Options-to-combined ratio", metrics.loc[metrics.metric == 'ratio_options_to_combined', 'value'].iloc[0], 'x'),
            ("Unique index-options participants", metrics.loc[metrics.metric == 'unique_entities_index_options', 'value'].iloc[0], ''),
            ("Peak single-day net profit", metrics.loc[metrics.metric == 'js_day_net_profit', 'value'].iloc[0], 'Cr'),
        ]
        for title, value, suffix in highlights:
            st.markdown(f"<div class='insight-card yellow'><h4>{title}</h4><p><span class='badge'>{value:,.0f}{suffix}</span></p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[1]:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    colf1, colf2 = st.columns([1, 4])
    with colf1:
        strat = st.selectbox('Filter strategy', ['All', 'Intraday', 'Extended Close'])
    df = imp.copy()
    if strat == 'Intraday':
        df = df[df['strategy'].str.contains('Intra', case=False, na=False)]
    elif strat == 'Extended Close':
        df = df[df['strategy'].str.contains('Extended', case=False, na=False)]
    st.plotly_chart(make_impugned_chart(df), use_container_width=True)
    show = df.copy()
    show['date'] = pd.to_datetime(show['date']).dt.strftime('%Y-%m-%d')
    show['profit_crore'] = show['profit_crore'].map(lambda x: f"₹{x:,.2f}")
    st.dataframe(show[['date', 'index', 'strategy', 'profit_crore', 'examination_period']], use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[2]:
    left, right = st.columns([1.25, 1], gap='large')
    with left:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Session path reconstruction</div>", unsafe_allow_html=True)
        st.plotly_chart(make_jan17_chart(jan17_path()), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Phase decomposition</div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='insight-card'>
              <h4>Patch I — support / lift</h4>
              <p>SEBI described roughly ₹{metrics.loc[metrics.metric == 'js_patch_i_total_position', 'value'].iloc[0]:,.2f} Cr of cash + futures positioning in BANKNIFTY constituents,
              with the group acting as the dominant early buyer.</p>
            </div>
            <div class='insight-card blue'>
              <h4>Patch II — unwind / pressure</h4>
              <p>Cash selling of about ₹{metrics.loc[metrics.metric == 'js_patch_ii_cash_sold', 'value'].iloc[0]:,.2f} Cr and index-futures selling of about
              ₹{metrics.loc[metrics.metric == 'js_patch_ii_futures_sold', 'value'].iloc[0]:,.2f} Cr compounded the close-side move.</p>
            </div>
            <div class='insight-card green'>
              <h4>Economic asymmetry</h4>
              <p>The equity/futures loss was comparatively small next to the options outcome: about ₹{metrics.loc[metrics.metric == 'js_intraday_equity_futures_loss', 'value'].iloc[0]:,.1f} Cr
              loss against a same-day net options profit near ₹{metrics.loc[metrics.metric == 'js_day_net_profit', 'value'].iloc[0]:,.2f} Cr.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Event log</div>", unsafe_allow_html=True)
    st.dataframe(jan17, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[3]:
    c1, c2 = st.columns([1.15, 1], gap='large')
    with c1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Entity/PAN view</div>", unsafe_allow_html=True)
        show_ent = ent[ent['entity_id'] != 'TOTAL'].copy()
        st.dataframe(show_ent[['entity_name', 'pan', 'jurisdiction', 'incorporation_region', 'index_options_crore', 'stock_futures_crore', 'total_profit_crore']],
                     use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Segment economics</div>", unsafe_allow_html=True)
        st.plotly_chart(segment_profit_chart(ent), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Entity contribution</div>", unsafe_allow_html=True)
    entity_plot = show_ent.sort_values('total_profit_crore', ascending=True)
    fig = px.bar(entity_plot, x='total_profit_crore', y='entity_name', orientation='h', color='jurisdiction',
                 color_discrete_map={'FPI': '#4dabf7', 'Domestic': '#e8590c'})
    fig.update_layout(height=280, margin=dict(l=8, r=8, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      xaxis_title='Total profit (₹ Cr)', yaxis_title='', font=dict(color='#d9e1ef'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[4]:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Mechanistic simulator</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='micro-note'>A stylized educational simulator based on the uploaded quantitative note: index move as the intermediate state variable, option convexity as the non-linear amplifier, and cash-market impact as the frictional cost.</div>",
        unsafe_allow_html=True,
    )
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        delta = st.slider('Δ (option delta coefficient)', min_value=0.0, max_value=2.5, value=0.8, step=0.05)
    with s2:
        gamma = st.slider('Γ (gamma / convexity coefficient)', min_value=0.0, max_value=1.5, value=0.25, step=0.01)
    with s3:
        kappa = st.slider('κ (impact cost per bp)', min_value=0.0, max_value=2.0, value=0.30, step=0.01)
    with s4:
        move_bps = st.slider('Induced index move (bps)', min_value=-20, max_value=20, value=8, step=1)

    pnl_opt, pnl_cash, pnl_net = simulator(delta, gamma, kappa, move_bps)
    m1, m2, m3 = st.columns(3)
    m1.metric('P&L — options leg', f"{pnl_opt:,.2f}")
    m2.metric('P&L — cash / impact leg', f"{pnl_cash:,.2f}")
    m3.metric('P&L — net', f"{pnl_net:,.2f}")

    curve = simulator_curve(delta, gamma, kappa)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=curve['move_bps'], y=curve['pnl_opt'], mode='lines', name='Options leg', line=dict(color='#51cf66', width=3)))
    fig.add_trace(go.Scatter(x=curve['move_bps'], y=curve['pnl_cash'], mode='lines', name='Cash / impact', line=dict(color='#ff6b6b', width=3)))
    fig.add_trace(go.Scatter(x=curve['move_bps'], y=curve['pnl_net'], mode='lines', name='Net P&L', line=dict(color='#e9edf5', width=4)))
    fig.add_vline(x=move_bps, line_dash='dot', line_color='#e8590c')
    fig.update_layout(height=360, margin=dict(l=8, r=8, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      xaxis_title='Induced index move (bps)', yaxis_title='Stylized P&L units', font=dict(color='#d9e1ef'), yaxis=dict(gridcolor='rgba(255,255,255,.08)'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class='insight-card yellow'>
          <h4>Reading the simulator</h4>
          <p>The uploaded note models the index as a weighted sum of constituents and the option book as a second-order expansion in the induced move.
          This panel lets you stress the convexity term against an explicit impact-cost term and inspect where net payoff turns positive or negative.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[5]:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Footprint scoring engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='micro-note'>A pattern score built for surveillance-style attribution: not identity proof, but a calibrated lens on whether a day resembles the recurrent structure described in the case file.</div>", unsafe_allow_html=True)

    pcol, scol = st.columns([1, 1.2], gap='large')
    with pcol:
        preset = st.selectbox('Preset day profile', [
            'Jan 17, 2024 — BANKNIFTY intraday',
            'Jul 10, 2024 — BANKNIFTY close concentration',
            'May 15, 2025 — NIFTY post-caution',
            'Generic control day',
            'Custom input',
        ])
        if preset != 'Custom input':
            vals, preset_score, preset_band = score_preset(preset)
            vc, od, ri, cc, db, tc = vals
            st.markdown(f"<div class='badge'>{preset_band} footprint · {preset_score:,.1f}/100</div>", unsafe_allow_html=True)
        else:
            vc = st.slider('Volume concentration', 0.0, 1.0, 0.50, 0.01)
            od = st.slider('Options dominance', 0.0, 1.0, 0.50, 0.01)
            ri = st.slider('Reversal intensity', 0.0, 1.0, 0.50, 0.01)
            cc = st.slider('Close concentration', 0.0, 1.0, 0.50, 0.01)
            db = st.slider('Delta build intensity', 0.0, 1.0, 0.50, 0.01)
            tc = st.slider('Timing cluster strength', 0.0, 1.0, 0.50, 0.01)
            preset_score, preset_band = footprint_score(vc, od, ri, cc, db, tc)

        score, band = footprint_score(vc, od, ri, cc, db, tc)
        st.metric('Footprint score', f"{score:,.1f}/100", band)

        radar_df = pd.DataFrame({
            'metric': ['Volume concentration', 'Options dominance', 'Reversal intensity', 'Close concentration', 'Delta build', 'Timing cluster'],
            'value': [vc, od, ri, cc, db, tc]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=radar_df['value'], theta=radar_df['metric'], fill='toself', line=dict(color='#e8590c', width=3), fillcolor='rgba(232,89,12,0.22)'))
        fig.update_layout(height=360, polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0,1], gridcolor='rgba(255,255,255,.08)', tickfont=dict(color='#8d96aa')), angularaxis=dict(tickfont=dict(color='#d9e1ef'))),
                          paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with scol:
        st.markdown("<div class='section-title'>Score anatomy</div>", unsafe_allow_html=True)
        contributions = pd.DataFrame({
            'component': ['Volume concentration', 'Options dominance', 'Reversal intensity', 'Close concentration', 'Delta build', 'Timing cluster'],
            'weighted_value': [1.15*vc, 1.05*od, 1.20*ri, 0.95*cc, 1.10*db, 0.85*tc]
        })
        fig2 = px.bar(contributions, x='weighted_value', y='component', orientation='h', color='weighted_value', color_continuous_scale=['#4dabf7', '#e8590c'])
        fig2.update_layout(height=360, margin=dict(l=8, r=8, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False,
                           xaxis_title='Weighted contribution', yaxis_title='', font=dict(color='#d9e1ef'))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(
            """
            <div class='insight-card blue'>
              <h4>Interpretation</h4>
              <p>High scores require a joint configuration: concentration in the relevant instruments, a derivative-over-underlying imbalance,
              deliberate reversal or settlement-window behavior, and a time-clustered build in directional exposure. The score is intended as a research proxy for recurring fingerprints.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[6]:
    left, right = st.columns(2, gap='large')
    with left:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Why this matters for market microstructure</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='insight-card'>
              <h4>1) Cross-market asymmetry</h4>
              <p>When the derivatives complex is several times larger than the immediate price-forming underlying segment, modest pressure in the latter can create disproportionate repricing in the former.</p>
            </div>
            <div class='insight-card blue'>
              <h4>2) Settlement-window fragility</h4>
              <p>Expiry conventions, close-based settlement formulas, and time-weighted or VWAP-style mechanisms can create narrow windows in which seemingly local order flow has outsized payoff significance.</p>
            </div>
            <div class='insight-card green'>
              <h4>3) Surveillance design</h4>
              <p>The useful unit of analysis is rarely a single order. It is the linked pattern: constituent baskets, derivatives, time clustering, order-book pressure, and reversal behavior inside the same session or expiry cycle.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Frontier expansion</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='insight-card yellow'>
              <h4>South Korea block-trade lens</h4>
              <p>Extend the framework to block-trade ecosystems by mapping dealer facilitation, post-trade drift, close-window liquidity shocks,
              and the relationship between block-print timing and index/derivative repricing. The goal is to look for repeated footprints, not to assume the same mechanism ex ante.</p>
            </div>
            <div class='insight-card blue'>
              <h4>Crypto venue lens</h4>
              <p>Translate the same research logic to perpetuals/options/spot ecosystems: lead-lag between spot and derivatives, sudden open-interest changes,
              exchange-specific funding behavior, and bursts of concentrated activity during low-depth intervals.</p>
            </div>
            <div class='insight-card'>
              <h4>Transferability test</h4>
              <p>Use a shared feature family across India, South Korea, and crypto: concentration, settlement sensitivity, directional exposure build,
              order-book impact, and reversal signatures. This allows a unified scoring surface across very different market designs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Research checklist</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='micro-note'>Useful next layers: settlement-rule mapping, block-trade timestamps, options-chain depth snapshots, constituent-weight sensitivity,
        venue-specific open-interest and funding events, and cross-venue lead-lag analysis. A transferable workflow starts with footprint extraction, then regime segmentation, then comparative scoring.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with section_tabs[7]:
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Dataset explorer</div>", unsafe_allow_html=True)
    dataset_name = st.selectbox('Select dataset', {
        'Impugned days': imp,
        'Entities / profits': ent,
        'Case timeline': timeline,
        'Jan 17 sample day': jan17,
        'Market structure metrics': metrics,
    }.keys())
    selected = {
        'Impugned days': imp,
        'Entities / profits': ent,
        'Case timeline': timeline,
        'Jan 17 sample day': jan17,
        'Market structure metrics': metrics,
    }[dataset_name]
    st.dataframe(selected, use_container_width=True, hide_index=True)
    csv = selected.to_csv(index=False).encode('utf-8')
    st.download_button('Download selected dataset as CSV', csv, file_name=f"{dataset_name.lower().replace(' ', '_')}.csv", mime='text/csv')
    st.markdown("</div>", unsafe_allow_html=True)
