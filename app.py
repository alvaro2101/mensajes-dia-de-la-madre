import streamlit as st
import os

st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding: 0rem;
        max-width: 100%; 
        text-align: center;
        overflow: hidden; /* Evita que la página haga scroll extra */
    }
    
    /* 1. Subimos el texto hacia la zona blanca */
    .texto-nino {
        color: #d81b60; /* Rosado oscuro para que resalte */
        font-size: 26px;
        font-weight: bold;
        text-shadow: 1px 1px 2px white;
        margin-top: -65vh; /* 🔥 AJUSTA ESTE NÚMERO: -60vh, -50vh para subir o bajar el texto */
        position: relative;
        z-index: 10;
    }
    
    /* 2. Forzamos al reproductor de audio a subir con el texto */
    [data-testid="stAudio"] {
        position: relative;
        z-index: 10;
        width: 80%; /* Lo hace un poco más estrecho y elegante */
        margin: 10px auto 0px auto; /* Lo centra perfectamente debajo del texto */
        padding-bottom: 60vh; /* Da espacio virtual abajo para que se mantenga arriba */
    }
    </style>
    """, unsafe_allow_html=True)

parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    # Ponemos la imagen de fondo primero
    try:
        st.image("dia_de_la_madre_image.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Recuerda colocar tu imagen.")
        
    # Colocamos el texto
    st.markdown(f'<div class="texto-nino">Un mensaje de {nombre_nino.capitalize()} ❤️</div>', unsafe_allow_html=True)
    
    # Colocamos el audio
    ruta_audio = f"audios/{nombre_nino.lower()}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")

else:
    st.info("Por favor, escanea el código QR para ver tu sorpresa.")