from __future__ import annotations

import numpy as np
import pandas as pd


COLUMNAS_ENTRADA = [
    "Periodo",
    "Ingresos (€)",
    "Gastos de explotación (€)",
    "Amortización contable (€)",
    "Tipo de gravamen (%)",
    "Inversiones adicionales (€)",
    "Variación capital circulante (€)",
    "Valor residual / otros cobros (€)",
]

MODELO_AMORTIZACION_MANUAL = "Manual"
MODELO_AMORTIZACION_LINEAL = "Lineal"
MODELO_AMORTIZACION_DEGRESIVA = "Degresiva doble"
MODELO_AMORTIZACION_DIGITOS = "Suma de dígitos"
MODELOS_AMORTIZACION = (
    MODELO_AMORTIZACION_MANUAL,
    MODELO_AMORTIZACION_LINEAL,
    MODELO_AMORTIZACION_DEGRESIVA,
    MODELO_AMORTIZACION_DIGITOS,
)


def crear_datos_defecto(n_periodos: int, inversion_inicial: float) -> pd.DataFrame:
    """Crea una tabla docente inicial coherente con el número de periodos."""
    amortizacion = inversion_inicial / n_periodos if n_periodos else 0.0
    return pd.DataFrame(
        {
            "Periodo": list(range(1, n_periodos + 1)),
            "Ingresos (€)": [110_000.0 for _ in range(n_periodos)],
            "Gastos de explotación (€)": [55_000.0 for _ in range(n_periodos)],
            "Amortización contable (€)": [amortizacion for _ in range(n_periodos)],
            "Tipo de gravamen (%)": [25.0 for _ in range(n_periodos)],
            "Inversiones adicionales (€)": [0.0 for _ in range(n_periodos)],
            "Variación capital circulante (€)": [0.0 for _ in range(n_periodos)],
            "Valor residual / otros cobros (€)": [
                0.0 if i < n_periodos - 1 else 30_000.0
                for i in range(n_periodos)
            ],
        }
    )


def ajustar_periodos(
    datos: pd.DataFrame,
    n_periodos: int,
    inversion_inicial: float,
) -> pd.DataFrame:
    """Ajusta la tabla editable cuando cambia el número de periodos."""
    defecto = crear_datos_defecto(n_periodos, inversion_inicial)
    if datos is None or datos.empty:
        return defecto

    trabajo = datos.copy()
    for columna in COLUMNAS_ENTRADA:
        if columna not in trabajo.columns:
            trabajo[columna] = defecto[columna]

    trabajo = trabajo[COLUMNAS_ENTRADA].copy()
    trabajo = trabajo.head(n_periodos).reset_index(drop=True)

    if len(trabajo) < n_periodos:
        faltan = defecto.iloc[len(trabajo) :].copy()
        trabajo = pd.concat([trabajo, faltan], ignore_index=True)

    trabajo["Periodo"] = list(range(1, n_periodos + 1))
    return trabajo


def calcular_amortizacion_contable(
    inversion_inicial: float,
    n_periodos: int,
    modelo: str,
    valor_no_amortizable: float = 0.0,
) -> list[float]:
    """Calcula una serie de amortización contable para la tabla fiscal."""
    if n_periodos < 1:
        return []

    base = max(0.0, float(inversion_inicial) - max(0.0, float(valor_no_amortizable)))
    if base == 0:
        return [0.0 for _ in range(n_periodos)]

    if modelo == MODELO_AMORTIZACION_LINEAL:
        return [base / n_periodos for _ in range(n_periodos)]

    if modelo == MODELO_AMORTIZACION_DIGITOS:
        suma_digitos = n_periodos * (n_periodos + 1) / 2
        return [base * (n_periodos - i) / suma_digitos for i in range(n_periodos)]

    if modelo == MODELO_AMORTIZACION_DEGRESIVA:
        tasa = min(1.0, 2 / n_periodos)
        saldo = base
        importes: list[float] = []
        for periodo in range(1, n_periodos + 1):
            if periodo == n_periodos:
                amortizacion = saldo
            else:
                amortizacion = min(saldo, saldo * tasa)
            importes.append(amortizacion)
            saldo = max(0.0, saldo - amortizacion)
        return importes

    raise ValueError(f"Modelo de amortización no reconocido: {modelo}")


def generar_caso_aleatorio(
    n_periodos: int,
    inversion_inicial: float,
    ingreso_medio: float,
    ratio_gastos: float,
    crecimiento_ingresos: float,
    volatilidad: float,
    probabilidad_inversion_adicional: float,
    inversion_adicional_media: float,
    variacion_cc_pct: float,
    valor_residual_pct: float,
    tipo_gravamen: float,
    modelo_amortizacion: str,
    valor_no_amortizable: float,
    semilla: int,
) -> pd.DataFrame:
    """Genera un caso aleatorio guiado por importes aproximados y porcentajes."""
    rng = np.random.default_rng(int(semilla))
    periodos = np.arange(n_periodos)

    crecimiento = (1 + crecimiento_ingresos) ** periodos
    ruido_ingresos = rng.normal(1.0, volatilidad, size=n_periodos)
    ingresos = np.maximum(0.0, ingreso_medio * crecimiento * ruido_ingresos)

    ruido_gastos = rng.normal(1.0, volatilidad / 2, size=n_periodos)
    gastos = np.maximum(0.0, ingresos * ratio_gastos * ruido_gastos)

    inversiones_adicionales = np.zeros(n_periodos)
    if inversion_adicional_media > 0 and probabilidad_inversion_adicional > 0:
        mascara = rng.random(n_periodos) < probabilidad_inversion_adicional
        importes = rng.normal(
            inversion_adicional_media,
            inversion_adicional_media * max(0.05, volatilidad),
            size=n_periodos,
        )
        inversiones_adicionales = np.where(mascara, np.maximum(0.0, importes), 0.0)

    variacion_cc = ingresos * variacion_cc_pct * rng.normal(1.0, 0.25, size=n_periodos)
    valor_residual = np.zeros(n_periodos)
    valor_residual[-1] = max(0.0, inversion_inicial * valor_residual_pct)

    amortizacion = calcular_amortizacion_contable(
        inversion_inicial,
        n_periodos,
        modelo_amortizacion,
        valor_no_amortizable,
    )

    return pd.DataFrame(
        {
            "Periodo": list(range(1, n_periodos + 1)),
            "Ingresos (€)": ingresos.round(2),
            "Gastos de explotación (€)": gastos.round(2),
            "Amortización contable (€)": np.round(amortizacion, 2),
            "Tipo de gravamen (%)": [float(tipo_gravamen) for _ in range(n_periodos)],
            "Inversiones adicionales (€)": inversiones_adicionales.round(2),
            "Variación capital circulante (€)": variacion_cc.round(2),
            "Valor residual / otros cobros (€)": valor_residual.round(2),
        }
    )
