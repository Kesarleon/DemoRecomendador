# Ambéa: Demo de Recomendador de Joyas en Streamlit

Esta es una aplicación de demostración interactiva construida con Streamlit que presenta un sistema de recomendación de joyas personalizado para la marca ficticia Ambéa.

La aplicación genera recomendaciones para un cliente basándose en su perfil, la temporada actual y las ofertas del mes.

## Cómo Desplegar en Streamlit Cloud

Sigue estos pasos para desplegar esta aplicación en tu propia cuenta de Streamlit Cloud.

### Prerrequisitos
1.  **Una cuenta de GitHub:** Necesitarás una para alojar los archivos del proyecto.
2.  **Archivos del proyecto:** Asegúrate de tener los siguientes archivos en tu repositorio:
    - `app.py` (el código principal de la aplicación)
    - `clientes.csv` (el dataset de clientes)
    - `productos.csv` (el dataset de productos)
    - `requirements.txt` (las dependencias de Python)

### Pasos para el Despliegue

**Paso 1: Sube tu proyecto a un repositorio de GitHub**

1.  Crea un nuevo repositorio en tu cuenta de GitHub.
2.  Sube los cuatro archivos (`app.py`, `clientes.csv`, `productos.csv`, `requirements.txt`) a este repositorio.

**Paso 2: Conéctate a Streamlit Cloud**

1.  Ve a [share.streamlit.io](https://share.streamlit.io) y regístrate o inicia sesión. Puedes usar tu cuenta de GitHub para una autenticación más sencilla.
2.  Autoriza a Streamlit para que pueda acceder a tus repositorios de GitHub.

**Paso 3: Crea una nueva aplicación**

1.  En tu panel de control de Streamlit Cloud, haz clic en el botón **"New app"**.
2.  Selecciona la opción **"From repo"**.
3.  En el campo **"Repository"**, elige el repositorio de GitHub donde subiste los archivos del proyecto.
4.  Asegúrate de que la **"Branch"** (rama) sea la correcta (normalmente `main` o `master`).
5.  El **"Main file path"** (ruta del archivo principal) debe ser `app.py`. Streamlit normalmente lo detecta automáticamente.
6.  Dale un nombre personalizado a tu URL de la aplicación si lo deseas.

**Paso 4: Despliega la aplicación**

1.  Haz clic en el botón **"Deploy!"**.
2.  Streamlit comenzará el proceso de despliegue. Instalará las dependencias listadas en `requirements.txt` y ejecutará la aplicación.
3.  ¡Listo! Una vez que termine el proceso, tu aplicación estará en vivo y accesible a través de la URL proporcionada.

Ahora tienes una demo funcional del recomendador de joyas Ambéa desplegada en la nube.