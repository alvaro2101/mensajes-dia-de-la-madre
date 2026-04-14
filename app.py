import streamlit as st
import os

# 1. Configuración básica de la página
st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="centered")

# 2. Mostrar la imagen general (cambia "imagen_madre.jpg" por el nombre de tu foto)
try:
    st.image("dia_de_la_madre_image.jpg", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Recuerda colocar tu imagen en la carpeta y verificar que el nombre coincida en el código.")

st.title("Un mensaje muy especial para ti ❤️")

# 3. Leer la URL para saber de qué niño es el QR
parametros = st.query_params

# Comprobamos si la URL tiene el parámetro "hijo"
if "hijo" in parametros:
    # Obtenemos el nombre del niño desde el enlace
    nombre_nino = parametros["hijo"]
    
    st.subheader(f"Tienes un mensaje de voz de {nombre_nino.capitalize()} 💌")
    
    # 4. Buscar y reproducir el audio correspondiente
    # IMPORTANTE: Los audios deben llamarse exactamente igual que el parámetro en minúsculas (ej: juan.mp3)
    ruta_audio = f"audios/{nombre_nino}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}. Revisa que esté en la carpeta 'audios'.")

else:
    # Este mensaje se muestra si alguien entra a la página web sin usar un QR
    st.info("Por favor, escanea el código QR que te entregamos para escuchar el mensaje de tu pequeño.")