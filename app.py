import streamlit as st
import base64
import os

st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="centered")

# 1. Función para convertir tu imagen en el fondo de la pantalla
def obtener_base64(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = obtener_base64("dia_de_la_madre_image.jpg")
    
    # CSS para colocar el fondo y ajustar las posiciones
    st.markdown(f"""
        <style>
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Convertimos la imagen en el fondo que cubre todo */
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        /* Empujamos el contenido hacia el centro/abajo de la pantalla */
        .block-container {{
            padding-top: 40vh; /* 🔥 AJUSTA ESTO: 50vh, 60vh etc. para bajar o subir el reproductor */
            text-align: center;
        }}
        
        .texto-nino {{
            color: #d81b60;
            font-size: 26px;
            font-weight: bold;
            text-shadow: 2px 2px 4px white, -2px -2px 4px white, 2px -2px 4px white, -2px 2px 4px white;
            margin-bottom: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ No se encontró 'dia_de_la_madre_image.jpg'.")

# 2. Leemos quién es el niño
parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    # 3. Mostramos el texto
    st.markdown(f'<div class="texto-nino">Un mensaje de {nombre_nino.capitalize()} ❤️</div>', unsafe_allow_html=True)
    
    # 4. Mostramos el audio
    ruta_audio = f"audios/{nombre_nino.lower()}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")

else:
    # Agregamos un fondo blanco al mensaje principal para que se lea bien sobre las flores
    st.markdown('<div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">Por favor, escanea el código QR para ver tu sorpresa.</div>', unsafe_allow_html=True)