import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
def setup_page_config(page_title="Menu Planning", page_icon="🍽️"):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )


# ─────────────────────────────────────────────
# THEME COLORS
# ─────────────────────────────────────────────
def get_theme_colors(dark_mode):
    if dark_mode:
        return {
            "bg_color":      "#0a0d13",
            "card_bg":       "#12161f",
            "card_bg2":      "#1a1f2e",
            "text_color":    "#f0f2f8",
            "text_muted":    "#8892a4",
            "border_color":  "#252d3d",
            "accent_color":  "#14b8a6",
            "accent2":       "#f97316",
            "accent3":       "#8b5cf6",
            "sidebar_bg":    "#0d1017",
            "hero_gradient": "linear-gradient(135deg, #0d9488 0%, #0a1628 60%, #0a0d13 100%)",
            "section_grad":  "linear-gradient(90deg, #14b8a6, #8b5cf6)",
        }
    else:
        return {
            "bg_color":      "#f4f6fb",
            "card_bg":       "#ffffff",
            "card_bg2":      "#eef2ff",
            "text_color":    "#111827",
            "text_muted":    "#6b7280",
            "border_color":  "#e0e7ef",
            "accent_color":  "#0d9488",
            "accent2":       "#f97316",
            "accent3":       "#7c3aed",
            "sidebar_bg":    "#f0f4fa",
            "hero_gradient": "linear-gradient(135deg, #0d9488 0%, #1d4ed8 60%, #312e81 100%)",
            "section_grad":  "linear-gradient(90deg, #0d9488, #7c3aed)",
        }


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def setup_sidebar():
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True

    c = get_theme_colors(st.session_state.dark_mode)

    with st.sidebar:
        # ── Theme toggle (styled via CSS in apply_custom_css) ──
        new_dark = st.toggle(
            "Dark Mode",
            value=st.session_state.dark_mode,
            key="theme_toggle"
        )
        st.session_state.dark_mode = new_dark
        c = get_theme_colors(new_dark)

        st.markdown("---")

        # ── Navigation ──
        st.markdown(f"""
        <div style="font-size:0.70rem;font-weight:700;color:{c['text_muted']};
             letter-spacing:1.2px;text-transform:uppercase;
             margin-bottom:6px;padding-left:4px;">
            Navigation
        </div>
        """, unsafe_allow_html=True)

        st.page_link("app.py",                       label="Dashboard",         icon=":material/home:")
        st.page_link("pages/1_Data_Overview.py",     label="Data Overview",     icon=":material/table_chart:")
        st.page_link("pages/2_Association_Rules.py", label="Association Rules", icon=":material/share:")
        st.page_link("pages/3_Customer_Segments.py", label="Customer Segments", icon=":material/group:")
        st.page_link("pages/4_Demand_Forecast.py",   label="Demand Forecast",   icon=":material/trending_up:")
        st.page_link("pages/5_Menu_Optimization.py", label="Menu Optimization", icon=":material/auto_fix_high:")

        st.markdown("---")

        # ── Team credits ──
        with st.expander("Project Team"):
            _team_card("VD", "Vinita Y. Deore",    "Role 316 · TYBCA Sem-VI", c)
            _team_card("IK", "Isha R. Khairnar",   "Role 326 · TYBCA Sem-VI", c)
            _team_card("VP", "Vaishnavi V. Pawar", "Role 343 · TYBCA Sem-VI", c)

    return st.session_state.dark_mode





def _team_card(initials, name, info, c):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:8px 0;
                padding:8px;border-radius:8px;background:{c['card_bg']};
                border:1px solid {c['border_color']};">
        <div style="width:36px;height:36px;border-radius:50%;
                    background:{c['hero_gradient']};
                    display:flex;align-items:center;justify-content:center;
                    font-weight:700;color:#fff;font-size:0.85rem;flex-shrink:0;">
            {initials}
        </div>
        <div>
            <div style="color:{c['text_color']};font-weight:600;font-size:0.82rem;">{name}</div>
            <div style="color:{c['text_muted']};font-size:0.69rem;">{info}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CSS INJECTION
# ─────────────────────────────────────────────
def apply_custom_css(dark_mode):
    c = get_theme_colors(dark_mode)

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        /* ── Background ── */
        .stApp {{
            background-color: {c['bg_color']};
        }}
        .main .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }}

        /* ── Always-visible Streamlit header toolbar ── */
        [data-testid="stHeader"] {{
            background: transparent !important;
            z-index: 999990 !important;
        }}
        [data-testid="stToolbar"],
        [data-testid="stAppToolbar"],
        .stAppToolbar {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999991 !important;
        }}
        [data-testid="stToolbar"] button,
        [data-testid="stAppToolbar"] button {{
            color: {c['text_color']} !important;
            opacity: 1 !important;
        }}
        /* Sidebar collapse/expand button always visible */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapsedControl"] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999992 !important;
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background-color: {c['sidebar_bg']};
            border-right: 1px solid {c['border_color']};
        }}
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div.stMarkdown,
        [data-testid="stSidebar"] label {{
            color: {c['text_color']};
        }}


        /* ── Hide default Streamlit auto page nav list only ── */
        [data-testid="stSidebarNav"] ul,
        [data-testid="stSidebarNavItems"] {{
            display: none !important;
        }}

        /* ── Always show sidebar open/close button ── */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}

        /* ── Style custom st.page_link buttons ── */
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {{
            border-radius: 8px;
            padding: 6px 10px;
            margin-bottom: 2px;
            font-size: 0.84rem;
            font-weight: 500;
            transition: background 0.15s ease;
            color: {c['text_color']} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {{
            background: {c['card_bg2']};
        }}
        [data-testid="stSidebar"] [aria-current="page"] {{
            background: {c['card_bg']};
            border-left: 3px solid {c['accent_color']};
            color: {c['accent_color']} !important;
            font-weight: 600;
        }}

        /* ── Style native st.toggle in sidebar ── */
        [data-testid="stSidebar"] [data-testid="stToggle"] {{
            background: {c['card_bg']};
            border: 1px solid {c['border_color']};
            border-radius: 10px;
            padding: 8px 12px;
            margin-bottom: 12px;
            width: 100%;
        }}
        [data-testid="stSidebar"] [data-testid="stToggle"] label {{
            font-size: 0.83rem !important;
            font-weight: 600 !important;
            color: {c['text_color']} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stToggle"] [data-baseweb="toggle"] {{
            transform: scale(1.1);
        }}

        /* ── Tab spacing: add gaps between tab labels ── */
        [data-testid="stTabs"] [role="tablist"] {{
            gap: 6px !important;
        }}
        [data-testid="stTabs"] button[role="tab"] {{
            border-radius: 8px 8px 0 0 !important;
            padding: 6px 16px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: {c['text_muted']} !important;
            background: {c['card_bg']} !important;
            border: 1px solid {c['border_color']} !important;
            border-bottom: none !important;
            transition: background 0.15s, color 0.15s;
        }}
        [data-testid="stTabs"] button[role="tab"]:hover {{
            background: {c['card_bg2']} !important;
            color: {c['text_color']} !important;
        }}
        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
            background: {c['accent_color']} !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border-color: {c['accent_color']} !important;
        }}

        .hero-banner {{
            background: {c['hero_gradient']};
            border-radius: 16px;
            padding: 32px 40px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::before {{
            content: "";
            position: absolute;
            top: -40px; right: -40px;
            width: 200px; height: 200px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        }}
        .hero-title {{
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            line-height: 1.2;
        }}
        .hero-sub {{
            font-size: 0.95rem;
            color: rgba(255,255,255,0.72);
            margin-top: 6px;
            font-weight: 400;
        }}
        .hero-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.72rem;
            color: #fff;
            font-weight: 600;
            margin-top: 12px;
            letter-spacing: 0.5px;
        }}

        /* ── Section Title ── */
        .section-title {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 20px 0 16px;
        }}
        .section-title-bar {{
            width: 4px;
            height: 24px;
            border-radius: 4px;
            background: {c['section_grad']};
        }}
        .section-title-text {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {c['text_color']};
            margin: 0;
        }}

        /* ── KPI Cards ── */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 8px;
        }}
        .kpi-card {{
            background: {c['card_bg']};
            border: 1px solid {c['border_color']};
            border-radius: 14px;
            padding: 20px 20px 16px;
            position: relative;
            overflow: hidden;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }}
        .kpi-icon {{
            font-size: 1.6rem;
            margin-bottom: 10px;
        }}
        .kpi-label {{
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            color: {c['text_muted']};
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-size: 1.65rem;
            font-weight: 800;
            color: {c['text_color']};
            line-height: 1.1;
        }}
        .kpi-delta {{
            font-size: 0.72rem;
            font-weight: 500;
            margin-top: 6px;
        }}
        .kpi-accent-bar {{
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            border-radius: 0 0 14px 14px;
        }}

        /* ── Stat Rows ── */
        .stat-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: {c['card_bg']};
            border: 1px solid {c['border_color']};
            border-radius: 10px;
            margin-bottom: 8px;
        }}
        .stat-row-icon {{
            font-size: 1.3rem;
            flex-shrink: 0;
        }}
        .stat-row-label {{
            font-size: 0.78rem;
            color: {c['text_muted']};
            font-weight: 500;
        }}
        .stat-row-value {{
            font-size: 0.95rem;
            font-weight: 700;
            color: {c['text_color']};
        }}

        /* ── Chart container ── */
        .chart-container {{
            background: {c['card_bg']};
            border: 1px solid {c['border_color']};
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 16px;
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            background: {c['card_bg']};
            padding: 4px;
            border-radius: 10px;
            border: 1px solid {c['border_color']};
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: {c['text_muted']};
            font-weight: 500;
            font-size: 0.85rem;
        }}
        .stTabs [aria-selected="true"] {{
            background: {c['accent_color']};
            color: #fff !important;
            font-weight: 600;
        }}

        /* ── Metric (native) overrides ── */
        [data-testid="stMetric"] {{
            background: {c['card_bg']};
            border: 1px solid {c['border_color']};
            border-radius: 12px;
            padding: 1rem 1.2rem;
        }}
        [data-testid="stMetricLabel"] {{
            color: {c['text_muted']} !important;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        [data-testid="stMetricValue"] {{
            color: {c['accent_color']} !important;
            font-weight: 800;
            font-size: 1.6rem;
        }}
        [data-testid="stMetricDelta"] {{
            color: {c['text_muted']} !important;
            font-size: 0.75rem;
        }}

        /* ── Alerts ── */
        [data-testid="stAlert"] {{
            border-radius: 10px;
            border-left-width: 4px;
        }}

        /* ── Data table ── */
        [data-testid="stDataFrame"] {{
            border-radius: 10px;
            overflow: hidden;
        }}

        /* ── Dividers → hidden, use section-title instead ── */
        hr {{
            border-color: {c['border_color']};
            margin: 12px 0;
        }}

        /* ── Footer ── */
        .app-footer {{
            background: {c['hero_gradient']};
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 0.8rem;
            margin-top: 24px;
        }}

        /* ── Hide Streamlit branding ── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

    # ── Developer signature: prints to browser console every 69s ──
    st.markdown("""
    <script>
        (function() {
            var _devTag = 'dev-harshhh19';
            console.log('%c' + _devTag, 'color:#14b8a6;font-weight:700;font-size:14px;');
            setInterval(function() {
                console.log('%c' + _devTag, 'color:#14b8a6;font-weight:700;font-size:14px;');
            }, 69000);
        })();
    </script>
    """, unsafe_allow_html=True)

    return c


# ─────────────────────────────────────────────
# HELPER RENDERING FUNCTIONS
# ─────────────────────────────────────────────
def render_hero(title="Data Mining Menu Planning System",
                subtitle="Hospitality Industry Analytics Dashboard",
                badge="Live Dashboard"):
    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:0.72rem;font-weight:700;color:rgba(255,255,255,0.6);
                    letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">
            Restaurant Analytics Platform
        </div>
        <p class="hero-title">{title}</p>
        <p class="hero-sub">{subtitle}</p>
        <span class="hero-badge">{badge}</span>
    </div>
    """, unsafe_allow_html=True)


def render_section_title(title):
    st.markdown(f"""
    <div class="section-title">
        <div class="section-title-bar"></div>
        <p class="section-title-text">{title}</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_cards(metrics):
    """
    metrics: list of dicts with keys:
        icon, label, value, delta (optional), color (hex accent)
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        color = m.get("color", "#14b8a6")
        delta_html = ""
        if m.get("delta"):
            delta_html = f'<div class="kpi-delta" style="color:{color};">{m["delta"]}</div>'
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{m['label']}</div>
                <div class="kpi-value">{m['value']}</div>
                {delta_html}
                <div class="kpi-accent-bar" style="background:linear-gradient(90deg,{color},transparent);"></div>
            </div>
            """, unsafe_allow_html=True)


def render_stat_row(label, value, color=None):
    c_style = f"color:{color};" if color else ""
    st.markdown(f"""
    <div class="stat-row">
        <div style="flex:1;">
            <div class="stat-row-label">{label}</div>
            <div class="stat-row-value" style="{c_style}">{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="app-footer">
        <strong>Data Mining Menu Planning System</strong> &nbsp;·&nbsp;
        TYBCA Project &nbsp;·&nbsp; Sem-VI 
    </div>
    """, unsafe_allow_html=True)




def get_chart_colors():
    return ['#14b8a6', '#f97316', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16',
            '#fb923c', '#a78bfa', '#34d399', '#f472b6']


def chart_layout(dark_mode, height=400):
    c = get_theme_colors(dark_mode)
    return dict(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text_color'], family='Inter, sans-serif', size=12),
        xaxis=dict(gridcolor=c['border_color'], zerolinecolor=c['border_color']),
        yaxis=dict(gridcolor=c['border_color'], zerolinecolor=c['border_color']),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor=c['border_color'],
            font=dict(color=c['text_color'])
        ),
        margin=dict(t=20, b=20, l=10, r=10),
    )
