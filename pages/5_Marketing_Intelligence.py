import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Evaluación de Campaña", layout="wide")

BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "RENDIMIENTO_ABRIL.xlsx"

@st.cache_data(ttl=5)
def cargar_excel(path):
    df = pd.read_excel(path, sheet_name=0)
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )
    return df

if st.button("Actualizar datos desde Excel"):
    st.cache_data.clear()

df = cargar_excel(EXCEL_PATH)
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

# =========================
# CSS DARK MODE
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617 0%, #071426 55%, #0f172a 100%);
    color: white !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

html, body, [class*="css"] {
    color: white !important;
}

label, p, span, div {
    color: white !important;
}

h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

[data-testid="stMetricLabel"] {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

[data-testid="stMetricDelta"] {
    color: #38bdf8 !important;
}

[data-testid="stMarkdownContainer"] {
    color: white !important;
}

[data-testid="stCaptionContainer"] {
    color: #cbd5e1 !important;
}

.card {
    background: rgba(15, 23, 42, 0.94);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
    min-height: 125px;
}

.metric-title {
    color: #ffffff !important;
    font-size: 13px;
    font-weight: 700;
}

.metric-value {
    color: #ffffff !important;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.metric-sub {
    color: #38bdf8 !important;
    font-size: 13px;
    margin-top: 6px;
}

hr {
    border-color: rgba(148, 163, 184, 0.25);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("Evaluación de Campaña")
st.markdown(f"### Campaña: **{campana}**")
st.markdown("Análisis integral de desempeño comercial, funnel, revenue e insights.")

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4, c5, c6 = st.columns(6)

cards = [
    ("Leads Meta", leads_meta, "Informe KONA Mkt"),
    ("Leads BoldKnight", leads_bold, f"{conv_meta_bold:.1%} de Meta"),
    ("Contactos", contactos, f"{conv_bold_contactos:.1%} de BoldKnight"),
    ("Agendamientos", agendamientos, f"{conv_contacto_agenda:.1%} de contactos"),
    ("En Cierre", en_cierre, "Pipeline activo"),
    ("Revenue", clp(revenue), "CLP generado"),
]

for col, (title, value, sub) in zip([c1, c2, c3, c4, c5, c6], cards):
    with col:
        display_value = int(value) if isinstance(value, float) else value
        st.markdown(f"""
        <div class="card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{display_value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# =========================
# FUNNEL / INDICADORES / REVENUE
# =========================
left, mid, right = st.columns([2.2, 1.2, 1.4])

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
            "#22c55e",
            "#8b5cf6",
            "#f59e0b",
            "#14b8a6",
            "#16a34a"
        ]}
    ))

    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10)
    )

    fig.update_traces(
        textfont=dict(color="white", size=14),
        connector=dict(line=dict(color="rgba(255,255,255,0.5)"))
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with mid:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Indicadores Clave")

    st.metric("Inversión", clp(inversion))
    st.metric("ROAS", f"{roas:.1f}x")
    st.metric("Costo por Contacto", clp(cpl))
    st.metric("Costo por Agendamiento", clp(cpa))
    st.metric("Costo por Oportunidad", clp(cpo))
    st.metric("Costo por Venta", clp(cpv))
    st.metric("Ticket Promedio", clp(ticket))

    st.markdown('</div>', unsafe_allow_html=True)

with right:
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
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="CLP",
        xaxis=dict(color="white"),
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.15)")
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# =========================
# SEGUNDA FILA
# =========================
col_a, col_b, col_c = st.columns([1.2, 1.4, 1.4])

with col_a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Distribución por Etapa")

    fig_donut = go.Figure(go.Pie(
        labels=[
            "Leads Meta",
            "Leads BoldKnight",
            "Contactos",
            "Agendamientos",
            "Oportunidades",
            "En Cierre",
            "Ventas"
        ],
        values=[
            leads_meta,
            leads_bold,
            contactos,
            agendamientos,
            oportunidades,
            en_cierre,
            ventas
        ],
        hole=0.55,
        textfont=dict(color="white"),
        marker=dict(line=dict(color="#020617", width=2))
    ))

    fig_donut.update_layout(
        height=330,
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
    st.subheader("Pipeline")

    p1, p2 = st.columns(2)
    p3, p4 = st.columns(2)

    p1.metric("Pipeline generado", clp(pipeline_potencial))
    p2.metric("Pipeline en cierre", clp(pipeline_en_cierre))
    p3.metric("Ventas cerradas", int(ventas))
    p4.metric("Revenue cerrado", clp(revenue))

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

# =========================
# INSIGHTS
# =========================
col_i, col_l = st.columns([1.5, 1])

with col_i:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Insights Comerciales")

    st.markdown(f"""
- La campaña generó **{int(leads_meta)} leads desde Meta** y **{int(leads_bold)} leads registrados en BoldKnight**.
- Se consolidaron **{int(contactos)} contactos comerciales efectivos**.
- Se lograron **{int(agendamientos)} agendamientos**, equivalentes a **{conv_contacto_agenda:.1%}** sobre contactos.
- Se generaron **{int(oportunidades)} oportunidades comerciales reales**.
- La campaña ya generó **{int(ventas)} venta cerrada** por **{clp(revenue)}**.
- El ROAS actual es de **{roas:.1f}x**, con una inversión de **{clp(inversion)}**.
- Existen **{int(en_cierre)} oportunidades en cierre**, por lo que el resultado final aún puede aumentar.
- Las ventas perdidas por falta de financiamiento deben registrarse como **demanda no capturada**, no como falta de interés comercial.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

with col_l:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Fricciones Comerciales")

    motivos = pd.DataFrame({
        "Motivo": ["Falta de financiamiento", "En cierre", "Evaluación / seguimiento"],
        "Casos": [2, int(en_cierre), max(int(oportunidades - en_cierre - ventas), 0)]
    })

    fig_loss = go.Figure(go.Bar(
        x=motivos["Casos"],
        y=motivos["Motivo"],
        orientation="h",
        text=motivos["Casos"],
        textposition="outside",
        marker_color=["#ef4444", "#f59e0b", "#38bdf8"],
        textfont=dict(color="white", size=14)
    ))

    fig_loss.update_layout(
        height=310,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(color="white", gridcolor="rgba(255,255,255,0.15)"),
        yaxis=dict(color="white")
    )

    st.plotly_chart(fig_loss, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Los datos se leen desde RENDIMIENTO_ABRIL.xlsx. Para actualizar en Streamlit Cloud: editar Excel, guardar, git add, commit y push.")