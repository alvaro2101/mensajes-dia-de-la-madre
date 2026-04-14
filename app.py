import streamlit as st
import os

# 1. Configuración de página
st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="centered")

# 2. CSS personalizado para diseño de "pantalla completa" en móviles
st.markdown("""
    <style>
    /* Ocultar el menú superior, header y footer por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Quitar los márgenes para que la imagen ocupe todo el ancho */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        text-align: center;
    }
    
    /* Pequeño margen para el reproductor de audio */
    .stAudio {
        margin-top: 20px;
        padding: 0px 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Leer la URL para saber de qué niño es el QR
parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    # 4. Mostrar la imagen principal ocupando el máximo ancho
    try:
        st.image("dia_de_la_madre_image.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Recuerda colocar tu imagen_madre.jpg en la carpeta.")
        
    st.markdown(f"### Un mensaje de {nombre_nino.capitalize()} ❤️")
    
    # 5. Reproductor de audio
    ruta_audio = f"audios/{nombre_nino}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")

else:
    st.info("Por favor, escanea el código QR para ver tu sorpresa.")