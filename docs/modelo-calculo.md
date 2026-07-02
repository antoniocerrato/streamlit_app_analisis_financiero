# Modelo de cálculo

## 1. Periodos

El momento 0 corresponde a la inversión inicial. Los periodos 1 a n corresponden a la explotación.

```text
FC_0 = -I_0
```

## 2. Base imponible

La base imponible antes de compensación se calcula como:

```text
BI_t = Ingresos_t - Gastos_t - Amortización_t
```

La amortización se incluye aquí porque reduce el resultado fiscal.

### 2.1. Modelos de amortización contable

La amortización puede escribirse manualmente en la tabla o calcularse de forma automática.
En todos los casos se usa solo para calcular la base imponible; no se resta directamente
en el flujo de caja.

Base amortizable:

```text
Base_amortizable = Inversion_inicial - Valor_no_amortizable
```

Amortización lineal:

```text
Amortizacion_t = Base_amortizable / n
```

Amortización degresiva doble:

```text
Amortizacion_t = Saldo_pendiente_t * (2 / n)
```

En el último periodo se amortiza el saldo pendiente para completar la base amortizable.

Amortización por suma de dígitos:

```text
Amortizacion_t = Base_amortizable * (n - t + 1) / (1 + 2 + ... + n)
```

## 3. Compensación de bases imponibles negativas

La app incluye una opción para compensar bases imponibles negativas de periodos anteriores.

Si está desactivada:

```text
BI_liquidable_t = max(BI_t, 0)
```

si está activada, las bases negativas se acumulan y se compensan con bases positivas posteriores.

## 4. Impuestos pagados

```text
Impuestos_t = BI_liquidable_t × TipoGravamen_t
```

El tipo de gravamen se introduce por periodo. El valor por defecto es 25 %.

## 5. Resultado contable después de impuestos

La app calcula este resultado como dato informativo:

```text
Resultado_contable_t = BI_t - Impuestos_t
```

No debe confundirse con el flujo de caja.

## 6. Flujo de caja operativo después de impuestos

```text
FCO_t = Ingresos_t - Gastos_t - Impuestos_t
```

## 7. Flujo de caja del periodo

Formulación principal adoptada:

```text
FC_t = Ingresos_t
       - Gastos_t
       - Impuestos_t
       - InversionesAdicionales_t
       - VariacionCapitalCirculante_t
       + ValorResidual_t
```

La amortización no se resta directamente en el flujo de caja porque no representa una salida real de dinero en el periodo.

## 8. Flujo actualizado

```text
FCA_t = FC_t / (1 + k)^t
```

donde:

```text
k = tasa_libre_riesgo + prima_riesgo
```

## 9. Valor actual neto

```text
VAN = -I_0 + sum(FC_t / (1 + k)^t)
```

## 10. Tasa interna de rentabilidad

La TIR es la tasa que hace que el VAN sea cero.

```text
0 = -I_0 + sum(FC_t / (1 + TIR)^t)
```

La app usa `numpy_financial.irr`.

## 11. Payback simple

El payback simple se calcula sobre los flujos no actualizados. Se usa interpolación lineal cuando la recuperación se produce dentro de un periodo.

## 12. Payback descontado

El payback descontado se calcula sobre los flujos actualizados. También usa interpolación lineal.

## 13. Índice de rentabilidad

```text
IR = Valor actual de flujos positivos / Inversión inicial
```

## 14. Rotación del capital

Rotación media anual:

```text
Rotacion_media = Ingresos_medios_anuales / Inversion_inicial
```

Rotación acumulada:

```text
Rotacion_acumulada = Ingresos_acumulados / Inversion_inicial
```

La rotación del capital no mide rentabilidad por sí sola. Solo mide relación entre volumen de ingresos y capital invertido.

## 15. Sensibilidad del VAN

La app calcula el VAN para tasas de descuento entre 0 % y 20 %, con incrementos de 1 punto porcentual.

## 16. Generador de casos aleatorios

El generador crea una tabla de entrada a partir de parámetros aproximados. Usa una semilla para que
el caso sea reproducible.

Los ingresos se generan alrededor de un ingreso medio, con crecimiento y variabilidad:

```text
Ingresos_t ≈ Ingreso_medio * (1 + crecimiento)^(t-1) * ruido_t
```

Los gastos de explotación se calculan como proporción de los ingresos, también con variabilidad:

```text
Gastos_t ≈ Ingresos_t * ratio_gastos * ruido_t
```

Las inversiones adicionales se generan por periodo según una probabilidad indicada. La variación
de capital circulante se expresa como porcentaje de los ingresos. El valor residual se coloca en
el último periodo.

Este generador no pretende predecir datos reales. Su objetivo es producir casos variados y
razonables para ejercicios de clase.
