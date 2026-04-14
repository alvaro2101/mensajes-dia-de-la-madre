import qrcode
import os

# 1. Asegurarnos de que la carpeta de destino existe
if not os.path.exists("qrs"):
    os.makedirs("qrs")

# 2. Lista con los nombres de los 16 niños
# IMPORTANTE: Escríbelos exactamente igual a como nombrarás sus audios (en minúsculas, sin tildes ni espacios).

nombres_ninos = [
    "antonella", "lia", "thaily", "estrella",
    "mariagracia", "gia", "angel", "emir",
    "leyto", "ivanna", "andrea", "andree",
    "roselyne", "cristofer", "arianna", "joaquin"
] # Reemplaza estos por los nombres reales

# 3. La URL base de tu página web
# OJO: Por ahora usamos localhost para probar en tu computadora. 
# Justo antes de imprimir los QR finales, cambiaremos esto por el enlace real de Streamlit Cloud.
url_base = "http://localhost:8501/?hijo="

print("Generando códigos QR de la clase...")

# 4. Bucle para crear un QR por cada niño
for nombre in nombres_ninos:
    # Construimos el enlace único (ej: http://localhost:8501/?hijo=mateo)
    enlace_personalizado = f"{url_base}{nombre}"
    
    # Generamos la imagen del código QR
    qr = qrcode.make(enlace_personalizado)
    
    # Guardamos la imagen en la carpeta 'qrs'
    ruta_guardado = f"qrs/qr_{nombre}.png"
    qr.save(ruta_guardado)
    
    print(f"✅ QR creado para {nombre} guardado en {ruta_guardado}")

print("¡Proceso terminado exitosamente!")