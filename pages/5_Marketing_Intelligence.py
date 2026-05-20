import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Evaluación de Campaña", layout="wide")

BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "RENDIMIENTO_ABRIL.xlsx"

@st.cache_data(ttl=5)
def cargar_excel(path):
    df = pd.read_excel(path, sheet_name="Datos KPI")
    df.columns = df.columns.str.replace("\n", " ", regex=False).str.strip()
    return df

@st.cache_data(ttl=5)
def cargar_insights(path):
    insights_df = pd.read_excel(path, sheet_name="Insights")
    insights_df.columns = insights_df.columns.str.replace("\n", " ", regex=False).str.strip()
    if "Insight" not in insights_df.columns:
        return []
    return (
        insights_df["Insight"]
        .iloc[:14]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .tolist()
    )

@st.cache_data(ttl=5)
def cargar_crm(path):
    crm_df = pd.read_excel(path, sheet_name="Referencias_CRM")
    crm_df.columns = crm_df.columns.str.strip()
    return crm_df

if st.button("Actualizar datos desde Excel"):
    st.cache_data.clear()

df = cargar_excel(EXCEL_PATH)
insights = cargar_insights(EXCEL_PATH)
crm_df = cargar_crm(EXCEL_PATH)

row = df.iloc[0]

def get_num(col, default=0):
    try:
        value = row.get(col, default)
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except Exception:
        return default

def safe_div(a, b):
    return a / b if b else 0

def clp(x):
    return f"${x:,.0f}".replace(",", ".")

campana = row.get("Campaña", "Campaña sin nombre")

leads_meta = get_num("Leads Contactos Meta (Informe KONA Mkt)")
leads_bold = get_num("Leads BoldKnight")
contactos = get_num("Contactos")
agendamientos = get_num("Appointment Count")
oportunidades = get_num("Oportunidades CRM arquimed")
en_cierre = get_num("En Cierre")
ventas = get_num("Ventas")
revenue = get_num("Revenue")
inversion = get_num("Inversion")

if oportunidades == 0:
    oportunidades = en_cierre + ventas

cpl = safe_div(inversion, contactos)
cpa = safe_div(inversion, agendamientos)
cpo = safe_div(inversion, oportunidades)
cpv = safe_div(inversion, ventas)
roas = safe_div(revenue, inversion)
ticket = safe_div(revenue, ventas)

conv_meta_bold = safe_div(leads_bold, leads_meta)
conv_bold_contactos = safe_div(contactos, leads_bold)
conv_contacto_agenda = safe_div(agendamientos, contactos)

ticket_ref = ticket if ticket else 15_500_000
pipeline_potencial = oportunidades * ticket_ref
pipeline_en_cierre = en_cierre * ticket_ref

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #0b3b66 0%, #061526 32%, #020617 100%);
    color: #ffffff !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1550px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06243d 0%, #03111f 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.25);
}

html, body, [class*="css"], label, p, span, div {
    color: #ffffff !important;
}

h1, h2, h3, h4, h5 {
    color: #ffffff !important;
    letter-spacing: -0.03em;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

.card {
    background: linear-gradient(145deg, rgba(8, 32, 56, 0.96), rgba(4, 18, 34, 0.96));
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.35);
}

.kpi-card {
    min-height: 150px;
    text-align: center;
}

.metric-title {
    color: #e0f2fe !important;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}

.metric-value {
    color: #38bdf8 !important;
    font-size: 34px;
    font-weight: 900;
}

.metric-sub {
    color: #86efac !important;
    font-size: 13px;
    margin-top: 8px;
}

.green-value {
    color: #86efac !important;
}

.blue-value {
    color: #38bdf8 !important;
}

.purple-value {
    color: #a78bfa !important;
}

.orange-value {
    color: #fbbf24 !important;
}

.crm-table-title {
    font-size: 24px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 8px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 16px;
    overflow: hidden;
}

button[kind="secondary"] {
    background: linear-gradient(90deg, #075985, #2563eb) !important;
    border: 1px solid rgba(125, 211, 252, 0.5) !important;
    color: white !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("# Evaluación de Campaña")
st.markdown(f"### Campaña: <span style='color:#38bdf8'>{campana}</span>", unsafe_allow_html=True)
st.markdown("Command Center de desempeño comercial, revenue intelligence y trazabilidad CRM.")

# KPI CARDS
c1, c2, c3, c4, c5, c6 = st.columns(6)

cards = [
    ("Leads Meta", leads_meta, "Informe KONA Mkt", "blue-value"),
    ("Leads BoldKnight", leads_bold, f"{conv_meta_bold:.1%} de Meta", "blue-value"),
    ("Contactos", contactos, f"{conv_bold_contactos:.1%} de BoldKnight", "green-value"),
    ("Agendamientos", agendamientos, f"{conv_contacto_agenda:.1%} de contactos", "purple-value"),
    ("En Cierre", en_cierre, "Pipeline activo", "orange-value"),
    ("Revenue", clp(revenue), "CLP generado", "green-value"),
]

for col, (title, value, sub, css_class) in zip([c1, c2, c3, c4, c5, c6], cards):
    with col:
        display_value = int(value) if isinstance(value, float) else value
        st.markdown(f"""
        <div class="card kpi-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value {css_class}">{display_value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# MAIN ROW
left, right = st.columns([1.45, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Funnel Comercial")

    fig = go.Figure(go.Funnel(
        y=[
            "Leads Meta",
            "Leads BoldKnight",
            "Contactos",
            "Agendamientos",
            "Oportunidades",
            "En Cierre",
            "Ventas"
        ],
        x=[
            leads_meta,
            leads_bold,
            contactos,
            agendamientos,
            oportunidades,
            en_cierre,
            ventas
        ],
        textinfo="value+percent previous",
        marker={"color": [
            "#2563eb",
            "#0ea5e9",
            "#14b8a6",
            "#8b5cf6",
            "#f59e0b",
            "#06b6d4",
            "#22c55e"
        ]}
    ))

    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10)
    )

    fig.update_traces(
        textfont=dict(color="white", size=15),
        connector=dict(line=dict(color="rgba(255,255,255,0.35)"))
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Indicadores Clave")

    st.metric("Inversión", clp(inversion))
    st.metric("ROAS", f"{roas:.2f}x")
    st.metric("Costo por Contacto", clp(cpl))
    st.metric("Costo por Agendamiento", clp(cpa))
    st.metric("Costo por Oportunidad", clp(cpo))
    st.metric("Costo por Venta", clp(cpv))
    st.metric("Ticket Promedio", clp(ticket))

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Inversión vs Revenue")

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["Inversión", "Revenue"],
        y=[inversion, revenue],
        text=[clp(inversion), clp(revenue)],
        textposition="outside",
        marker_color=["#2563eb", "#22c55e"],
        textfont=dict(color="white", size=14)
    ))

    fig_bar.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(gridcolor="rgba(255,255,255,0.12)")
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# SECOND ROW
col_a, col_b, col_c = st.columns([1.2, 1.25, 1.25])

with col_a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Distribución por Etapa")

    fig_donut = go.Figure(go.Pie(
        labels=["Meta", "BoldKnight", "Contactos", "Agendamientos", "OPP", "Cierre", "Ventas"],
        values=[leads_meta, leads_bold, contactos, agendamientos, oportunidades, en_cierre, ventas],
        hole=0.58,
        textfont=dict(color="white"),
        marker=dict(line=dict(color="#020617", width=2))
    ))

    fig_donut.update_layout(
        height=340,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(font=dict(color="white"))
    )

    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Pipeline Comercial")

    st.metric("Pipeline generado", clp(pipeline_potencial))
    st.metric("Pipeline en cierre", clp(pipeline_en_cierre))
    st.metric("Ventas cerradas", int(ventas))
    st.metric("Revenue cerrado", clp(revenue))

    st.markdown('</div>', unsafe_allow_html=True)

with col_c:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Proyección Ejecutiva")

    ventas_proy_min = max(ventas, round(oportunidades * 0.30))
    ventas_proy_max = max(ventas_proy_min, round(oportunidades * 0.50))
    rev_min = ventas_proy_min * ticket_ref
    rev_max = ventas_proy_max * ticket_ref

    st.metric("Ventas proyectadas", f"{int(ventas_proy_min)} - {int(ventas_proy_max)}")
    st.metric("Revenue proyectado", f"{clp(rev_min)} - {clp(rev_max)}")
    st.markdown("Proyección basada en oportunidades generadas y ticket promedio observado.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# INSIGHTS + FRICTIONS
col_i, col_l = st.columns([1.35, 1])

with col_i:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Insights Comerciales")

    if insights:
        for insight in insights:
            st.markdown(f"✅ {insight}")
    else:
        st.markdown("No existen insights cargados en la hoja Insights.")

    st.markdown('</div>', unsafe_allow_html=True)

with col_l:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fricciones Comerciales")

    motivos = pd.DataFrame({
        "Motivo": ["Falta financiamiento", "En cierre", "Seguimiento"],
        "Casos": [2, int(en_cierre), max(int(oportunidades - en_cierre - ventas), 0)]
    })

    fig_loss = go.Figure(go.Bar(
        x=motivos["Casos"],
        y=motivos["Motivo"],
        orientation="h",
        text=motivos["Casos"],
        textposition="outside",
        marker_color=["#ef4444", "#f59e0b", "#38bdf8"],
        textfont=dict(color="white")
    ))

    fig_loss.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.12)")
    )

    st.plotly_chart(fig_loss, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# CRM TABLE
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="crm-table-title">Referencias CRM</div>', unsafe_allow_html=True)
st.markdown("Trazabilidad operacional de oportunidades, OCC y cotizaciones asociadas a la campaña.")

if "Valor CLP" in crm_df.columns:
    crm_df["Valor CLP"] = crm_df["Valor CLP"].apply(
        lambda x: clp(x) if pd.notna(x) and isinstance(x, (int, float)) else x
    )

st.dataframe(crm_df, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

st.caption("Datos provenientes desde RENDIMIENTO_ABRIL.xlsx | Módulo Campaign Intelligence")