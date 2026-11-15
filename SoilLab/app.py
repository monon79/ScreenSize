import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

from soil_lab.calculations import (
    clean_sieve_data,
    calculate_sieve_results,
    soil_parameters,
    design_filter_pack,
)
from soil_lab.reports import build_excel_report, build_pdf_report

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SoilLab | Groundwater Well Design",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================
st.session_state.setdefault("appearance", "Light")
st.session_state.setdefault("sieve_results", None)
st.session_state.setdefault("total_weight", None)

# ============================================================
# THEME / DESIGN SYSTEM
# ============================================================
THEMES = {
    "Light": {
        "bg": "#F4F7F9",
        "surface": "#FFFFFF",
        "surface2": "#EAF1F4",
        "text": "#1B2D3A",
        "muted": "#5A6F7D",
        "border": "#D5E0E6",
        "primary": "#1F6F85",
        "primary_hover": "#17586A",
        "on_primary": "#FFFFFF",
        "accent": "#DCEFEA",
        "success": "#1E7A52",
        "success_bg": "#E4F4EC",
        "warning": "#9A5F10",
        "warning_bg": "#FFF3DF",
        "danger": "#A8352F",
        "danger_bg": "#FCE9E7",
        "info_bg": "#E6F1F6",
        "shadow": "0 1px 3px rgba(20, 50, 65, .06), 0 6px 18px rgba(20, 50, 65, .05)",
        "hero_a": "#173B49",
        "hero_b": "#2F7A86",
        "plot_bg": "#FFFFFF",
        "plot_font": "#1B2D3A",
        "grid_major": "#B7C5CE",
        "grid_minor": "#E3EAEF",
        "aquifer": "#1F7A8C",
        "pack": "#D98A2B",
    },
    "Dark": {
        "bg": "#0F1A22",
        "surface": "#182733",
        "surface2": "#223543",
        "text": "#EAF1F4",
        "muted": "#A9BCC6",
        "border": "#2F4553",
        "primary": "#6DB8C8",
        "primary_hover": "#8FCCD9",
        "on_primary": "#0C2229",
        "accent": "#25494D",
        "success": "#76CFA3",
        "success_bg": "#15332A",
        "warning": "#EDBB70",
        "warning_bg": "#3A2E17",
        "danger": "#F09A94",
        "danger_bg": "#3D1E1D",
        "info_bg": "#1C3340",
        "shadow": "0 1px 3px rgba(0, 0, 0, .35)",
        "hero_a": "#1C3945",
        "hero_b": "#2D5A66",
        "plot_bg": "#182733",
        "plot_font": "#EAF1F4",
        "grid_major": "#4F6877",
        "grid_minor": "#2D4350",
        "aquifer": "#6DB8C8",
        "pack": "#F0B35E",
    },
}


def apply_theme():
    name = st.session_state["appearance"]
    t = THEMES[name]
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            color-scheme: {"dark" if name == "Dark" else "light"};
        }}

        /* ---------- Base ---------- */
        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background: {t["bg"]} !important;
            color: {t["text"]} !important;
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
            font-size: 16px;
            line-height: 1.55;
        }}
        button, input, textarea, select,
        [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"],
        [data-testid="stMetric"], [data-testid="stDataFrame"] {{
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
        }}
        [data-testid="stHeader"] {{ background: transparent !important; }}
        #MainMenu, footer {{ visibility: hidden; }}

        [data-testid="stMainBlockContainer"] {{
            max-width: 1280px;
            padding: 1.5rem 2rem 3rem 2rem;
        }}
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-size: 1rem;
            color: {t["text"]};
        }}

        /* ---------- Headings ---------- */
        h1, h2, h3, h4 {{
            font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
            color: {t["text"]} !important;
            letter-spacing: -0.02em;
            font-weight: 700 !important;
        }}
        h2 {{ font-size: 1.75rem !important; margin-top: .25rem !important; }}
        h3 {{ font-size: 1.3rem !important; margin-top: 1.1rem !important; }}
        h4 {{ font-size: 1.1rem !important; }}

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {{
            background: {t["surface"]} !important;
            border-right: 1px solid {t["border"]};
        }}
        [data-testid="stSidebar"] * {{ color: {t["text"]}; }}
        [data-testid="stSidebar"] h2 {{ font-size: 1.4rem !important; }}
        [data-testid="stSidebar"] h3 {{
            font-size: .8rem !important;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: {t["muted"]} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] .stCaption {{ color: {t["muted"]} !important; }}
        [data-testid="stSidebar"] [role="radiogroup"] label {{
            padding: .45rem .6rem;
            border-radius: 10px;
            transition: background .15s ease;
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
            background: {t["surface2"]};
        }}
        [data-testid="stSidebar"] [role="radiogroup"] label p {{
            font-size: 1rem !important;
            font-weight: 500;
        }}

        /* ---------- Metric cards ---------- */
        [data-testid="stMetric"] {{
            background: {t["surface"]};
            border: 1px solid {t["border"]};
            border-radius: 14px;
            padding: 14px 18px;
            box-shadow: {t["shadow"]};
            height: 100%;
        }}
        [data-testid="stMetricLabel"] p {{
            color: {t["muted"]} !important;
            font-size: .85rem !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: .04em;
        }}
        [data-testid="stMetricValue"] {{
            color: {t["text"]} !important;
            font-size: 1.55rem !important;
            font-weight: 700 !important;
            line-height: 1.25;
        }}
        [data-testid="stMetricValue"] > div {{
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }}

        /* ---------- Tables ---------- */
        [data-testid="stDataFrame"], [data-testid="stTable"] {{
            border: 1px solid {t["border"]};
            border-radius: 12px;
            overflow: hidden;
            box-shadow: {t["shadow"]};
        }}

        /* ---------- Inputs ---------- */
        [data-testid="stWidgetLabel"] p {{
            font-size: .95rem !important;
            font-weight: 600;
            color: {t["text"]} !important;
        }}
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div,
        [data-testid="stNumberInput"] div[data-baseweb="input"] {{
            background: {t["surface"]} !important;
            border-color: {t["border"]} !important;
            color: {t["text"]} !important;
            border-radius: 10px !important;
        }}
        input, textarea {{ color: {t["text"]} !important; font-size: 1rem !important; }}
        div[data-baseweb="select"] * {{ color: {t["text"]} !important; }}
        div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li {{
            background: {t["surface"]} !important;
            color: {t["text"]} !important;
        }}
        div[data-baseweb="popover"] li:hover {{ background: {t["surface2"]} !important; }}

        [data-testid="stFileUploader"] section {{
            background: {t["surface"]};
            border: 2px dashed {t["border"]};
            border-radius: 14px;
            padding: 1.1rem;
        }}
        [data-testid="stFileUploader"] section * {{ color: {t["text"]} !important; }}

        /* ---------- Buttons ---------- */
        .stButton > button, .stDownloadButton > button {{
            border-radius: 10px;
            border: 1px solid {t["border"]};
            background: {t["surface"]};
            color: {t["text"]};
            min-height: 2.8rem;
            font-size: 1rem;
            font-weight: 600;
            transition: all .15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: {t["primary"]};
            color: {t["primary"]};
            transform: translateY(-1px);
        }}
        .stButton > button[kind="primary"] {{
            background: {t["primary"]};
            color: {t["on_primary"]};
            border: none;
            font-size: 1.05rem;
            min-height: 3rem;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: {t["primary_hover"]};
            color: {t["on_primary"]};
        }}
        .stButton > button[kind="primary"] p {{ color: {t["on_primary"]} !important; }}

        /* ---------- Alerts ---------- */
        div[data-testid="stAlert"] {{
            border-radius: 12px;
            font-size: .98rem;
        }}

        /* ---------- Custom components ---------- */
        .sl-hero {{
            background: linear-gradient(115deg, {t["hero_a"]}, {t["hero_b"]});
            border-radius: 18px;
            padding: 1.5rem 1.8rem;
            margin-bottom: 1.4rem;
            box-shadow: 0 8px 24px rgba(15, 50, 65, .14);
        }}
        .sl-hero h1 {{
            color: #FFFFFF !important;
            margin: 0 !important;
            font-size: 2.1rem !important;
            font-weight: 800 !important;
        }}
        .sl-hero p {{
            color: #DCEBEE !important;
            margin: .4rem 0 0 0 !important;
            font-size: 1.05rem !important;
        }}
        .sl-section-note {{
            color: {t["muted"]} !important;
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: .8rem;
        }}
        .sl-card {{
            background: {t["surface"]};
            border: 1px solid {t["border"]};
            border-radius: 16px;
            padding: 1.2rem 1.4rem;
            box-shadow: {t["shadow"]};
            height: 100%;
        }}
        .sl-card .sl-step {{
            display: inline-block;
            background: {t["accent"]};
            color: {t["success"]};
            font-weight: 800;
            font-size: .85rem;
            padding: .15rem .6rem;
            border-radius: 999px;
            margin-bottom: .5rem;
        }}
        .sl-card h4 {{ margin: 0 0 .35rem 0 !important; }}
        .sl-card p {{ margin: 0; color: {t["muted"]} !important; font-size: .97rem; }}
        .sl-banner {{
            border-radius: 14px;
            padding: 1rem 1.3rem;
            margin: .6rem 0 1rem 0;
            border: 1px solid transparent;
        }}
        .sl-banner .sl-banner-label {{
            font-size: .78rem; font-weight: 700;
            letter-spacing: .08em; text-transform: uppercase; opacity: .85;
        }}
        .sl-banner .sl-banner-title {{ font-size: 1.4rem; font-weight: 800; margin-top: .15rem; }}
        .sl-banner-danger  {{ background: {t["danger_bg"]};  color: {t["danger"]};  border-color: {t["danger"]}55; }}
        .sl-banner-success {{ background: {t["success_bg"]}; color: {t["success"]}; border-color: {t["success"]}55; }}
        .sl-check {{
            display: flex; align-items: center; gap: .7rem;
            background: {t["surface"]};
            border: 1px solid {t["border"]};
            border-radius: 10px;
            padding: .6rem .9rem;
            margin-bottom: .45rem;
            font-size: .98rem;
        }}
        .sl-check .sl-dot {{
            width: 1.5rem; height: 1.5rem; border-radius: 50%;
            display: inline-flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: .85rem; flex-shrink: 0;
        }}
        .sl-met .sl-dot    {{ background: {t["success_bg"]}; color: {t["success"]}; }}
        .sl-notmet .sl-dot {{ background: {t["surface2"]};   color: {t["muted"]}; }}
        .sl-check .sl-status {{ margin-left: auto; font-weight: 700; }}
        .sl-met .sl-status    {{ color: {t["success"]}; }}
        .sl-notmet .sl-status {{ color: {t["muted"]}; }}
        hr {{ border-color: {t["border"]} !important; }}

        /* ---------- Responsive ---------- */
        @media (max-width: 900px) {{
            [data-testid="stMainBlockContainer"] {{ padding: 1rem; }}
            .sl-hero h1 {{ font-size: 1.6rem !important; }}
            [data-testid="stMetricValue"] {{ font-size: 1.3rem !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return t


theme = apply_theme()

# ============================================================
# HEADER AND SIDEBAR
# ============================================================
st.markdown(
    """
    <div class="sl-hero">
        <h1>🌿 SoilLab</h1>
        <p>Soil particle-size analysis · Well selection · Screen and gravel-pack design</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🌿 SoilLab")
    st.caption("Groundwater well-design workspace")
    st.divider()

    page = st.radio(
        "Workspace",
        [
            "Welcome",
            "Sieve Analysis",
            "Automatic Well Selection",
            "Filter-Pack Design",
            "Settings & Help",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Appearance")
    appearance_choice = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state["appearance"] == "Light" else 1,
        horizontal=True,
        key="sidebar_appearance",
        label_visibility="collapsed",
    )
    if appearance_choice != st.session_state["appearance"]:
        st.session_state["appearance"] = appearance_choice
        st.rerun()
    st.caption("Theme is kept for this session.")

SAMPLE_DATA = pd.DataFrame({
    "sieve_mm": [4.75, 2.00, 0.425, 0.250, 0.150, 0.075, 0.0],
    "retained_g": [25, 45, 110, 90, 100, 80, 50],
})

D_KEYS = ["D10", "D30", "D40", "D60", "D70"]

# ============================================================
# COMMON HELPERS
# ============================================================
def fmt_mm(value, digits=3):
    return f"{value:.{digits}f} mm" if value is not None else "Not bracketed"


def fmt_num(value, digits=2):
    return f"{value:.{digits}f}" if value is not None else "N/A"


def note(text):
    st.markdown(f'<p class="sl-section-note">{text}</p>', unsafe_allow_html=True)


def render_d_values(params):
    cols = st.columns(5)
    for col, key in zip(cols, D_KEYS):
        col.metric(key, fmt_mm(params[key]))


def collect_sieve_data():
    st.subheader("1 · Laboratory sample")
    note(
        "Enter the dry mass retained on each sieve. Use <b>0 mm</b> for the pan. "
        "All sieve openings must be in millimetres."
    )

    method = st.radio(
        "Data-entry method",
        ["Manual entry", "Upload Excel"],
        horizontal=True,
        key="data_method",
    )

    total_mass = st.number_input(
        "Total dry sample mass (g)",
        min_value=0.01,
        value=500.0,
        step=10.0,
        help="The dry mass of the complete sample before sieving.",
    )

    if method == "Manual entry":
        st.caption("Tip: click the bottom row of the table to add a sieve, or select a row and press Delete to remove it.")
        data = st.data_editor(
            SAMPLE_DATA,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="manual_sieve_table",
            column_config={
                "sieve_mm": st.column_config.NumberColumn(
                    "Sieve opening (mm)", min_value=0.0, format="%.3f",
                ),
                "retained_g": st.column_config.NumberColumn(
                    "Mass retained (g)", min_value=0.0, format="%.2f",
                ),
            },
        )
        return data, total_mass

    template = BytesIO()
    SAMPLE_DATA.to_excel(template, index=False, engine="openpyxl")
    st.download_button(
        "⬇ Download Excel template",
        data=template.getvalue(),
        file_name="SoilLab_input_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.caption("Required Excel columns: sieve_mm and retained_g.")
    uploaded = st.file_uploader("Upload sieve-analysis workbook", type=["xlsx"])
    if uploaded is None:
        return None, total_mass
    try:
        return pd.read_excel(uploaded), total_mass
    except Exception as exc:
        st.error(f"Unable to read this workbook: {exc}")
        return None, total_mass


def draw_gradation_curve(results, extra_curve=None, title="Grain-Size Distribution Curve"):
    t = theme
    formation = results.loc[
        results["sieve_mm"] > 0,
        ["sieve_mm", "percent_passing"],
    ].sort_values("sieve_mm")

    if formation.empty:
        st.warning("No positive sieve openings are available for the graph.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=formation["sieve_mm"],
        y=formation["percent_passing"],
        mode="lines+markers",
        name="Aquifer formation",
        line=dict(color=t["aquifer"], width=3.5),
        marker=dict(size=9, color=t["aquifer"], line=dict(width=1.5, color=t["plot_bg"])),
        hovertemplate="Particle size: %{x:.4g} mm<br>Passing: %{y:.2f}%<extra></extra>",
    ))

    if extra_curve is not None:
        fig.add_trace(go.Scatter(
            x=extra_curve["particle_size_mm"],
            y=extra_curve["percent_passing"],
            mode="lines",
            name="Proposed filter pack",
            line=dict(color=t["pack"], width=3.5, dash="dash"),
            hovertemplate="Particle size: %{x:.4g} mm<br>Passing: %{y:.2f}%<extra></extra>",
        ))

    min_size = float(formation["sieve_mm"].min())
    max_size = float(formation["sieve_mm"].max())
    if extra_curve is not None:
        min_size = min(min_size, float(extra_curve["particle_size_mm"].min()))
        max_size = max(max_size, float(extra_curve["particle_size_mm"].max()))

    log_min = np.floor(np.log10(max(min_size, 1e-6)))
    log_max = np.ceil(np.log10(max_size))
    if log_min == log_max:
        log_min -= 1
        log_max += 1

    font_color = t["plot_font"]
    fig.update_layout(
        title=dict(text=title, x=0.01, xanchor="left", font=dict(size=20)),
        template="plotly_dark" if st.session_state["appearance"] == "Dark" else "plotly_white",
        height=580,
        hovermode="closest",
        margin=dict(l=80, r=40, t=80, b=100),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14)),
        plot_bgcolor=t["plot_bg"],
        paper_bgcolor=t["plot_bg"],
        font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=14, color=font_color),
    )
    fig.update_xaxes(
        title=dict(text="Particle size, D (mm)", font=dict(size=15)),
        type="log",
        range=[log_min, log_max],
        dtick=1,
        showline=True,
        linecolor=font_color,
        mirror=True,
        showgrid=True,
        gridcolor=t["grid_major"],
        minor=dict(showgrid=True, gridcolor=t["grid_minor"], dtick="D1"),
        ticks="outside",
        tickfont=dict(size=13),
        zeroline=False,
    )
    fig.update_yaxes(
        title=dict(text="Percentage finer / passing (%)", font=dict(size=15)),
        range=[0, 100],
        dtick=10,
        ticksuffix="%",
        showline=True,
        linecolor=font_color,
        mirror=True,
        showgrid=True,
        gridcolor=t["grid_major"],
        minor=dict(showgrid=True, gridcolor=t["grid_minor"], dtick=5),
        ticks="outside",
        tickfont=dict(size=13),
        zeroline=False,
    )
    for pct, label in [(10, "D10"), (30, "D30"), (40, "D40"), (60, "D60"), (70, "D70")]:
        fig.add_hline(
            y=pct,
            line_dash="dot",
            line_color=t["muted"],
            line_width=1,
            annotation_text=f"{label} · {pct}%",
            annotation_position="top left",
            annotation_font=dict(size=11, color=t["muted"]),
        )

    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})
    st.caption(
        "Semi-logarithmic graph: logarithmic particle-size axis (mm) and "
        "linear percentage-passing axis (%). Hover over a point to read exact values."
    )


def get_current_results():
    return st.session_state.get("sieve_results")


def automatic_decision(params, formation_condition):
    required = [params.get(k) for k in ["D10", "D40", "D70", "Cu"]]
    if any(value is None for value in required):
        return None

    d10, d40, d70, cu = params["D10"], params["D40"], params["D70"], params["Cu"]
    slot_low = 0.40 * d40
    slot_high = 0.70 * d70

    homogeneous_trigger = (
        formation_condition == "Homogeneous / uniform"
        and cu < 3.0
        and d10 < 0.25
    )
    fine_slot_trigger = slot_high < 0.75

    if homogeneous_trigger or fine_slot_trigger:
        well_type = "Artificial gravel-packed well"
    else:
        well_type = "Naturally developed well (preliminary)"

    reasons = []
    if homogeneous_trigger:
        reasons.append("Formation marked homogeneous / uniform, Cu < 3, and D10 < 0.25 mm.")
    if fine_slot_trigger:
        reasons.append("The interpreted upper slot-size estimate (0.70 × D70) is below 0.75 mm.")

    return {
        "well_type": well_type,
        "slot_low": slot_low,
        "slot_high": slot_high,
        "homogeneous_trigger": homogeneous_trigger,
        "fine_slot_trigger": fine_slot_trigger,
        "reasons": reasons,
    }


def banner(kind, label, title):
    st.markdown(
        f'<div class="sl-banner sl-banner-{kind}">'
        f'<div class="sl-banner-label">{label}</div>'
        f'<div class="sl-banner-title">{title}</div></div>',
        unsafe_allow_html=True,
    )


def check_row(label, passed):
    cls = "sl-met" if passed else "sl-notmet"
    icon = "✓" if passed else "–"
    status = "Met" if passed else "Not met"
    st.markdown(
        f'<div class="sl-check {cls}"><span class="sl-dot">{icon}</span>'
        f'<span>{label}</span><span class="sl-status">{status}</span></div>',
        unsafe_allow_html=True,
    )


def step_card(step, title, text):
    st.markdown(
        f'<div class="sl-card"><span class="sl-step">STEP {step}</span>'
        f'<h4>{title}</h4><p>{text}</p></div>',
        unsafe_allow_html=True,
    )

# ============================================================
# WELCOME
# ============================================================
if page == "Welcome":
    st.header("Welcome to SoilLab")
    note(
        "A guided workspace for sieve analysis, grain-size distribution, "
        "preliminary well selection and gravel-pack design."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        step_card("01", "Analyse", "Enter laboratory sieve data or upload an Excel workbook.")
    with c2:
        step_card("02", "Decide", "Review D-values and get a preliminary natural or gravel-packed well recommendation.")
    with c3:
        step_card("03", "Design", "Estimate filter-pack gradation and screen-opening limits.")

    st.write("")
    st.info("**Quick start:** open **Sieve Analysis** in the left navigation. A sample dataset is preloaded so you can explore the app right away.")

    st.subheader("Units used throughout SoilLab")
    u1, u2, u3 = st.columns(3)
    u1.metric("Particle / sieve size", "mm")
    u2.metric("Mass", "g")
    u3.metric("Percentages", "%")

# ============================================================
# SIEVE ANALYSIS
# ============================================================
elif page == "Sieve Analysis":
    st.header("Sieve analysis")
    note(
        "Enter one representative aquifer sample. Check the mass recovery "
        "before using the calculated parameters for well design."
    )
    raw, total_mass = collect_sieve_data()

    st.write("")
    if st.button("Calculate sieve analysis", type="primary", use_container_width=True):
        if raw is None:
            st.error("Please enter data or upload an Excel file.")
        else:
            try:
                clean = clean_sieve_data(raw)
                results = calculate_sieve_results(clean, total_mass)
                st.session_state["sieve_results"] = results
                st.session_state["total_weight"] = total_mass
                st.success("Sieve analysis calculated successfully.")
            except (ValueError, TypeError, OverflowError) as exc:
                st.error(str(exc))

    results = get_current_results()
    if results is not None:
        recovery = results.attrs.get("mass_recovery_pct")
        if recovery is None:
            recovery = results["retained_g"].sum() / st.session_state["total_weight"] * 100
        params = soil_parameters(results)

        st.divider()
        st.subheader("2 · Calculation summary")
        a, b, c = st.columns(3)
        a.metric("Mass recovery", f"{recovery:.2f} %")
        b.metric("Mass retained", f'{results["retained_g"].sum():.2f} g')
        c.metric("Dry sample mass", f'{st.session_state["total_weight"]:.2f} g')

        if recovery < 99.5:
            st.warning(
                "Mass recovery is below 99.5%. Some material may have been lost during "
                "sieving or transfer. Interpret the fine end of the curve cautiously."
            )
        elif recovery > 100.5:
            st.warning(
                "Mass recovery is above 100.5%. Check the weighings, moisture content "
                "and total sample mass entered."
            )
        else:
            st.success("Mass recovery is within the accepted checking band (99.5% – 100.5%).")

        st.subheader("3 · Sieve-analysis table")
        view = results.rename(columns={
            "sieve_mm": "Sieve opening (mm)",
            "retained_g": "Mass retained (g)",
            "percent_retained": "Retained (%)",
            "cumulative_retained_pct": "Cumulative retained (%)",
            "percent_passing": "Percentage passing (%)",
        })[[
            "Sieve opening (mm)", "Mass retained (g)", "Retained (%)",
            "Cumulative retained (%)", "Percentage passing (%)",
        ]]
        st.dataframe(
            view,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sieve opening (mm)": st.column_config.NumberColumn(format="%.3f"),
                "Mass retained (g)": st.column_config.NumberColumn(format="%.2f"),
                "Retained (%)": st.column_config.NumberColumn(format="%.2f"),
                "Cumulative retained (%)": st.column_config.NumberColumn(format="%.2f"),
                "Percentage passing (%)": st.column_config.NumberColumn(format="%.2f"),
            },
        )

        st.subheader("4 · Characteristic particle sizes")
        render_d_values(params)
        st.write("")
        p1, p2 = st.columns(2)
        p1.metric("Coefficient of uniformity (Cu)", fmt_num(params["Cu"]))
        p2.metric("Coefficient of curvature (Cc)", fmt_num(params["Cc"]))

        st.subheader("5 · Semi-logarithmic gradation curve")
        draw_gradation_curve(results)

        st.subheader("6 · Download reports")
        excel_data = build_excel_report(results, params, recovery)
        pdf_data = build_pdf_report(results, params, recovery)
        dl1, dl2 = st.columns(2)
        dl1.download_button(
            "⬇ Download Excel report",
            data=excel_data,
            file_name="SoilLab_sieve_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        dl2.download_button(
            "⬇ Download PDF report",
            data=pdf_data,
            file_name="SoilLab_sieve_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# ============================================================
# AUTOMATIC WELL SELECTION
# ============================================================
elif page == "Automatic Well Selection":
    st.header("Automatic well-type selection")
    results = get_current_results()

    if results is None:
        st.info("First complete a **Sieve Analysis**. Your results will then be available here.")
    else:
        params = soil_parameters(results)
        note(
            "SoilLab applies the preliminary rules transcribed from your supplied "
            "well-screen design slides."
        )

        st.subheader("Aquifer properties")
        render_d_values(params)
        st.write("")
        st.metric("Aquifer coefficient of uniformity (Cu)", fmt_num(params["Cu"], 3))

        st.divider()
        st.subheader("Formation condition")
        formation_condition = st.selectbox(
            "Formation condition from bore log",
            ["Not sure / variable layers", "Homogeneous / uniform", "Coarse / non-uniform"],
            help="Use the bore log and field observations. Cu alone does not prove that a formation is homogeneous.",
        )
        decision = automatic_decision(params, formation_condition)

        if decision is None:
            st.error(
                "The required D10, D40, D70 or Cu value is outside the measured range. "
                "Add suitable sieve sizes or obtain a complete curve."
            )
        else:
            st.subheader("Preliminary recommendation")
            if decision["well_type"].startswith("Artificial"):
                banner("danger", "Recommended", "Artificial gravel-packed well")
            else:
                banner("success", "Preliminary option", "Naturally developed well")

            if decision["reasons"]:
                st.markdown("**Reason(s)**")
                for reason in decision["reasons"]:
                    st.write(f"• {reason}")
            else:
                st.write(
                    "The gravel-pack trigger criteria from the supplied slides were not met. "
                    "Natural development is shown as a preliminary option only; verify "
                    "formation stability, fines migration and screen retention."
                )

            st.subheader("Criteria check")
            st.caption(
                "The first three conditions act together as one trigger; the slot-size "
                "condition is a separate alternative trigger."
            )
            check_row("Homogeneous / uniform formation", formation_condition == "Homogeneous / uniform")
            check_row("Aquifer Cu < 3", params["Cu"] < 3)
            check_row("Aquifer D10 < 0.25 mm", params["D10"] < 0.25)
            check_row("0.70 × D70 < 0.75 mm", decision["slot_high"] < 0.75)

            st.subheader("Natural-well slot estimate")
            s1, s2 = st.columns(2)
            s1.metric("Lower estimate · 0.40 × D40", f'{decision["slot_low"]:.3f} mm')
            s2.metric("Upper estimate · 0.70 × D70", f'{decision["slot_high"]:.3f} mm')

        st.warning(
            "**Important:** this is an automatic preliminary recommendation using your supplied slide criteria. "
            "The 40–70% slot interpretation and 0.75 mm threshold should be confirmed with the original "
            "reference. Final well design requires professional review."
        )

# ============================================================
# FILTER PACK DESIGN
# ============================================================
elif page == "Filter-Pack Design":
    st.header("Filter-pack design")
    results = get_current_results()

    if results is None:
        st.info("Complete the **Sieve Analysis** first.")
    else:
        params = soil_parameters(results)
        note(
            "Design a theoretical filter-pack target curve using the D30 sizing "
            "ratio from your lecture slides."
        )

        st.subheader("Design inputs")
        i1, i2, i3 = st.columns(3)
        with i1:
            formation = st.selectbox(
                "Aquifer formation category",
                ["Fine and uniform", "Intermediate", "Coarse and non-uniform"],
            )
        suggested = {
            "Fine and uniform": 4,
            "Intermediate": 5,
            "Coarse and non-uniform": 6,
        }[formation]
        with i2:
            factor = st.selectbox(
                "Filter-pack D30 / aquifer D30 ratio",
                [4, 5, 6],
                index=[4, 5, 6].index(suggested),
                help=f"Suggested ratio for this formation category: {suggested}.",
            )
        with i3:
            target_cu = st.number_input(
                "Target filter-pack Cu",
                min_value=1.01,
                max_value=2.50,
                value=2.00,
                step=0.05,
            )

        if params["D30"] is None:
            st.error("Aquifer D30 cannot be determined from the current data.")
        else:
            try:
                pack_curve, pack = design_filter_pack(params["D30"], factor, target_cu)

                st.divider()
                st.subheader("Proposed filter-pack properties")
                pcols = st.columns(4)
                pcols[0].metric("Filter-pack D10", f'{pack["D10"]:.3f} mm')
                pcols[1].metric("Filter-pack D30", f'{pack["D30"]:.3f} mm')
                pcols[2].metric("Filter-pack D60", f'{pack["D60"]:.3f} mm')
                pcols[3].metric("Filter-pack Cu", f'{pack["Cu"]:.2f}')

                st.info(
                    f"**D30 (filter pack)** = {factor} × D30 (aquifer) = "
                    f"{factor} × {params['D30']:.3f} mm = **{pack['D30']:.3f} mm**."
                )
                st.metric(
                    "Preliminary maximum screen-opening check",
                    f'{pack["D10"]:.3f} mm',
                    help="Preliminary retention check only. Final screen design requires additional checks.",
                )

                st.subheader("Gradation curves")
                draw_gradation_curve(results, pack_curve, "Aquifer and Proposed Filter-Pack Gradation")

                st.subheader("Proposed filter-pack data")
                st.dataframe(
                    pack_curve.iloc[::15].rename(columns={
                        "particle_size_mm": "Particle size (mm)",
                        "percent_passing": "Percentage passing (%)",
                    }),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Particle size (mm)": st.column_config.NumberColumn(format="%.4f"),
                        "Percentage passing (%)": st.column_config.NumberColumn(format="%.2f"),
                    },
                )
                st.warning(
                    "This smooth curve is a theoretical lognormal grading target, not a tested gravel product. "
                    "Laboratory-test the actual filter-pack material and verify retention, permeability, "
                    "bridging, placement and screen compatibility."
                )
            except ValueError as exc:
                st.error(str(exc))

# ============================================================
# SETTINGS AND HELP
# ============================================================
elif page == "Settings & Help":
    st.header("Settings & Help")

    st.subheader("Appearance")
    st.write("Choose the visual theme that is most comfortable for your working environment.")
    selected_theme = st.radio(
        "Application theme",
        ["Light", "Dark"],
        index=0 if st.session_state["appearance"] == "Light" else 1,
        horizontal=True,
        key="settings_appearance",
    )
    if selected_theme != st.session_state["appearance"]:
        st.session_state["appearance"] = selected_theme
        st.rerun()
    st.caption("The selected theme applies to the interface and gradation graph for this session.")

    st.divider()
    st.subheader("How to use SoilLab")
    st.markdown("""
1. Enter sieve openings in **mm** and retained dry mass in **g**, or upload an Excel workbook.
2. Enter the total dry sample mass.
3. Calculate the sieve analysis and check mass recovery.
4. Review D10, D30, D40, D60, D70, Cu and Cc.
5. Open **Automatic Well Selection** and choose the formation condition based on the bore log.
6. If gravel packing is selected, use **Filter-Pack Design** to generate a preliminary grading curve.
""")

    st.divider()
    st.subheader("Design assumptions and limitations")
    st.markdown("""
- The automatic well recommendation uses preliminary criteria supplied in the user's lecture slides.
- The current interpretation uses a natural-well slot interval of 0.40 × D40 to 0.70 × D70.
- The gravel-pack trigger uses homogeneous / uniform formation, Cu < 3 and D10 < 0.25 mm, or an interpreted upper slot estimate below 0.75 mm.
- Filter-pack D30 is selected at 4, 5 or 6 times aquifer D30; target filter-pack Cu is limited to 2.5.
- The filter-pack curve is theoretical. Actual pack material must be tested by sieve analysis.
- Do not combine different aquifer strata into one averaged curve.
- Final design must consider aquifer stability, fines migration, screen retention, open area, entrance velocity, corrosion, structural strength, well development and manufacturer tolerances.
""")

st.divider()
st.caption("SoilLab · Particle and sieve sizes: mm · Mass: g · Percentages: % · Preliminary design support only.")