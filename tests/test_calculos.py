from __future__ import annotations

import unittest

from calculos import (
    COLUMNAS_ENTRADA,
    MODELO_AMORTIZACION_DEGRESIVA,
    MODELO_AMORTIZACION_DIGITOS,
    MODELO_AMORTIZACION_LINEAL,
    ajustar_periodos,
    calcular_amortizacion_contable,
    crear_datos_defecto,
    generar_caso_aleatorio,
)


class CalculosTests(unittest.TestCase):
    def test_amortizaciones_suman_base_amortizable(self) -> None:
        for modelo in (
            MODELO_AMORTIZACION_LINEAL,
            MODELO_AMORTIZACION_DEGRESIVA,
            MODELO_AMORTIZACION_DIGITOS,
        ):
            with self.subTest(modelo=modelo):
                serie = calcular_amortizacion_contable(
                    inversion_inicial=200_000,
                    n_periodos=5,
                    modelo=modelo,
                    valor_no_amortizable=20_000,
                )
                self.assertEqual(len(serie), 5)
                self.assertAlmostEqual(sum(serie), 180_000, places=6)
                self.assertTrue(all(valor >= 0 for valor in serie))

    def test_generador_aleatorio_devuelve_columnas_de_entrada(self) -> None:
        df = generar_caso_aleatorio(
            n_periodos=6,
            inversion_inicial=250_000,
            ingreso_medio=120_000,
            ratio_gastos=0.55,
            crecimiento_ingresos=0.02,
            volatilidad=0.08,
            probabilidad_inversion_adicional=0.2,
            inversion_adicional_media=25_000,
            variacion_cc_pct=0.03,
            valor_residual_pct=0.15,
            tipo_gravamen=25,
            modelo_amortizacion=MODELO_AMORTIZACION_LINEAL,
            valor_no_amortizable=0,
            semilla=123,
        )

        self.assertEqual(list(df.columns), COLUMNAS_ENTRADA)
        self.assertEqual(len(df), 6)
        self.assertEqual(df["Periodo"].tolist(), [1, 2, 3, 4, 5, 6])
        self.assertGreater(df["Valor residual / otros cobros (€)"].iloc[-1], 0)

    def test_ajustar_periodos_conserva_y_completa(self) -> None:
        df = crear_datos_defecto(3, 90_000)
        df.loc[0, "Ingresos (€)"] = 123_456

        ajustado = ajustar_periodos(df, 5, 100_000)

        self.assertEqual(len(ajustado), 5)
        self.assertEqual(ajustado.loc[0, "Ingresos (€)"], 123_456)
        self.assertEqual(ajustado["Periodo"].tolist(), [1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
