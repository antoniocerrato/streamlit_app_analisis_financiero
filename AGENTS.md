# AGENTS.md

## Propósito de este archivo

Este archivo ofrece contexto e instrucciones para agentes de programación que trabajen sobre esta app en Visual Studio, GitHub Copilot, Cursor u otros entornos asistidos por IA.

## Descripción general del proyecto

El proyecto es una aplicación docente en Streamlit para estudiar la viabilidad económica de proyectos. Está orientada a estudiantes de asignaturas de Proyectos, con ejemplos y lenguaje próximos a la Ingeniería Civil en España.

La app permite introducir datos por periodos y calcula:

- base imponible;
- impuestos pagados;
- flujos de caja;
- flujos de caja actualizados;
- VAN;
- TIR;
- payback simple;
- payback descontado;
- prima de riesgo;
- rotación del capital;
- índice de rentabilidad;
- sensibilidad del VAN.

## Principios de diseño

1. Priorizar claridad docente sobre complejidad financiera.
2. Usar terminología en español de España.
3. Usar "hormigón", no "concreto".
4. Evitar tecnicismos innecesarios si no aportan claridad.
5. Mantener las fórmulas visibles y coherentes con la teoría.
6. No añadir supuestos fiscales complejos sin documentarlos.
7. Separar claramente cálculo fiscal y cálculo de caja.
8. Evitar que la amortización se reste dos veces.
9. Mantener las entradas editables por periodo.
10. Mantener la app desplegable en Streamlit Community Cloud.

## Criterio de flujo de caja

El criterio actual del proyecto es calcular el flujo de caja de forma directa:

```text
FC_t = Ingresos_t
       - Gastos de explotación_t
       - Impuestos pagados_t
       - Inversiones adicionales_t
       - Variación de capital circulante_t
       + Valor residual u otros cobros_t
```

La amortización se usa para calcular la base imponible, pero no se resta directamente en el flujo de caja.

## Fiscalidad

La app usa por defecto un tipo de gravamen del 25 %. Este valor es editable por periodo.

No introducir reglas fiscales avanzadas salvo que se documenten claramente. Esta app no pretende sustituir asesoramiento fiscal.

## Estilo de código

- Mantener el código en Python claro y legible.
- Evitar abstracciones excesivas.
- Documentar las funciones de cálculo.
- No añadir dependencias innecesarias.
- Mantener compatibilidad con Streamlit Community Cloud.
- Usar nombres de variables en español cuando ayuden a la comprensión docente.

## Archivos importantes

- `app.py`: aplicación principal.
- `README.md`: guía general del proyecto.
- `CONTEXTO_APP.md`: contexto docente y funcional.
- `docs/modelo-calculo.md`: fórmulas y criterios.
- `docs/especificacion-funcional.md`: estructura funcional.
- `docs/teoria-viabilidad-economica.md`: teoría para publicar en la web.
- `.github/copilot-instructions.md`: instrucciones para asistentes de código.

## Tareas futuras posibles

- Separar funciones de cálculo en un módulo `calculos.py`.
- Añadir pruebas unitarias para VAN, TIR y payback.
- Añadir importación de datos desde CSV o Excel.
- Añadir escenarios: optimista, base y pesimista.
- Añadir exportación a PDF.
- Añadir enlaces desde la app a la página teórica publicada en GitHub Pages.
