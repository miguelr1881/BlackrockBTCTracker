from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


def generate_blackrock_image(btc, usd, change, date, output_dir='.'):
    # Crear nombre de archivo basado en la fecha (formato: blackrock_btc_YYYY-MM-DD.png)
    import re
    # Extraer solo caracteres alfanuméricos y guiones de la fecha
    safe_date = re.sub(r'[^a-zA-Z0-9-]', '', date.replace(' ', '-'))
    output_path = f"{output_dir}/blackrock_btc_{safe_date}.png"
    try:
        # Cargar la imagen de plantilla
        img = Image.open('template.png')
        draw = ImageDraw.Draw(img)

        # Configuración de la fuente Arial Black
        font_size = 75
        font_loaded = False

        # Lista de fuentes del sistema ordenadas por similitud a Arial Black
        system_fonts = [
            # Fuentes más similares a Arial Black (bold/extra bold)
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraBold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
            # Respaldos adicionales
            "/System/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica Bold.ttf",
            "DejaVuSans-Bold.ttf",
            "Ubuntu-Bold.ttf"
        ]

        # Intentar cargar cada fuente
        for font_path in system_fonts:
            try:
                font = ImageFont.truetype(font_path, font_size)
                print(f"✅ Using font: {font_path}")
                font_loaded = True
                break
            except Exception as e:
                continue

        # Si no se pudo cargar ninguna fuente del sistema, usar la por defecto pero más grande
        if not font_loaded:
            try:
                # Usar una fuente por defecto más grande para compensar
                font = ImageFont.load_default()
                print("⚠️ Using default font - may appear smaller")
            except:
                font = ImageFont.load_default()

        # Configuración de colores
        text_color = (255, 255, 255)  # Blanco

        # Obtener dimensiones de la imagen
        width, height = img.size

        # Formatear el cambio con signo y color según sea positivo o negativo
        if change.startswith('-'):
            # Si es negativo, dejarlo como está y usar rojo pastel
            change_text = change
            change_color = (255, 150, 150)  # Rojo pastel
        else:
            # Si es positivo, agregar signo + y usar verde
            change_text = f"+{change}" if change and not change.startswith(
                '+') else change
            change_color = (120, 200, 120)  # Verde pastel

        # Textos a mostrar con sus respectivos colores (más vibrantes para compensar la fuente)
        text_items = [
            # Naranja más intenso para mayor impacto
            (f"{btc} BTC", (255, 165, 70)),
            # Celeste más vibrante
            (usd, (80, 180, 255)),
            # Cambio con color según sea positivo o negativo (más contrastante)
            (change_text, change_color),
            # Gris más claro para mejor legibilidad
            (date, (140, 140, 140))
        ]

        # Calcular el espacio total necesario para todos los textos
        total_height = 0
        text_heights = []
        text_widths = []

        for text, _ in text_items:
            bbox = draw.textbbox((0, 0), str(text), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_heights.append(text_height)
            text_widths.append(text_width)
            total_height += text_height

        # Espaciado entre líneas (aumentado a 60 píxeles)
        line_spacing = 80  # Aumentado de 40 a 60 píxeles
        total_height += line_spacing * (len(text_items) - 1)

        # Posición Y inicial - bajada el doble que antes
        offset_arriba = -74  # Reducido de 10 a -10 para bajar el doble que antes
        start_y = (height - total_height) // 2 - offset_arriba

        # Dibujar cada línea de texto centrada con su color correspondiente
        current_y = start_y
        for i, (text, color) in enumerate(text_items):
            text_width = text_widths[i]
            text_height = text_heights[i]

            # Calcular posición X para centrar el texto
            x = (width - text_width) // 2

            # Dibujar el texto sin contorno
            draw.text((x, current_y), str(text), font=font, fill=color)

            # Mover a la siguiente línea
            current_y += text_height + line_spacing

        # Guardar la imagen (manejo de directorio)
        try:
            directory = os.path.dirname(output_path)
            if directory:  # Solo crear directorios si la ruta los incluye
                os.makedirs(directory, exist_ok=True)
            img.save(output_path)
            print(f"✅ Imagen generada: {output_path}")
            return output_path  # Devolver la ruta del archivo generado
        except Exception as save_error:
            print(f"❌ Error al guardar la imagen: {save_error}")
            # Intentar guardar en el directorio actual si falla la ruta especificada
            try:
                output_path = 'blackrock_btc_output.png'
                img.save(output_path)
                print(f"✅ Imagen guardada en: {os.path.abspath(output_path)}")
                return output_path
            except Exception as e:
                print(f"❌ Error crítico al guardar la imagen: {e}")
                raise

    except Exception as e:
        print(f"❌ Error al generar la imagen: {e}")
        raise

    except Exception as e:
        print(f"❌ Error al generar la imagen: {str(e)}")
        import traceback
        traceback.print_exc()
