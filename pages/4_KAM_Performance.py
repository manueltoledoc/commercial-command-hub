import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="KAM Performance",
    page_icon="📊",
    layout="wide"
)

st.title("📊 KAM Performance")
st.subheader("Ejemplo de rendimiento comercial - Carlos")

# -----------------------------
# Datos de ejemplo
# -----------------------------

data = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
    "Leads": [28, 35, 42, 50, 46, 58],
    "Oportunidades": [12, 18, 22, 25, 21, 30],
    "Cotizaciones": [8, 14, 18, 20, 17, 24],
    "Ventas": [2, 4, 5, 6, 5, 8],
    "Venta_CLP": [8500000, 17500000, 23000000, 28500000, 24000000, 39000000],
    "Meta_CLP": [20000000, 22000000, 25000000, 28000000, 30000000, 35000000]
}

df = pd.DataFrame(data)

df["Conversión Lead a Venta (%)"] = (df["Ventas"] / df["Leads"] * 100).round(1)
df["Cumplimiento Meta (%)"] = (df["Venta_CLP"] / df["Meta_CLP"] * 100).round(1)

# -----------------------------
# KPIs principales
# -----------------------------

total_leads = df["Leads"].sum()
total_oportunidades = df["Oportunidades"].sum()
total_ventas = df["Ventas"].sum()
total_venta_clp = df["Venta_CLP"].sum()
total_meta = df["Meta_CLP"].sum()
cumplimiento_total = total_venta_clp / total_meta * 100
conversion_total = total_ventas / total_leads * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Leads", f"{total_leads}")
col2.metric("Oportunidades", f"{total_oportunidades}")
col3.metric("Ventas cerradas", f"{total_ventas}")
col4.metric("Venta acumulada", f"${total_venta_clp:,.0f}".replace(",", "."))
col5.metric("Cumplimiento meta", f"{cumplimiento_total:.1f}%")

st.divider()

# -----------------------------
# Tabla resumen
# -----------------------------

st.subheader("Resumen mensual")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Gráficos
# -----------------------------

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Venta mensual vs meta")

    fig_venta = px.bar(
        df,
        x="Mes",
        y=["Venta_CLP", "Meta_CLP"],
        barmode="group",
        text_auto=True,
        labels={
            "value": "CLP",
            "variable": "Indicador"
        }
    )

    st.plotly_chart(fig_venta, use_container_width=True)

with col_b:
    st.subheader("Cumplimiento de meta (%)")

    fig_cumplimiento = px.line(
        df,
        x="Mes",
        y="Cumplimiento Meta (%)",
        markers=True,
        text="Cumplimiento Meta (%)"
    )

    fig_cumplimiento.update_traces(textposition="top center")
    st.plotly_chart(fig_cumplimiento, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Embudo comercial")

    funnel_data = pd.DataFrame({
        "Etapa": ["Leads", "Oportunidades", "Cotizaciones", "Ventas"],
        "Cantidad": [
            total_leads,
            total_oportunidades,
            df["Cotizaciones"].sum(),
            total_ventas
        ]
    })

    fig_funnel = px.funnel(
        funnel_data,
        x="Cantidad",
        y="Etapa"
    )

    st.plotly_chart(fig_funnel, use_container_width=True)

with col_d:
    st.subheader("Conversión Lead → Venta")

    fig_conversion = px.bar(
        df,
        x="Mes",
        y="Conversión Lead a Venta (%)",
        text="Conversión Lead a Venta (%)"
    )

    st.plotly_chart(fig_conversion, use_container_width=True)

st.divider()

# -----------------------------
# Evaluación simple del KAM
# -----------------------------

st.subheader("Evaluación ejecutiva")

if cumplimiento_total >= 100:
    st.success("Carlos está sobre la meta comercial acumulada.")
elif cumplimiento_total >= 80:
    st.warning("Carlos está cerca de la meta, pero requiere seguimiento.")
else:
    st.error("Carlos está bajo la meta acumulada. Se recomienda revisar pipeline y actividades comerciales.")

st.write(f"""
**Carlos** registra una venta acumulada de **${total_venta_clp:,.0f} CLP**, 
con un cumplimiento total de **{cumplimiento_total:.1f}%** sobre su meta asignada.

Su conversión acumulada desde lead a venta es de **{conversion_total:.1f}%**.
""".replace(",", "."))