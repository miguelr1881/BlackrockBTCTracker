# Blackrock BTC Holdings Tracker

Este proyecto rastrea automáticamente las tenencias de Bitcoin (BTC) de Blackrock, genera una imagen con la información más reciente y la sube a una carpeta específica en Google Drive.

## Características

- Web scraping de las tenencias de BTC de Blackrock
- Generación automática de imágenes con diseño personalizado
- Subida automática a Google Drive
- Formato de imagen optimizado para redes sociales
- Registro de datos históricos

## Requisitos Previos

- Python 3.7 o superior
- Cuenta de Google Cloud Platform
- Habilitada la API de Google Drive

## Instalación

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd Blackrock-BTC-Holding-Tracker
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   
   Si no existe el archivo requirements.txt, instala manualmente:
   ```bash
   pip install requests beautifulsoup4 Pillow pydrive google-api-python-client google-auth-httplib2 google-auth-oauthlib flask
   ```

## Configuración de Google Drive API

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Drive
4. Crea credenciales de tipo "OAuth 2.0 Client ID"
5. Descarga el archivo JSON de credenciales
6. Renombra el archivo descargado a `client_secrets.json` y colócalo en el directorio raíz del proyecto

## Uso

### Ejecución Básica

```bash
python main.py
```

### Estructura de Archivos

- `main.py`: Punto de entrada de la aplicación
- `scraper.py`: Lógica de web scraping para obtener datos de Blackrock
- `image_generator.py`: Genera la imagen con los datos obtenidos
- `upload_to_drive.py`: Maneja la subida de archivos a Google Drive
- `template.png`: Imagen base para la generación de gráficos
- `output_images/`: Directorio donde se guardan las imágenes generadas localmente

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
GOOGLE_DRIVE_FOLDER=IFTTT
```

## Funcionamiento

1. El script obtiene los datos más recientes de las tenencias de BTC de Blackrock
2. Genera una imagen con un diseño limpio y profesional
3. Sube la imagen a la carpeta especificada en Google Drive
4. La imagen se nombra automáticamente con la fecha de los datos

## Personalización

### Cambiar el Diseño de la Imagen

Modifica el archivo `template.png` para cambiar el diseño base de la imagen generada.

### Cambiar la Carpeta de Destino

Edita la variable `folder_name` en `upload_to_drive.py` para cambiar la carpeta de destino en Google Drive.

## Programación Automática (Opcional)

Puedes programar la ejecución automática usando cron (Linux/macOS) o Task Scheduler (Windows) para ejecutar el script diariamente.

## Solución de Problemas

### Error de Autenticación

Si recibes errores de autenticación:
1. Asegúrate de que el archivo `client_secrets.json` existe y es válido
2. Verifica que hayas habilitado la API de Google Drive
3. Elimina el archivo `mycreds.txt` para forzar una nueva autenticación

### Problemas con las Dependencias

Si hay problemas con las dependencias:
```bash
pip install --upgrade -r requirements.txt
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, envía un Pull Request con tus mejoras.

## Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio.
