# Decisiones de diseño

## 1. Streamlit

Se utiliza Streamlit porque permite crear aplicaciones docentes interactivas en Python con rapidez.

## 2. Fórmula directa de flujo de caja

Se adopta la fórmula directa para facilitar la comprensión:

```text
Flujo de caja = Ingresos - Gastos - Impuestos - Inversiones adicionales - Variación de capital circulante + Valor residual
```

Esta decisión se tomó porque resulta más natural para el alumnado que partir del resultado contable y sumar la amortización.

## 3. Amortización

La amortización se mantiene porque es necesaria para calcular la base imponible.

No se resta en el flujo de caja para evitar doble contabilización.

## 4. Fiscalidad simplificada

La app usa un modelo fiscal simplificado. El tipo de gravamen es editable por periodo.

## 5. Rotación del capital

Se añade la rotación del capital como indicador complementario. No sustituye a los indicadores de rentabilidad.

## 6. Prima de riesgo

Se separa la tasa libre de riesgo de la prima de riesgo para que el estudiante comprenda que la tasa de descuento incluye una compensación por incertidumbre.

## 7. Ejemplos

Los ejemplos deben mantenerse dentro de contextos empresariales claros. Evitar ejemplos de infraestructuras públicas orientados a análisis coste-beneficio social.
