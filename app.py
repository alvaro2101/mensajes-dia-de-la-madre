import streamlit as st
import os

st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="wide")

# CSS Mágico para montar el audio sobre la imagen
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding: 0rem;
        max-width: 100%; 
        text-align: center;
    }
    
    /* Esta es la magia para subir el texto y el audio sobre la imagen */
    .contenedor-flotante {
        margin-top: -45vh; /* AJUSTA ESTE NÚMERO: hazlo más grande (ej. -50vh) para subirlo más, o más pequeño (ej. -30vh) para bajarlo */
        position: relative;
        z-index: 10;
        padding: 0 20px;
    }
    
    /* Estilo para que el nombre resalte sobre el fondo blanco */
    .texto-nino {
        color: #d81b60; /* Color rosado oscuro */
        font-size: 26px;
        font-weight: bold;
        text-shadow: 1px 1px 2px white;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    # 1. Ponemos la imagen primero para que quede de "fondo"
    try:
        st.image("dia_de_la_madre_image.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Recuerda colocar tu imagen.")
        
    # 2. Abrimos el contenedor flotante que se subirá con CSS
    st.markdown('<div class="contenedor-flotante">', unsafe_allow_html=True)
    
    # El texto personalizado
    st.markdown(f'<div class="texto-nino">Un mensaje de {nombre_nino.capitalize()} ❤️</div>', unsafe_allow_html=True)
    
    # 3. El reproductor de audio
    ruta_audio = f"audios/{nombre_nino.lower()}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")
        
    # Cerramos el contenedor
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Por favor, escanea el código QR para ver tu sorpresa.")