# Guía de despliegue

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud

1. Crear o abrir un repositorio en GitHub.
2. Subir los archivos de la app.
3. Entrar en Streamlit Community Cloud.
4. Crear una nueva app.
5. Seleccionar el repositorio y la rama.
6. Indicar el archivo principal:

```text
app.py
```

Si está en subcarpeta:

```text
streamlit_app_viabilidad/app.py
```

7. Desplegar.

## Enlace desde GitHub Pages

Cuando Streamlit proporcione una URL pública, modificar el botón de la web principal.

Ejemplo:

```html
<a class="button" href="https://TU-APP.streamlit.app">Abrir aplicación</a>
```

## Recomendación de estructura del repositorio

```text
apps-proyectos/
├── index.html
├── styles.css
├── teoria/
│   └── viabilidad-economica.md
└── streamlit_app_viabilidad/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── AGENTS.md
    ├── CONTEXTO_APP.md
    └── docs/
        ├── modelo-calculo.md
        ├── especificacion-funcional.md
        └── teoria-viabilidad-economica.md
```
