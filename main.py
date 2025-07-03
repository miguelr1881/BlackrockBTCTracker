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

        # Create output directory if it doesn't exist
        output_dir = 'output_images'
        os.makedirs(output_dir, exist_ok=True)

        # Generate image
        output_path = generate_blackrock_image(btc, usd, change, date, output_dir)

        # Extract only the filename (for Drive upload)
        file_name = os.path.basename(output_path)

        # Upload image to Google Drive
        upload_to_drive(output_path, file_name)

        return (
            f"✅ Image generated and uploaded successfully!<br>"
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
