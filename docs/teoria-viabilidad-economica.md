# Viabilidad económica de proyectos

## 1. Objetivo del análisis

El análisis de viabilidad económica permite estudiar si un proyecto genera suficiente rentabilidad para justificar la inversión necesaria. En el ámbito de la Ingeniería Civil, este análisis puede aplicarse a decisiones empresariales como la adquisición de maquinaria, la implantación de una instalación auxiliar de obra, la apertura de una planta temporal de producción o la comparación entre alternativas técnicas con consecuencias económicas diferentes.

El objetivo no es únicamente saber si el proyecto produce beneficios contables, sino analizar si genera caja suficiente para recuperar la inversión inicial y obtener una rentabilidad adecuada al riesgo asumido.

## 2. Inversión inicial

La inversión inicial es el desembolso necesario para poner en marcha el proyecto.

Puede incluir:

- maquinaria;
- equipos auxiliares;
- instalaciones;
- montaje;
- licencias;
- necesidades iniciales de capital circulante.

$$
FC_0 = -I_0
$$

## 3. Ingresos y gastos de explotación

Los ingresos son las entradas económicas generadas por el proyecto. Los gastos de explotación son las salidas necesarias para que el proyecto funcione.

En Ingeniería Civil, un ejemplo adecuado sería una planta auxiliar de prefabricados de hormigón utilizada por una empresa para abastecer varias obras.

## 4. Amortización

La amortización representa la pérdida de valor contable de un activo.

$$
\text{Amortizacion anual} = \frac{\text{Valor amortizable}}{\text{Vida util}}
$$

La amortización reduce la base imponible, pero no es una salida real de caja.

## 5. Base imponible

$$
BI_t = Ingresos_t - Gastos_t - Amortizacion_t
$$

## 6. Impuestos

$$
Impuestos_t = BI_{liquidable,t} \times TipoGravamen_t
$$

En la app se usa por defecto el 25 %, aunque puede modificarse por periodo.

## 7. Flujo de caja

La app usa la formulación directa:

$$
FC_t = Ingresos_t - Gastos_t - Impuestos_t - InversionesAdicionales_t - \Delta CC_t + ValorResidual_t
$$

Esta forma es clara para docencia porque muestra directamente las entradas y salidas reales de dinero.

## 8. Tasa de descuento y prima de riesgo

La tasa de descuento se calcula como:

$$
k = tasa\ libre\ de\ riesgo + prima\ de\ riesgo
$$

La prima de riesgo compensa la incertidumbre del proyecto.

## 9. VAN

$$
VAN = -I_0 + \sum_{t=1}^{n}\frac{FC_t}{(1+k)^t}
$$

Un VAN positivo indica que el proyecto genera valor por encima de la rentabilidad exigida.

## 10. TIR

La TIR es la tasa que hace que el VAN sea cero.

## 11. Payback

El payback simple mide cuándo se recupera la inversión usando flujos no actualizados.

El payback descontado mide cuándo se recupera la inversión usando flujos actualizados.

## 12. Rotación del capital

$$
Rotacion\ media = \frac{Ingresos\ medios}{Inversion\ inicial}
$$

$$
Rotacion\ acumulada = \frac{Ingresos\ acumulados}{Inversion\ inicial}
$$

La rotación ayuda a entender cuánto volumen de actividad genera la inversión, pero no sustituye al VAN ni a la TIR.

## 13. Ejemplo breve

Una empresa adquiere un equipo auxiliar para fabricar elementos prefabricados de hormigón durante 4 años.

Datos:

- inversión inicial: 200.000 €;
- ingresos anuales: 110.000 €;
- gastos anuales: 55.000 €;
- amortización anual: 40.000 €;
- tipo de gravamen: 25 %;
- valor residual final: 30.000 €.

Base imponible anual:

$$
BI = 110000 - 55000 - 40000 = 15000
$$

Impuesto:

$$
Impuesto = 15000 \times 0{,}25 = 3750
$$

Flujo de caja anual ordinario:

$$
FC = 110000 - 55000 - 3750 = 51250
$$

Flujo de caja del último año:

$$
FC_4 = 110000 - 55000 - 3750 + 30000 = 81250
$$

## 14. Errores habituales

- Confundir beneficio contable con flujo de caja.
- Restar la amortización dos veces.
- Olvidar los impuestos.
- Ignorar la prima de riesgo.
- No considerar inversiones adicionales.
- Decidir solo con el payback.
