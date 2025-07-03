from flask import Flask
from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from upload_to_drive import upload_to_drive

import os

app = Flask(__name__)


# Endpoint de prueba simple
@app.route('/')
def home():
    return "✅ Blackrock BTC Bot is running."


# Endpoint que ejecuta el bot completo
@app.route('/run')
def run_blackrock_bot():
    try:
        # Extraer datos del scraping
        btc, usd, change, date = get_blackrock_data()

        # Crear el directorio de salida si no existe
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generar la imagen
        output_path = generate_blackrock_image(btc, usd, change, date,
                                               output_dir)

        # Obtener solo el nombre del archivo
        file_name = os.path.basename(output_path)

        # Subir la imagen a Google Drive
        upload_to_drive(output_path, file_name)

        # Respuesta simple para cron-job.org
        return "✅ Image created & uploaded."

    except Exception as e:
        # Devuelve un error simple si algo falla
        return f"❌ Error: {str(e)}", 500


# Ejecutar Flask en Replit
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
