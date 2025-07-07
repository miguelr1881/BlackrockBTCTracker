from flask import Flask
from scraper import get_blackrock_data
from image_generator import generate_blackrock_image
from upload_to_drive import upload_to_drive

import os

app = Flask(__name__)

@app.route('/')
def run_blackrock_bot():
    try:
        # Get data from scraper
        btc, usd, change, date = get_blackrock_data()
        print(f"🔍 Valor actual BTC: {btc}, USD: {usd}")

        # Crear output directory si no existe
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generar imagen
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)
        file_name = os.path.basename(output_path)

        # Subir a Drive (solo sube si hay cambio)
        result = upload_to_drive(output_path, file_name, btc)

        if result == "No change":
            return f"ℹ️ No changes detected. BTC remains at {btc}."

        return (
            f"✅ Change detected, image generated and uploaded successfully!<br>"
            f"<ul>"
            f"<li>BTC: {btc}</li>"
            f"<li>USD: {usd}</li>"
            f"<li>Change: {change}</li>"
            f"<li>Date: {date}</li>"
            f"</ul>"
        )

    except Exception as e:
        return f"❌ Error: {str(e)}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
