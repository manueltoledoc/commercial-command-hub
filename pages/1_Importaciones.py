import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Importaciones | CCH", layout="wide")

st.title("Dash Importaciones")
st.caption("Seguimiento visual de ORP, ODI, PI, cliente, producto y estado logístico")

hoy = date.today()

data = [
    ["ORP-1001", "ODI-4501", "PI-C1-8891", "Clínica Los Andes", "Vetus E7", "Esperando PI", hoy + timedelta(days=35), "Verde"],
    ["ORP-1002", "ODI-4502", "PI-C1-8892", "Hospital Veterinario Sur", "BC-60R Vet", "Esperando pago SWIFT", hoy + timedelta(days=12), "Amarillo"],
    ["ORP-1003", "ODI-4503", "PI-C1-8893", "Universidad Central", "Veta 5 Plus", "Embarcada", hoy - timedelta(days=3), "Rojo"],
    ["ORP-1004", "ODI-4504", "PI-C1-8894", "Clínica San Martín", "VetXpert Cube", "En tránsito", hoy + timedelta(days=20), "Verde"],
    ["ORP-1005", "ODI-4505", "PI-C1-8895", "Centro Vet Norte", "DP-50 Vet", "Esperando embarque", hoy + timedelta(days=6), "Amarillo"],
]

df = pd.DataFrame(data, columns=[
    "ORP",
    "ODI",
    "PI",
    "CLIENTE",
    "PRODUCTO",
    "ESTADO",
    "ETA",
    "RIESGO"
])

def semaforo(riesgo):
    if riesgo == "Verde":
        return "🟢"
    elif riesgo == "Amarillo":
        return "🟡"
    elif riesgo == "Rojo":
        return "🔴"
    return "⚪"

df["SEMAFORO"] = df["RIESGO"].apply(semaforo)
df["DIAS_PARA_LLEGADA"] = df["ETA"].apply(lambda x: (x - hoy).days)
df["ETA"] = df["ETA"].apply(lambda x: x.strftime("%d-%m-%Y"))

st.subheader("Resumen general")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total ORP", len(df))
col2.metric("En plazo", (df["RIESGO"] == "Verde").sum())
col3.metric("En riesgo", (df["RIESGO"] == "Amarillo").sum())
col4.metric("Atrasadas", (df["RIESGO"] == "Rojo").sum())

st.divider()

st.subheader("Tablero de importaciones")

df_vista = df[
    [
        "SEMAFORO",
        "ORP",
        "ODI",
        "PI",
        "CLIENTE",
        "PRODUCTO",
        "ESTADO",
        "ETA",
        "DIAS_PARA_LLEGADA",
        "RIESGO",
    ]
]

st.dataframe(
    df_vista,
    use_container_width=True,
    hide_index=True
)