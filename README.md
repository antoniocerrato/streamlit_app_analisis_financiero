# App Streamlit: Viabilidad económica de proyectos

Aplicación docente para analizar la viabilidad económica de un proyecto mediante flujos de caja, fiscalidad básica, actualización de flujos e indicadores de rentabilidad.

## Objetivo

La app está pensada para estudiantes de asignaturas de Proyectos, especialmente en contextos de Ingeniería Civil. Permite construir casos sencillos de inversión y explotación, modificando los valores por periodo y observando cómo cambian los indicadores económicos.

## Funcionalidades principales

- Entrada editable por periodos.
- Descarga y carga de plantilla Excel para completar datos fuera de la app.
- Generador de casos aleatorios guiado por ingresos, gastos, crecimiento, inversiones adicionales y capital circulante.
- Inversión inicial.
- Ingresos y gastos de explotación.
- Amortización contable manual, lineal, degresiva doble o por suma de dígitos.
- Base imponible.
- Tipo de gravamen por periodo, con 25 % por defecto.
- Impuestos pagados.
- Flujos de caja.
- Flujos de caja actualizados.
- VAN.
- TIR.
- Payback simple.
- Payback descontado.
- Prima de riesgo.
- Rotación media anual del capital.
- Rotación acumulada del capital.
- Índice de rentabilidad.
- Sensibilidad del VAN a distintas tasas de descuento.
- Exportación a Excel.
- Teoría de apoyo integrada, con fórmulas renderizadas desde Markdown.

## Criterio docente adoptado

La app calcula primero la base imponible:

```text
Base imponible = Ingresos - Gastos de explotación - Amortización
```

Después calcula los impuestos:

```text
Impuestos = Base imponible liquidable × Tipo de gravamen
```

Y finalmente calcula el flujo de caja con una formulación directa:

```text
Flujo de caja = Ingresos
              - Gastos de explotación
              - Impuestos pagados
              - Inversiones adicionales
              - Variación de capital circulante
              + Valor residual u otros cobros
```

La amortización no se resta directamente en el flujo de caja porque no es una salida real de dinero. Su efecto se recoge indirectamente al reducir la base imponible y, por tanto, los impuestos.

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

En el equipo de trabajo habitual existe un entorno de Anaconda ya preparado para Streamlit:

```powershell
D:\Usuarios\antonio\anaconda3\envs\streamlit-apps\Scripts\streamlit.exe run app.py
```

Si hay que comprobar las dependencias del entorno:

```powershell
D:\Usuarios\antonio\anaconda3\envs\streamlit-apps\python.exe -c "import streamlit, pandas, numpy, numpy_financial, openpyxl"
```

Nota: en este equipo `conda env list` puede fallar por un problema de plugins/permisos de conda. Para trabajar
con esta app basta con usar directamente los ejecutables del entorno `streamlit-apps`.

## Despliegue en Streamlit Community Cloud

1. Sube esta carpeta a un repositorio de GitHub.
2. Entra en Streamlit Community Cloud.
3. Crea una nueva app conectada al repositorio.
4. Selecciona la rama principal.
5. Indica como archivo principal:

```text
app.py
```

Si la app está dentro de una subcarpeta, usa la ruta completa, por ejemplo:

```text
streamlit_app_viabilidad/app.py
```

## Archivos de contexto para agentes

Este repositorio incluye varios archivos `.md` diseñados para ayudar a agentes de programación en Visual Studio, GitHub Copilot, Cursor u otros entornos:

- `AGENTS.md`: instrucciones generales para agentes.
- `CONTEXTO_APP.md`: contexto funcional y docente de la aplicación.
- `docs/modelo-calculo.md`: especificación de fórmulas y criterios de cálculo.
- `docs/especificacion-funcional.md`: descripción de pantallas, entradas y salidas.
- `docs/teoria-viabilidad-economica.md`: contenido teórico para la web.
- `.github/copilot-instructions.md`: instrucciones específicas para Copilot u otros agentes compatibles.
