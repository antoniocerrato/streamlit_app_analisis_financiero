# Contexto de la aplicación

## Nombre

Viabilidad económica de proyectos.

## Finalidad

Aplicación docente para que el alumnado practique el análisis económico de proyectos variando parámetros de entrada y observando cómo cambian los principales indicadores.

## Público objetivo

Estudiantes de asignaturas de Proyectos, especialmente en titulaciones de Ingeniería Civil o asignaturas técnicas donde se introducen análisis de inversión, flujos de caja y rentabilidad.

## Problema que resuelve

En clase se suelen resolver ejercicios cerrados con datos fijos. Esta app permite que el estudiante modifique:

- número de periodos;
- inversión inicial;
- ingresos;
- gastos;
- amortización;
- tipo de gravamen;
- inversiones adicionales;
- variación de capital circulante;
- valor residual;
- tasa libre de riesgo;
- prima de riesgo.

Así puede observar el efecto de cada variable sobre el VAN, la TIR, el payback y otros indicadores.

## Enfoque docente

La app no pretende ser una herramienta profesional de valoración financiera avanzada. Su objetivo es explicar bien los fundamentos:

1. Se calcula la base imponible.
2. Se calculan los impuestos.
3. Se calcula el flujo de caja.
4. Se actualizan los flujos.
5. Se interpretan los indicadores.

## Decisión importante sobre el flujo de caja

La versión actual utiliza una fórmula directa de flujo de caja:

```text
Flujo de caja = Ingresos
              - Gastos de explotación
              - Impuestos pagados
              - Inversiones adicionales
              - Variación de capital circulante
              + Valor residual u otros cobros
```

Esta formulación se eligió porque es más comprensible para los estudiantes que la expresión alternativa:

```text
Flujo de caja = Resultado después de impuestos + Amortización
```

Ambas pueden ser equivalentes en determinados casos, pero la formulación directa evita confusión.

## Adaptación a España

- Moneda: euro.
- Terminología: español de España.
- Tipo de gravamen por defecto: 25 %, editable.
- Conceptos: Impuesto sobre Sociedades, base imponible, amortización contable, capital circulante.

## Adaptación a Ingeniería Civil

Los ejemplos deben evitar confundirse con análisis coste-beneficio social. Preferir contextos empresariales claros, como:

- adquisición de maquinaria auxiliar;
- instalación temporal de producción;
- planta auxiliar de prefabricados de hormigón;
- equipos de obra;
- comparación interna entre producir o subcontratar.

Evitar ejemplos de infraestructuras públicas donde el objetivo principal sea valorar beneficios sociales, ahorro de tiempo, externalidades o bienestar colectivo, salvo que se indique expresamente que se trata de análisis coste-beneficio.

## Relación con la web

La app está pensada para enlazarse desde una web estática alojada en GitHub Pages. La web contendrá:

- portada de las aplicaciones;
- enlace a la app Streamlit;
- teoría en Markdown o HTML;
- ejercicios de ejemplo.

## Relación con Streamlit

Streamlit ejecuta el código Python en servidor. GitHub Pages solo debe funcionar como portal estático de acceso.
