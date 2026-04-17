import streamlit as st
import base64
import os

st.set_page_config(page_title="¡Feliz Día de la Madre!", page_icon="❤️", layout="centered")

def obtener_base64(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = obtener_base64("dia_de_la_madre_image.jpg")
    
    st.markdown(f"""
        <style>
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            overflow: hidden; /* Evita barras de desplazamiento */
        }}
        
        .block-container {{
            padding-top: 55vh; 
            text-align: center;
            z-index: 10;
        }}
        
        .texto-nino {{
            color: #d81b60;
            font-size: 28px; /* Un poquito más grande */
            font-weight: bold;
            text-shadow: 2px 2px 4px white, -2px -2px 4px white, 2px -2px 4px white, -2px 2px 4px white;
            margin-bottom: 10px;
        }}
        
        .frase-poetica {{
            color: #d81b60;
            font-size: 16px;
            font-style: italic;
            text-shadow: 1px 1px 3px white;
            margin-top: 10px;
            margin-bottom: 20px;
        }}
        
        /* --- MAGIA: ANIMACIÓN DE CORAZONES --- */
        @keyframes lluvia {{
            0% {{ transform: translateY(-10vh) scale(0.5); opacity: 0.8; }}
            100% {{ transform: translateY(100vh) scale(1.2); opacity: 0; }}
        }}
        .corazon {{
            position: absolute;
            color: #ff4d6d;
            font-size: 20px;
            animation: lluvia linear infinite;
            z-index: 1;
        }}
        .c1 {{ left: 15%; animation-duration: 5s; animation-delay: 0s; }}
        .c2 {{ left: 35%; animation-duration: 7s; animation-delay: 1s; }}
        .c3 {{ left: 55%; animation-duration: 6s; animation-delay: 2.5s; }}
        .c4 {{ left: 75%; animation-duration: 8s; animation-delay: 0.5s; }}
        .c5 {{ left: 90%; animation-duration: 5.5s; animation-delay: 1.5s; }}
        </style>
        
        <div class="corazon c1">❤️</div>
        <div class="corazon c2">💖</div>
        <div class="corazon c3">🌸</div>
        <div class="corazon c4">❤️</div>
        <div class="corazon c5">💕</div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ No se encontró la imagen.")

parametros = st.query_params

if "hijo" in parametros:
    nombre_nino = parametros["hijo"]
    
    st.markdown(f'<div class="texto-nino">Un mensaje de {nombre_nino.capitalize()}</div>', unsafe_allow_html=True)
    
    ruta_audio = f"audios/{nombre_nino.lower()}.mp3"
    
    if os.path.exists(ruta_audio):
        audio_file = open(ruta_audio, 'rb')
        audio_bytes = audio_file.read()
        
        # El reproductor de siempre
        st.audio(audio_bytes, format='audio/mp3')
        
        # La frase bonita debajo
        st.markdown('<div class="frase-poetica">"No hay sonido más dulce que la voz de quien te llama Mamá"</div>', unsafe_allow_html=True)
        
        # Botón para descargar el audio
        st.download_button(
            label="📥 Guardar este hermoso recuerdo",
            data=audio_bytes,
            file_name=f"mensaje_de_{nombre_nino}.mp3",
            mime="audio/mp3"
        )
    else:
        st.error(f"No se encontró el audio de {nombre_nino}.")

else:
    st.markdown('<div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">Por favor, escanea el código QR para ver tu sorpresa.</div>', unsafe_allow_html=True)