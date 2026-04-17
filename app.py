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
        position: relative; /* Esto convierte a la pantalla en nuestro lienzo */
    }
    
    /* 1. Pegatina del TEXTO */
    .contenedor-texto {
        position: absolute;
        top: 60%; /* 🔥 Para subir el texto baja este número (ej. 50%), para bajarlo súbelo (ej. 70%) */
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        text-align: center;
        z-index: 10;
    }
    
    .texto-nino {
        color: #d81b60;
        font-size: 26px;
        font-weight: bold;
        /* Le puse un borde blanco más fuerte por si toca alguna flor de fondo */
        text-shadow: 2px 2px 4px white, -2px -2px 4px white, 2px -2px 4px white, -2px 2px 4px white; 
    }
    
    /* 2. Pegatina del AUDIO */
    div[data-testid="stAudio"] {
        position: absolute;
        top: 70%; /* 🔥 Este debe ser unos 10 números mayor que el del texto para quedar justo debajo */
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    # 1. El lienzo (la imagen)
    try:
        st.image("dia_de_la_madre_image.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Recuerda colocar tu imagen.")
        
    # 2. Imprimimos el texto flotante
    st.markdown(f'<div class="contenedor-texto"><span class="texto-nino">Un mensaje de {nombre_nino.capitalize()} ❤️</span></div>', unsafe_allow_html=True)
    
    # 3. Imprimimos el audio flotante
    ruta_audio = f"audios/{nombre_nino.lower()}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")

else:
    st.info("Por favor, escanea el código QR para ver tu sorpresa.")