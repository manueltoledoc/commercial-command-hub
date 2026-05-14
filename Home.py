import streamlit as st

st.set_page_config(
    page_title="Commercial Command Hub",
    page_icon="🧭",
    layout="wide"
)

# =====================================================
# ESTILOS GLOBALES
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
}

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER */

.hero-container {
    padding: 45px;
    border-radius: 24px;
    background: linear-gradient(135deg, #111827, #0F172A);
    border: 1px solid #1E3A8A;
    margin-bottom: 35px;
}

.hero-title {
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 20px;
    color: #93C5FD;
    margin-bottom: 0px;
}

/* MODULE CARDS */

.module-card {
    background: #111827;
    padding: 28px;
    border-radius: 22px;
    border: 1px solid #1E40AF;
    transition: 0.3s;
    min-height: 240px;
}

.module-card:hover {
    border: 1px solid #60A5FA;
    box-shadow: 0px 0px 25px rgba(59,130,246,0.25);
}

.module-title {
    color: white;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 14px;
}

.module-text {
    color: #CBD5E1;
    font-size: 16px;
    line-height: 1.5;
}

/* FOOTER */

.footer {
    color: #64748B;
    text-align: center;
    margin-top: 50px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero-container">
    <div class="hero-title">
        Commercial Command Hub
    </div>
    <div class="hero-subtitle">
        Intelligent Commercial Infrastructure Platform
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# INTRO
# =====================================================

st.markdown(
    """
    <span style='color:#CBD5E1; font-size:18px'>
    Centralized commercial intelligence, logistics visibility,
    sales performance analytics and operational forecasting.
    </span>
    """,
    unsafe_allow_html=True
)

st.write("")

# =====================================================
# MODULE GRID
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">🚢 Importaciones</div>
            <div class="module-text">
            Control logístico de OCC, ORP, ODI, PI, shipping,
            ETA, atrasos y seguimiento operacional.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/1_Importaciones.py",
            label="Open Module"
        )

    st.write("")

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">🧲 Sales Funnel</div>
            <div class="module-text">
            Gestión avanzada de oportunidades,
            pipeline comercial y forecast de ventas.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/2_Sales_Funnel.py",
            label="Open Module"
        )

with col2:

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">📦 Inventory Forecast</div>
            <div class="module-text">
            Proyección de demanda, stock crítico,
            consumo histórico y planificación.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/3_Inventory_Forecast.py",
            label="Open Module"
        )

    st.write("")

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">👥 KAM Performance</div>
            <div class="module-text">
            KPIs comerciales, conversión,
            productividad y desempeño de KAMs.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/4_KAM_Performance.py",
            label="Open Module"
        )

with col3:

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">📣 Marketing Intelligence</div>
            <div class="module-text">
            Attribution analytics, campaign performance,
            lead generation and ROAS visibility.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/5_Marketing_Intelligence.py",
            label="Open Module"
        )

    st.write("")

    with st.container(border=False):

        st.markdown("""
        <div class="module-card">
            <div class="module-title">🤖 AI Assistant</div>
            <div class="module-text">
            Intelligent operational assistant for
            commercial and strategic decision support.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link(
            "pages/6_AI_Assistant.py",
            label="Open Module"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
Commercial Command Hub · Executive Edition · v0.1
</div>
""", unsafe_allow_html=True)