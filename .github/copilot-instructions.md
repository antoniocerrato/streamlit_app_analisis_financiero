# Instrucciones para asistentes de código

Este proyecto es una app docente de Streamlit sobre viabilidad económica de proyectos.

## Contexto

- Usuario principal: profesor de asignatura de Proyectos.
- Público: estudiantes.
- Idioma: español de España.
- Campo: Ingeniería Civil.
- Término preferido: hormigón, no concreto.

## Objetivo de la app

Ayudar al alumnado a comprender y practicar:

- base imponible;
- impuestos;
- flujos de caja;
- VAN;
- TIR;
- payback;
- prima de riesgo;
- rotación del capital.

## Regla crítica

No modificar la fórmula principal de flujo de caja sin actualizar la documentación.

Fórmula actual:

```text
FC_t = Ingresos_t - Gastos_t - Impuestos_t - InversionesAdicionales_t - VariacionCapitalCirculante_t + ValorResidual_t
```

La amortización se usa para calcular impuestos, pero no se resta directamente en el flujo de caja.

## Estilo esperado

- Código claro.
- Comentarios útiles.
- Evitar complejidad innecesaria.
- Mantener nombres en español cuando sea didáctico.
- No añadir dependencias salvo necesidad clara.
- Mantener compatibilidad con Streamlit Community Cloud.
