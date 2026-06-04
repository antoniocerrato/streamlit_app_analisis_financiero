from __future__ import annotations

from io import BytesIO
from typing import Optional

import numpy as np
import numpy_financial as npf
import pandas as pd
import streamlit as st


# =============================================================================
# Configuración de la página
# =============================================================================

st.set_page_config(
    page_title="Viabilidad económica de proyectos",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Viabilidad económica de proyectos")
st.caption(
    "Aplicación docente para calcular base imponible, impuestos, flujos de caja, "
    "VAN, TIR, payback, prima de riesgo y rotación del capital."
)


# =============================================================================
# Funciones auxiliares
# =============================================================================

def euro(valor: float | int | None, decimales: int = 2) -> str:
    """Devuelve una cantidad en euros con formato español."""
    if valor is None:
        return "—"
    try:
        if pd.isna(valor):
            return "—"
    except TypeError:
        pass

    return f"{float(valor):,.{decimales}f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def porcentaje(valor: float | int | None, decimales: int = 2) -> str:
    """Devuelve una tasa decimal como porcentaje con formato español."""
    if valor is None:
        return "—"
    try:
        if pd.isna(valor):
            return "—"
    except TypeError:
        pass

    return f"{100 * float(valor):.{decimales}f} %".replace(".", ",")


def numero(valor: float | int | None, decimales: int = 3) -> str:
    """Devuelve un número con formato español."""
    if valor is None:
        return "—"
    try:
        if pd.isna(valor):
            return "—"
    except TypeError:
        pass

    return f"{float(valor):,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_payback(flujos: list[float]) -> Optional[float]:
    """
    Calcula el periodo de recuperación con interpolación lineal.

    Parámetros
    ----------
    flujos:
        Lista de flujos de caja. El elemento 0 corresponde al momento inicial.

    Devuelve
    --------
    float | None
        Periodo de recuperación. Devuelve None si la inversión no se recupera.
    """
    acumulado = float(flujos[0])

    if acumulado >= 0:
        return 0.0

    for periodo in range(1, len(flujos)):
        acumulado_anterior = acumulado
        flujo_periodo = float(flujos[periodo])
        acumulado += flujo_periodo

        if acumulado >= 0:
            if flujo_periodo == 0:
                return float(periodo)
            fraccion = -acumulado_anterior / flujo_periodo
            return (periodo - 1) + fraccion

    return None


def texto_payback(valor: Optional[float]) -> str:
    """Formatea el payback."""
    if valor is None:
        return "No se recupera"
    return f"{valor:.2f} periodos".replace(".", ",")


def calcular_metricas(flujos: list[float], tasa_descuento: float) -> dict:
    """Calcula VAN, TIR, payback simple, payback descontado e indicadores auxiliares."""
    flujos_actualizados = [
        flujo / ((1 + tasa_descuento) ** periodo)
        for periodo, flujo in enumerate(flujos)
    ]

    van = float(sum(flujos_actualizados))

    try:
        tir = npf.irr(flujos)
        if tir is None or np.isnan(tir) or np.isinf(tir):
            tir = None
        else:
            tir = float(tir)
    except Exception:
        tir = None

    payback = calcular_payback(flujos)
    payback_descontado = calcular_payback(flujos_actualizados)

    inversion_inicial = abs(flujos[0]) if flujos and flujos[0] < 0 else None
    valor_actual_flujos_positivos = sum(x for x in flujos_actualizados[1:] if x > 0)

    indice_rentabilidad = None
    if inversion_inicial and inversion_inicial > 0:
        indice_rentabilidad = valor_actual_flujos_positivos / inversion_inicial

    acumulado = np.cumsum(flujos)
    acumulado_descontado = np.cumsum(flujos_actualizados)

    return {
        "flujos_actualizados": flujos_actualizados,
        "van": van,
        "tir": tir,
        "payback": payback,
        "payback_descontado": payback_descontado,
        "indice_rentabilidad": indice_rentabilidad,
        "exposicion_maxima": float(min(acumulado)),
        "exposicion_maxima_descontada": float(min(acumulado_descontado)),
    }


def generar_excel(df_resultados: pd.DataFrame, df_resumen: pd.DataFrame) -> bytes:
    """Genera un archivo Excel descargable con resultados y resumen."""
    salida = BytesIO()
    with pd.ExcelWriter(salida, engine="openpyxl") as writer:
        df_resultados.to_excel(writer, sheet_name="Resultados por periodo", index=False)
        df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
    return salida.getvalue()


# =============================================================================
# Barra lateral
# =============================================================================

with st.sidebar:
    st.header("Parámetros generales")

    n_periodos = int(
        st.number_input(
            "Número de periodos",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
            help="Normalmente serán años, aunque también podrían ser trimestres o semestres.",
        )
    )

    inversion_inicial = float(
        st.number_input(
            "Inversión inicial / desembolso inicial (€)",
            min_value=0.0,
            value=200_000.0,
            step=5_000.0,
        )
    )

    st.subheader("Tasa de descuento")

    tasa_libre_riesgo = (
        float(
            st.number_input(
                "Tasa libre de riesgo (%)",
                value=3.0,
                step=0.25,
            )
        )
        / 100
    )

    prima_riesgo = (
        float(
            st.number_input(
                "Prima de riesgo (%)",
                value=5.0,
                step=0.25,
            )
        )
        / 100
    )

    tasa_descuento = tasa_libre_riesgo + prima_riesgo
    st.info(f"Tasa de descuento utilizada: **{porcentaje(tasa_descuento)}**")

    st.subheader("Fiscalidad")

    compensar_bases_negativas = st.checkbox(
        "Compensar bases imponibles negativas",
        value=False,
        help=(
            "Si se activa, las bases imponibles negativas se acumulan y se compensan "
            "con bases positivas de periodos posteriores."
        ),
    )

    impuesto_minimo_cero = st.checkbox(
        "No considerar impuestos negativos",
        value=True,
        help=(
            "Si se activa, una base imponible negativa no genera un cobro fiscal. "
            "Es la hipótesis más sencilla para ejercicios docentes."
        ),
    )


# =============================================================================
# Datos de entrada
# =============================================================================

st.subheader("1. Datos por periodo")

amortizacion_defecto = inversion_inicial / n_periodos if n_periodos else 0.0

datos_defecto = pd.DataFrame(
    {
        "Periodo": list(range(1, n_periodos + 1)),
        "Ingresos (€)": [110_000.0 for _ in range(n_periodos)],
        "Gastos de explotación (€)": [55_000.0 for _ in range(n_periodos)],
        "Amortización contable (€)": [amortizacion_defecto for _ in range(n_periodos)],
        "Tipo de gravamen (%)": [25.0 for _ in range(n_periodos)],
        "Inversiones adicionales (€)": [0.0 for _ in range(n_periodos)],
        "Variación capital circulante (€)": [0.0 for _ in range(n_periodos)],
        "Valor residual / otros cobros (€)": [
            0.0 if i < n_periodos - 1 else 30_000.0
            for i in range(n_periodos)
        ],
    }
)

st.write(
    "Edita la tabla para construir el caso. La amortización se utiliza para calcular "
    "la base imponible y el impuesto, pero el flujo de caja se calcula restando "
    "directamente los impuestos pagados."
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


# =============================================================================
# Cálculo fiscal
# =============================================================================

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

for columna in columnas_numericas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce").fillna(0.0)

df["Base imponible antes de compensación (€)"] = (
    df["Ingresos (€)"]
    - df["Gastos de explotación (€)"]
    - df["Amortización contable (€)"]
)

bases_compensadas = []
bases_liquidables = []
impuestos = []
saldo_bases_negativas = 0.0

for _, fila in df.iterrows():
    base = float(fila["Base imponible antes de compensación (€)"])
    tipo = float(fila["Tipo de gravamen (%)"]) / 100

    base_compensada = 0.0

    if compensar_bases_negativas:
        if base < 0:
            saldo_bases_negativas += abs(base)
            base_liquidable = 0.0 if impuesto_minimo_cero else base
        else:
            base_compensada = min(base, saldo_bases_negativas)
            saldo_bases_negativas -= base_compensada
            base_liquidable = base - base_compensada
    else:
        base_liquidable = max(base, 0.0) if impuesto_minimo_cero else base

    impuesto = base_liquidable * tipo

    bases_compensadas.append(base_compensada)
    bases_liquidables.append(base_liquidable)
    impuestos.append(impuesto)

df["Base compensada de periodos anteriores (€)"] = bases_compensadas
df["Base imponible liquidable (€)"] = bases_liquidables
df["Impuestos pagados (€)"] = impuestos


# =============================================================================
# Flujo de caja modificado
# =============================================================================

# Formulación docente adoptada:
#
# FC_t = Ingresos_t
#        - Gastos de explotación_t
#        - Impuestos pagados_t
#        - Inversiones adicionales_t
#        - Variación de capital circulante_t
#        + Valor residual u otros cobros_t
#
# La amortización NO se resta aquí, porque no es una salida real de caja.
# Sí se usa antes para calcular la base imponible y, por tanto, los impuestos.

df["Flujo de caja operativo después de impuestos (€)"] = (
    df["Ingresos (€)"]
    - df["Gastos de explotación (€)"]
    - df["Impuestos pagados (€)"]
)

df["Flujo de caja (€)"] = (
    df["Flujo de caja operativo después de impuestos (€)"]
    - df["Inversiones adicionales (€)"]
    - df["Variación capital circulante (€)"]
    + df["Valor residual / otros cobros (€)"]
)

df["Resultado contable después de impuestos (€)"] = (
    df["Base imponible antes de compensación (€)"]
    - df["Impuestos pagados (€)"]
)


# =============================================================================
# Métricas
# =============================================================================

flujos = [-float(inversion_inicial)] + df["Flujo de caja (€)"].tolist()

metricas = calcular_metricas(flujos, tasa_descuento)
metricas_sin_prima = calcular_metricas(flujos, tasa_libre_riesgo)

df["Flujo de caja actualizado (€)"] = metricas["flujos_actualizados"][1:]
df["Flujo de caja acumulado (€)"] = np.cumsum(df["Flujo de caja (€)"]) - inversion_inicial
df["Flujo actualizado acumulado (€)"] = np.cumsum(df["Flujo de caja actualizado (€)"]) - inversion_inicial

ingresos_totales = float(df["Ingresos (€)"].sum())
ingresos_medios = float(df["Ingresos (€)"].mean())
rotacion_media = ingresos_medios / inversion_inicial if inversion_inicial > 0 else None
rotacion_acumulada = ingresos_totales / inversion_inicial if inversion_inicial > 0 else None


# =============================================================================
# Visualización de resultados
# =============================================================================

st.subheader("2. Resultados principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("VAN", euro(metricas["van"]))
with col2:
    st.metric("TIR", porcentaje(metricas["tir"]) if metricas["tir"] is not None else "No calculable")
with col3:
    st.metric("Payback simple", texto_payback(metricas["payback"]))
with col4:
    st.metric("Payback descontado", texto_payback(metricas["payback_descontado"]))

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Tasa de descuento", porcentaje(tasa_descuento))
with col6:
    st.metric("Prima de riesgo", porcentaje(prima_riesgo))
with col7:
    st.metric("Rotación media anual", numero(rotacion_media))
with col8:
    st.metric("Rotación acumulada", numero(rotacion_acumulada))

col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric(
        "Índice de rentabilidad",
        numero(metricas["indice_rentabilidad"]),
    )
with col10:
    st.metric("VAN sin prima de riesgo", euro(metricas_sin_prima["van"]))
with col11:
    st.metric("Exposición máxima de caja", euro(metricas["exposicion_maxima"]))
with col12:
    st.metric("Ingresos acumulados", euro(ingresos_totales))


# =============================================================================
# Tabla de cálculo
# =============================================================================

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
    "Impuestos pagados (€)",
    "Resultado contable después de impuestos (€)",
    "Flujo de caja operativo después de impuestos (€)",
    "Inversiones adicionales (€)",
    "Variación capital circulante (€)",
    "Valor residual / otros cobros (€)",
    "Flujo de caja (€)",
    "Flujo de caja actualizado (€)",
    "Flujo de caja acumulado (€)",
    "Flujo actualizado acumulado (€)",
]

st.dataframe(df[columnas_salida], use_container_width=True, hide_index=True)


# =============================================================================
# Gráficas
# =============================================================================

st.subheader("4. Gráficas")

grafico = pd.DataFrame(
    {
        "Periodo": df["Periodo"],
        "Flujo de caja": df["Flujo de caja (€)"],
        "Flujo de caja actualizado": df["Flujo de caja actualizado (€)"],
        "Flujo de caja acumulado": df["Flujo de caja acumulado (€)"],
        "Flujo actualizado acumulado": df["Flujo actualizado acumulado (€)"],
    }
).set_index("Periodo")

st.line_chart(grafico)


# =============================================================================
# Sensibilidad
# =============================================================================

st.subheader("5. Sensibilidad del VAN")

tasas = np.arange(0.00, 0.205, 0.01)
sensibilidad = pd.DataFrame(
    {
        "Tasa de descuento (%)": [100 * tasa for tasa in tasas],
        "VAN (€)": [calcular_metricas(flujos, tasa)["van"] for tasa in tasas],
    }
)

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    st.line_chart(sensibilidad.set_index("Tasa de descuento (%)"))

with col_s2:
    st.write("Comparación:")
    st.write(f"- VAN con tasa libre de riesgo: **{euro(metricas_sin_prima['van'])}**")
    st.write(f"- VAN con prima de riesgo: **{euro(metricas['van'])}**")
    st.write(
        "- Efecto de aplicar la prima de riesgo: "
        f"**{euro(metricas['van'] - metricas_sin_prima['van'])}**"
    )


# =============================================================================
# Resumen y descarga
# =============================================================================

st.subheader("6. Resumen descargable")

resumen = pd.DataFrame(
    {
        "Indicador": [
            "Inversión inicial",
            "Tasa libre de riesgo",
            "Prima de riesgo",
            "Tasa de descuento",
            "Ingresos acumulados",
            "Rotación media anual del capital",
            "Rotación acumulada del capital",
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
            porcentaje(tasa_libre_riesgo),
            porcentaje(prima_riesgo),
            porcentaje(tasa_descuento),
            euro(ingresos_totales),
            numero(rotacion_media),
            numero(rotacion_acumulada),
            euro(metricas["van"]),
            euro(metricas_sin_prima["van"]),
            porcentaje(metricas["tir"]) if metricas["tir"] is not None else "No calculable",
            texto_payback(metricas["payback"]),
            texto_payback(metricas["payback_descontado"]),
            numero(metricas["indice_rentabilidad"]),
            euro(metricas["exposicion_maxima"]),
            euro(metricas["exposicion_maxima_descontada"]),
        ],
    }
)

st.dataframe(resumen, use_container_width=True, hide_index=True)

excel_bytes = generar_excel(df[columnas_salida], resumen)

st.download_button(
    label="Descargar resultados en Excel",
    data=excel_bytes,
    file_name="viabilidad_economica_proyecto.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)


# =============================================================================
# Criterios de cálculo usados
# =============================================================================

st.divider()

with st.expander("Criterios de cálculo usados"):
    st.markdown(
        """
        ### Base imponible

        La base imponible se calcula como:

        \[
        BI_t = Ingresos_t - Gastos_t - Amortización_t
        \]

        La amortización se resta aquí porque es un gasto contable fiscalmente relevante.

        ### Impuestos pagados

        \[
        Impuestos_t = BI_{liquidable,t} \\times TipoGravamen_t
        \]

        Si se activa la opción correspondiente, las bases imponibles negativas pueden
        compensarse con bases positivas de periodos posteriores.

        ### Flujo de caja

        En esta aplicación se utiliza la formulación directa:

        \[
        FC_t = Ingresos_t - Gastos_t - Impuestos_t - InversionesAdicionales_t - \Delta CC_t + ValorResidual_t
        \]

        La amortización no se resta directamente en el flujo de caja, porque no es una
        salida real de dinero. Su efecto aparece de forma indirecta al reducir los impuestos.

        ### VAN

        \[
        VAN = -I_0 + \sum_{t=1}^{n} \\frac{FC_t}{(1+k)^t}
        \]

        ### TIR

        La TIR es la tasa de descuento que hace que el VAN sea cero.

        ### Payback simple y descontado

        El payback simple usa flujos no actualizados. El payback descontado usa flujos
        actualizados mediante la tasa de descuento.
        """
    )
