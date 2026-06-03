import numpy as np
import numpy_financial as npf
import pandas as pd
import streamlit as st
from io import BytesIO


# ---------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Viabilidad económica de proyectos",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Viabilidad económica de proyectos")
st.caption(
    "Aplicación docente para calcular flujos de caja, base imponible, impuestos, "
    "VAN, TIR, payback simple y payback descontado."
)


# ---------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------

def euro(x, decimals=2):
    """Formatea una cantidad monetaria en estilo español."""
    if pd.isna(x):
        return "—"
    return f"{x:,.{decimals}f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def percent(x, decimals=2):
    """Formatea una tasa en porcentaje."""
    if x is None or pd.isna(x):
        return "—"
    return f"{100 * x:.{decimals}f} %".replace(".", ",")


def calcular_payback(flujos):
    """
    Calcula el payback con interpolación lineal.
    flujos[0] corresponde al momento inicial.
    Devuelve el periodo de recuperación o None si no se recupera.
    """
    acumulado = flujos[0]

    if acumulado >= 0:
        return 0.0

    for i in range(1, len(flujos)):
        anterior = acumulado
        acumulado += flujos[i]

        if acumulado >= 0:
            if flujos[i] == 0:
                return float(i)
            fraccion = -anterior / flujos[i]
            return (i - 1) + fraccion

    return None


def calcular_metricas(flujos, tasa_descuento):
    """Calcula los principales indicadores financieros."""
    flujos_actualizados = [
        flujo / ((1 + tasa_descuento) ** i)
        for i, flujo in enumerate(flujos)
    ]

    van = sum(flujos_actualizados)

    try:
        tir = npf.irr(flujos)
        if tir is None or np.isnan(tir) or np.isinf(tir):
            tir = None
    except Exception:
        tir = None

    payback = calcular_payback(flujos)
    payback_desc = calcular_payback(flujos_actualizados)

    inversion_inicial = abs(flujos[0]) if flujos and flujos[0] < 0 else None
    valor_actual_flujos_positivos = sum(x for x in flujos_actualizados[1:] if x > 0)

    if inversion_inicial and inversion_inicial > 0:
        indice_rentabilidad = valor_actual_flujos_positivos / inversion_inicial
    else:
        indice_rentabilidad = None

    acumulados = np.cumsum(flujos)
    acumulados_desc = np.cumsum(flujos_actualizados)

    return {
        "flujos_actualizados": flujos_actualizados,
        "van": van,
        "tir": tir,
        "payback": payback,
        "payback_desc": payback_desc,
        "indice_rentabilidad": indice_rentabilidad,
        "exposicion_maxima": min(acumulados),
        "exposicion_maxima_desc": min(acumulados_desc),
    }


def texto_payback(valor):
    if valor is None:
        return "No se recupera"
    return f"{valor:.2f} periodos".replace(".", ",")


def dataframe_to_excel_bytes(df, resumen):
    """Genera un archivo Excel descargable."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Resultados por periodo", index=False)
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
    return output.getvalue()


# ---------------------------------------------------------------------
# Parámetros generales
# ---------------------------------------------------------------------

with st.sidebar:
    st.header("Parámetros generales")

    n_periodos = st.number_input(
        "Número de periodos",
        min_value=1,
        max_value=30,
        value=5,
        step=1,
        help="Normalmente serán años, pero también pueden ser trimestres, semestres, etc.",
    )

    inversion_inicial = st.number_input(
        "Inversión inicial / desembolso inicial (€)",
        min_value=0.0,
        value=100_000.0,
        step=5_000.0,
    )

    st.subheader("Tasa de descuento")

    tasa_libre_riesgo = st.number_input(
        "Tasa libre de riesgo (%)",
        value=3.0,
        step=0.25,
    ) / 100

    prima_riesgo = st.number_input(
        "Prima de riesgo (%)",
        value=5.0,
        step=0.25,
    ) / 100

    tasa_descuento = tasa_libre_riesgo + prima_riesgo

    st.info(f"Tasa de descuento usada: **{percent(tasa_descuento)}**")

    st.subheader("Fiscalidad")

    compensar_bases_negativas = st.checkbox(
        "Compensar bases imponibles negativas de periodos anteriores",
        value=False,
        help=(
            "Si se activa, las pérdidas fiscales de un periodo se acumulan "
            "y se compensan con bases positivas futuras."
        ),
    )

    impuesto_minimo_cero = st.checkbox(
        "No considerar impuestos negativos",
        value=True,
        help=(
            "Si se activa, cuando la base imponible es negativa no se genera "
            "un cobro fiscal. Es la opción docente más habitual."
        ),
    )


# ---------------------------------------------------------------------
# Tabla de datos de entrada
# ---------------------------------------------------------------------

st.subheader("1. Datos por periodo")

amortizacion_defecto = inversion_inicial / n_periodos if n_periodos > 0 else 0.0

datos_defecto = pd.DataFrame(
    {
        "Periodo": list(range(1, int(n_periodos) + 1)),
        "Ingresos (€)": [40_000.0 + 5_000.0 * i for i in range(int(n_periodos))],
        "Gastos de explotación (€)": [18_000.0 + 1_500.0 * i for i in range(int(n_periodos))],
        "Amortización contable (€)": [amortizacion_defecto for _ in range(int(n_periodos))],
        "Tipo de gravamen (%)": [25.0 for _ in range(int(n_periodos))],
        "Inversiones adicionales (€)": [0.0 for _ in range(int(n_periodos))],
        "Variación capital circulante (€)": [0.0 for _ in range(int(n_periodos))],
        "Valor residual / otros cobros (€)": [0.0 for _ in range(int(n_periodos))],
    }
)

st.write(
    "Edita directamente la tabla. La amortización reduce la base imponible, "
    "pero se suma de nuevo para obtener el flujo de caja porque no es una salida de caja."
)

datos = st.data_editor(
    datos_defecto,
    num_rows="fixed",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Periodo": st.column_config.NumberColumn("Periodo", disabled=True),
        "Ingresos (€)": st.column_config.NumberColumn(format="%.2f"),
        "Gastos de explotación (€)": st.column_config.NumberColumn(format="%.2f"),
        "Amortización contable (€)": st.column_config.NumberColumn(format="%.2f"),
        "Tipo de gravamen (%)": st.column_config.NumberColumn(format="%.2f"),
        "Inversiones adicionales (€)": st.column_config.NumberColumn(format="%.2f"),
        "Variación capital circulante (€)": st.column_config.NumberColumn(format="%.2f"),
        "Valor residual / otros cobros (€)": st.column_config.NumberColumn(format="%.2f"),
    },
)


# ---------------------------------------------------------------------
# Cálculos por periodo
# ---------------------------------------------------------------------

df = datos.copy()

columnas_numericas = [
    "Ingresos (€)",
    "Gastos de explotación (€)",
    "Amortización contable (€)",
    "Tipo de gravamen (%)",
    "Inversiones adicionales (€)",
    "Variación capital circulante (€)",
    "Valor residual / otros cobros (€)",
]

for col in columnas_numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

df["Base imponible antes de compensación (€)"] = (
    df["Ingresos (€)"]
    - df["Gastos de explotación (€)"]
    - df["Amortización contable (€)"]
)

bases_compensadas = []
bases_liquidables = []
impuestos = []
saldo_base_negativa = 0.0

for _, fila in df.iterrows():
    base = fila["Base imponible antes de compensación (€)"]
    tipo = fila["Tipo de gravamen (%)"] / 100

    base_compensada = 0.0

    if compensar_bases_negativas:
        if base < 0:
            saldo_base_negativa += abs(base)
            base_liquidable = 0.0 if impuesto_minimo_cero else base
        else:
            base_compensada = min(base, saldo_base_negativa)
            saldo_base_negativa -= base_compensada
            base_liquidable = base - base_compensada
    else:
        if impuesto_minimo_cero:
            base_liquidable = max(base, 0.0)
        else:
            base_liquidable = base

    impuesto = base_liquidable * tipo

    bases_compensadas.append(base_compensada)
    bases_liquidables.append(base_liquidable)
    impuestos.append(impuesto)

df["Base compensada de periodos anteriores (€)"] = bases_compensadas
df["Base imponible liquidable (€)"] = bases_liquidables
df["Impuesto de sociedades (€)"] = impuestos

df["Resultado después de impuestos (€)"] = (
    df["Base imponible antes de compensación (€)"]
    - df["Impuesto de sociedades (€)"]
)

df["Flujo de caja (€)"] = (
    df["Resultado después de impuestos (€)"]
    + df["Amortización contable (€)"]
    - df["Inversiones adicionales (€)"]
    - df["Variación capital circulante (€)"]
    + df["Valor residual / otros cobros (€)"]
)

flujos = [-float(inversion_inicial)] + df["Flujo de caja (€)"].tolist()

metricas = calcular_metricas(flujos, tasa_descuento)
metricas_sin_prima = calcular_metricas(flujos, tasa_libre_riesgo)

df["Flujo de caja actualizado (€)"] = metricas["flujos_actualizados"][1:]
df["Flujo de caja acumulado (€)"] = np.cumsum(df["Flujo de caja (€)"])
df["Flujo actualizado acumulado (€)"] = np.cumsum(df["Flujo de caja actualizado (€)"]) - inversion_inicial


# ---------------------------------------------------------------------
# Resultados principales
# ---------------------------------------------------------------------

st.subheader("2. Resultados principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("VAN", euro(metricas["van"]))
with col2:
    st.metric("TIR", percent(metricas["tir"]) if metricas["tir"] is not None else "No calculable")
with col3:
    st.metric("Payback simple", texto_payback(metricas["payback"]))
with col4:
    st.metric("Payback descontado", texto_payback(metricas["payback_desc"]))

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Tasa libre de riesgo", percent(tasa_libre_riesgo))
with col6:
    st.metric("Prima de riesgo", percent(prima_riesgo))
with col7:
    st.metric("Tasa de descuento", percent(tasa_descuento))
with col8:
    st.metric(
        "Índice de rentabilidad",
        "—" if metricas["indice_rentabilidad"] is None else f"{metricas['indice_rentabilidad']:.3f}".replace(".", ","),
    )

st.subheader("3. Tabla de cálculo")

columnas_salida = [
    "Periodo",
    "Ingresos (€)",
    "Gastos de explotación (€)",
    "Amortización contable (€)",
    "Base imponible antes de compensación (€)",
    "Base compensada de periodos anteriores (€)",
    "Base imponible liquidable (€)",
    "Tipo de gravamen (%)",
    "Impuesto de sociedades (€)",
    "Resultado después de impuestos (€)",
    "Inversiones adicionales (€)",
    "Variación capital circulante (€)",
    "Valor residual / otros cobros (€)",
    "Flujo de caja (€)",
    "Flujo de caja actualizado (€)",
    "Flujo de caja acumulado (€)",
    "Flujo actualizado acumulado (€)",
]

st.dataframe(
    df[columnas_salida],
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------------------
# Gráficas
# ---------------------------------------------------------------------

st.subheader("4. Gráficas")

graf_df = pd.DataFrame(
    {
        "Periodo": df["Periodo"],
        "Flujo de caja": df["Flujo de caja (€)"],
        "Flujo de caja actualizado": df["Flujo de caja actualizado (€)"],
        "Flujo de caja acumulado": df["Flujo de caja acumulado (€)"] - inversion_inicial,
        "Flujo actualizado acumulado": df["Flujo actualizado acumulado (€)"],
    }
).set_index("Periodo")

st.line_chart(graf_df)


# ---------------------------------------------------------------------
# Sensibilidad del VAN
# ---------------------------------------------------------------------

st.subheader("5. Sensibilidad del VAN")

tasas_sensibilidad = np.arange(0.00, 0.205, 0.01)

sensibilidad = pd.DataFrame(
    {
        "Tasa de descuento (%)": [100 * t for t in tasas_sensibilidad],
        "VAN (€)": [calcular_metricas(flujos, t)["van"] for t in tasas_sensibilidad],
    }
)

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    st.line_chart(
        sensibilidad.set_index("Tasa de descuento (%)")
    )

with col_s2:
    st.write("Comparación rápida:")
    st.write(f"- VAN con tasa libre de riesgo: **{euro(metricas_sin_prima['van'])}**")
    st.write(f"- VAN con prima de riesgo: **{euro(metricas['van'])}**")
    st.write(f"- Diferencia atribuible a la prima de riesgo: **{euro(metricas['van'] - metricas_sin_prima['van'])}**")
    st.write(f"- Exposición máxima de caja: **{euro(metricas['exposicion_maxima'])}**")


# ---------------------------------------------------------------------
# Resumen y descarga
# ---------------------------------------------------------------------

st.subheader("6. Resumen descargable")

resumen = pd.DataFrame(
    {
        "Indicador": [
            "Inversión inicial",
            "Tasa libre de riesgo",
            "Prima de riesgo",
            "Tasa de descuento",
            "VAN",
            "VAN sin prima de riesgo",
            "TIR",
            "Payback simple",
            "Payback descontado",
            "Índice de rentabilidad",
            "Exposición máxima de caja",
            "Exposición máxima de caja descontada",
        ],
        "Valor": [
            euro(inversion_inicial),
            percent(tasa_libre_riesgo),
            percent(prima_riesgo),
            percent(tasa_descuento),
            euro(metricas["van"]),
            euro(metricas_sin_prima["van"]),
            percent(metricas["tir"]) if metricas["tir"] is not None else "No calculable",
            texto_payback(metricas["payback"]),
            texto_payback(metricas["payback_desc"]),
            "—" if metricas["indice_rentabilidad"] is None else f"{metricas['indice_rentabilidad']:.3f}".replace(".", ","),
            euro(metricas["exposicion_maxima"]),
            euro(metricas["exposicion_maxima_desc"]),
        ],
    }
)

st.dataframe(resumen, use_container_width=True, hide_index=True)

excel_bytes = dataframe_to_excel_bytes(df[columnas_salida], resumen)

st.download_button(
    label="Descargar resultados en Excel",
    data=excel_bytes,
    file_name="viabilidad_economica_proyecto.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.divider()

with st.expander("Criterios de cálculo usados"):
    st.markdown(
        """
        - **Base imponible antes de compensación** = ingresos − gastos de explotación − amortización contable.
        - **Impuesto de sociedades** = base imponible liquidable × tipo de gravamen.
        - **Resultado después de impuestos** = base imponible antes de compensación − impuesto de sociedades.
        - **Flujo de caja** = resultado después de impuestos + amortización − inversiones adicionales − variación de capital circulante + valor residual u otros cobros.
        - **Flujo de caja actualizado** = flujo de caja / (1 + tasa de descuento)^periodo.
        - **VAN** = desembolso inicial negativo + suma de flujos actualizados.
        - **TIR** = tasa que hace que el VAN sea cero.
        - **Payback simple** = periodo en el que se recupera la inversión con flujos no actualizados.
        - **Payback descontado** = periodo en el que se recupera la inversión con flujos actualizados.
        """
    )
