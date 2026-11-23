import streamlit as st
import pandas as pd
import numpy as np
import json
import streamlit.components.v1 as components
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
