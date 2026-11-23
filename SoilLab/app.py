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
