# Especificación funcional

## Pantalla principal

La pantalla principal contiene:

1. Título y descripción.
2. Barra lateral de parámetros generales.
3. Generador de casos y modelos de amortización.
4. Descarga y carga de plantilla Excel.
5. Tabla editable de datos por periodo.
6. Indicadores principales.
7. Tabla de cálculo.
8. Gráficas.
9. Sensibilidad del VAN.
10. Resumen descargable.
11. Criterios de cálculo usados y teoría de apoyo.

## Barra lateral

### Parámetros generales

- Número de periodos.
- Inversión inicial.

### Tasa de descuento

- Tasa libre de riesgo.
- Prima de riesgo.
- Tasa de descuento resultante.

### Fiscalidad

- Opción para compensar bases imponibles negativas.
- Opción para no considerar impuestos negativos.

### Amortización contable

- Modo manual.
- Amortización lineal.
- Amortización degresiva doble.
- Amortización por suma de dígitos.
- Valor no amortizable o residual fiscal.
- Botón para aplicar la amortización calculada a la tabla.

### Generador de casos

Permite crear un caso aleatorio guiado por:

- semilla;
- ingresos medios aproximados;
- ratio de gastos de explotación sobre ingresos;
- crecimiento medio de ingresos;
- variabilidad del caso;
- probabilidad e importe medio de inversiones adicionales;
- variación de capital circulante sobre ingresos;
- valor residual final;
- tipo de gravamen.

## Tabla editable

Columnas:

- Periodo.
- Ingresos.
- Gastos de explotación.
- Amortización contable.
- Tipo de gravamen.
- Inversiones adicionales.
- Variación del capital circulante.
- Valor residual u otros cobros.

## Plantilla Excel

La app permite:

- descargar una plantilla con la hoja `Datos por periodo`;
- completar la plantilla en Excel;
- subir la plantilla completada;
- cargar sus datos en la tabla editable.

La plantilla debe respetar las columnas esperadas. Si no encuentra la hoja `Datos por periodo`,
la app intenta leer la primera hoja del archivo.

## Indicadores principales

- VAN.
- TIR.
- Payback simple.
- Payback descontado.
- Tasa de descuento.
- Prima de riesgo.
- Rotación media anual.
- Rotación acumulada.
- Índice de rentabilidad.
- VAN sin prima de riesgo.
- Exposición máxima de caja.
- Ingresos acumulados.

## Tabla de cálculo

Debe mostrar de forma transparente:

- base imponible;
- impuestos;
- resultado contable;
- flujo de caja operativo;
- ajustes de caja;
- flujo de caja;
- flujo actualizado;
- acumulados.

## Gráficas

Se muestra una gráfica de líneas con:

- flujo de caja;
- flujo de caja actualizado;
- flujo de caja acumulado;
- flujo actualizado acumulado.

## Sensibilidad del VAN

Se muestra una gráfica del VAN frente a la tasa de descuento.

## Descarga

La app permite descargar en Excel:

- tabla de resultados por periodo;
- resumen de indicadores.

También permite descargar una plantilla Excel independiente para entrada de datos.
