import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps

COLOR_QR = "#D32F2F"  # Un rojo bonito y oscuro para que escanee bien
COLOR_TEXTO = "#1A237E" # Un azul oscuro escolar para el nombre

FUENTE_RUTA = "arial.ttf" 

datos_ninos = [
    {"nombre": "Antonella", "link": "https://drive.google.com/drive/folders/10vFxIKdBKbnGfYllDZTPPL519IZmHb17?usp=sharing"},
    {"nombre": "Lia", "link": "https://drive.google.com/drive/folders/1w_r_rk89Lu9U1437BXiahlGNsmkIuCPB?usp=sharing"},
    {"nombre": "Thaily", "link": "https://drive.google.com/drive/folders/1F29prhCWlKtFqvCQyMwL-OJ1TcXJjTdC?usp=sharing"},
    {"nombre": "Estrella", "link": "https://drive.google.com/drive/folders/1F29prhCWlKtFqvCQyMwL-OJ1TcXJjTdC?usp=sharing"},
    {"nombre": "Mariagracia", "link": "https://drive.google.com/drive/folders/1h9A6zyK_ZTTUezeaJWK1ZHxV0UKvIrl1?usp=sharing"},
    {"nombre": "Gia", "link": "https://drive.google.com/drive/folders/10hn_mrbu8sYubYdDbxNknwNsJBLZmQLC?usp=sharing"},
    {"nombre": "Angel", "link": "https://drive.google.com/drive/folders/1fNkNmy6xrKfSYp0fR8PNw54rxGWEFm6n?usp=sharing"},
    {"nombre": "Emir", "link": "https://drive.google.com/drive/folders/1KjD6qRk48CvK7lCbA5f661PBxCJtprB8?usp=sharing"},
    {"nombre": "Leyto", "link": "https://drive.google.com/drive/folders/10NcBYeiIMzpqvBTuwS19qNmBe_l2Z2zm?usp=sharing"},
    {"nombre": "Ivanna", "link": "https://drive.google.com/drive/folders/1DWU0JTbNoPoh9_6GPj2WcMqmAVrgI41-?usp=sharing"},
    {"nombre": "Andrea", "link": "https://drive.google.com/drive/folders/1pc02VfTgid-aeNYk79hx_yo_U1NkCml3?usp=sharing"},
    {"nombre": "Andree", "link": "https://drive.google.com/drive/folders/1UjPBGdcwhZkNLRZe4hubv18_Jv0U-mOL?usp=sharing"},
    {"nombre": "Roselyne", "link": "https://drive.google.com/drive/folders/1lK1Z7n_kJdWY-eFlxUonH9Y9Jqye5Hd0?usp=sharing"},
    {"nombre": "Cristofer", "link": "https://drive.google.com/drive/folders/1czNwhOtasr6n0WaZUjteBZ3wu9W644bx?usp=sharing"},
    {"nombre": "Arianna", "link": "https://drive.google.com/drive/folders/1htokSW7njH-8k2pLtu4tzgJrrSNBvCfk?usp=sharing"},
    {"nombre": "Joaquin", "link": "https://drive.google.com/drive/folders/1EmHGNSF0bQZRV81pTdtoZ-Oa3wCCNZNn?usp=sharing"}
]
def generar_qr_personalizado(nombre, link):
    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Nivel L es suficiente para enlaces
        box_size=15, # Tamaño del píxel del QR
        border=3,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Crear la imagen del QR (usando el color personalizado)
    img_qr = qr.make_image(fill_color=COLOR_QR, back_color="white").convert('RGB')
    
    ancho_qr, alto_qr = img_qr.size
    
    # Crear un espacio debajo para el nombre
    ESPACIO_TEXTO = 60
    nueva_imagen = Image.new('RGB', (ancho_qr, alto_qr + ESPACIO_TEXTO), "white")
    nueva_imagen.paste(img_qr, (0, 0))
    
    # Añadir un borde simple redondeado a todo el conjunto
    nueva_imagen = ImageOps.expand(nueva_imagen, border=5, fill=COLOR_TEXTO)

    # Preparar el lienzo de dibujo
    draw = ImageDraw.Draw(nueva_imagen)
    
    # Cargar la fuente
    try:
        font = ImageFont.truetype(FUENTE_RUTA, 30)
    except:
        font = ImageFont.load_default(size=20)
        
    # Calcular ancho y alto del texto para centrarlo
    # Usamos textbbox para Pillow moderno
    text_bbox = draw.textbbox((0, 0), nombre, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    # Posicionar el texto centrado debajo del QR
    x_texto = (nueva_imagen.width - text_width) / 2
    y_texto = alto_qr + 15
    
    # Dibujar el nombre
    draw.text((x_texto, y_texto), nombre, fill=COLOR_TEXTO, font=font)
    
    # Guardar la imagen final
    nueva_imagen.save(f"QR_ESCOLAR_{nombre}.png")
    print(f"✅ Generado con éxito: QR_ESCOLAR_{nombre}.png")

# Ejecutar el proceso con los datos de prueba
print("--- INICIANDO PRUEBA DE GENERACIÓN (con datos de ejemplo) ---")
for nino in datos_ninos:
    generar_qr_personalizado(nino['nombre'], nino['link'])
print("--- PRUEBA FINALIZADA. REVISA LOS ARCHIVOS PNG GENERADOS ---")