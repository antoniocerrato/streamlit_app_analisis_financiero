# App Streamlit: Viabilidad económica de proyectos

Aplicación docente para calcular:

- Base imponible por periodo.
- Impuesto de sociedades.
- Flujos de caja.
- Flujos de caja actualizados.
- VAN.
- TIR.
- Payback simple.
- Payback descontado.
- Prima de riesgo y tasa de descuento.
- Índice de rentabilidad.
- Sensibilidad del VAN.

## Archivos

- `app.py`: aplicación principal de Streamlit.
- `requirements.txt`: dependencias necesarias para el despliegue.

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Crea un repositorio en GitHub.
2. Sube `app.py` y `requirements.txt` al repositorio.
3. Entra en Streamlit Community Cloud.
4. Conecta tu cuenta de GitHub.
5. Selecciona el repositorio.
6. Indica como archivo principal:

```text
app.py
```

7. Despliega la aplicación.

## Enlace desde tu web de GitHub Pages

Cuando Streamlit te dé la URL pública de la aplicación, modifica el botón correspondiente en tu `index.html`.

Por ejemplo, cambia:

```html
<a class="button" href="apps/van-tir.html">Abrir aplicación</a>
```

por:

```html
<a class="button" href="https://TU-APP.streamlit.app">Abrir aplicación</a>
```
