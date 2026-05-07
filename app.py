import streamlit as st
import base64
import os

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="¡Feliz Día de la Madre!",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def obtener_base64(ruta_archivo: str) -> str:
    with open(ruta_archivo, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ─────────────────────────────────────────────
#  ESTILOS GLOBALES
# ─────────────────────────────────────────────
def inyectar_estilos(img_base64: str | None = None) -> None:

    fondo_css = (
        f'url("data:image/jpg;base64,{img_base64}")'
        if img_base64
        else "linear-gradient(135deg, #ffe0ec 0%, #ffd6e8 50%, #ffb3d1 100%)"
    )

    st.markdown(
        f"""
        <style>
        /* ── RESET STREAMLIT ── */
        #MainMenu, header, footer {{ visibility: hidden; }}

        /* ── FONDO ──
           top center: la parte superior de la imagen siempre
           queda fija en el tope del viewport. Asi el padding-top
           apunta siempre a la misma zona de la imagen. */
        .stApp {{
            background: {fondo_css} top center / cover no-repeat;
            background-attachment: scroll;   /* 'fixed' rompe en iOS Safari */
        }}

        /* ─────────────────────────────────────────
           CONTENEDOR PRINCIPAL
           ─────────────────────────────────────────
           Medicion real de la captura (Android):
             Zona blanca de la imagen: ~42% a ~74% del alto
             padding-top = 40vh empieza justo debajo del titulo
             El bloque completo mide ~26vh y termina en ~66vh,
             bien antes de las flores inferiores (~74vh)
        ───────────────────────────────────────── */
        .block-container {{
            padding-top:    40vh !important;
            padding-bottom: 0    !important;
            padding-left:   1rem !important;
            padding-right:  1rem !important;
            text-align: center;
            z-index: 10;
            max-width: 400px !important;
            margin: 0 auto !important;
        }}

        /* Tablet / desktop */
        @media (min-width: 600px) {{
            .block-container {{
                padding-top: 43vh !important;
                max-width: 500px !important;
            }}
        }}

        /* ── ELIMINAR margenes internos de Streamlit ──
           Cada st.audio, st.markdown y st.columns agrega ~1rem
           de separacion vertical. Lo forzamos a cero para que
           el bloque sea lo mas compacto posible. */
        div[data-testid="stVerticalBlock"] > div,
        div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            gap: 0 !important;
            row-gap: 0 !important;
        }}
        .element-container {{
            margin-top:    0 !important;
            margin-bottom: 0 !important;
        }}

        /* ── TARJETA — fondo transparente (zona ya es blanca) ── */
        .tarjeta {{
            background:    transparent;
            padding:       0 8px 4px;
            margin-bottom: 0;
        }}

        /* ── NOMBRE DEL NINO ── */
        .texto-nino {{
            color:         #c2185b;
            font-size:     clamp(17px, 5vw, 24px);
            font-weight:   700;
            margin-bottom: 0;
            line-height:   1.3;
        }}

        /* ── FRASE POETICA ── */
        .frase-poetica {{
            color:         #880e4f;
            font-size:     clamp(11px, 3.5vw, 14px);
            font-style:    italic;
            margin-top:    3px;
            margin-bottom: 0;
            line-height:   1.4;
        }}

        /* ── REPRODUCTOR DE AUDIO ── */
        div[data-testid="stAudio"] {{
            margin-top:    4px !important;
            margin-bottom: 0   !important;
        }}
        audio {{
            width:         100%  !important;
            border-radius: 10px;
            margin-top:    0;
            margin-bottom: 0;
        }}

        /* ── BOTON DE DESCARGA ── */
        div[data-testid="stDownloadButton"] {{
            display:         flex;
            justify-content: center;
            margin-top:      6px  !important;
            margin-bottom:   0    !important;
        }}

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stDownloadButton"] > a {{
            background:    linear-gradient(135deg, #e91e8c, #f06292) !important;
            color:         white    !important;
            border:        none     !important;
            border-radius: 50px    !important;
            padding:       11px 28px !important;
            font-size:     clamp(13px, 4vw, 15px) !important;
            font-weight:   600     !important;
            width:         100%    !important;
            max-width:     300px   !important;
            cursor:        pointer  !important;
            box-shadow:    0 4px 18px rgba(233, 30, 140, 0.35) !important;
            transition:    transform 0.15s, box-shadow 0.15s   !important;
            text-align:    center   !important;
            display:       block    !important;
        }}

        div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stDownloadButton"] > a:hover {{
            transform:  translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(233, 30, 140, 0.5) !important;
        }}

        /* ── COLUMNAS para centrar el boton ── */
        div[data-testid="stHorizontalBlock"] {{
            gap:           0 !important;
            margin-top:    0 !important;
            margin-bottom: 0 !important;
        }}

        /* ── ALERTAS ── */
        div[data-testid="stAlert"] {{
            border-radius: 12px;
        }}

        /* ─────────────────────────────────────────
           CORAZONES FLOTANTES
        ───────────────────────────────────────── */
        @keyframes lluvia {{
            0%   {{ transform: translateY(-10vh) scale(0.5); opacity: 0.9; }}
            100% {{ transform: translateY(105vh) scale(1.2); opacity: 0;   }}
        }}

        .corazon {{
            position:       fixed;
            pointer-events: none;
            font-size:      20px;
            animation:      lluvia linear infinite;
            z-index:        0;
        }}
        .c1 {{ left: 8%;  animation-duration: 5.0s; animation-delay: 0.0s; }}
        .c2 {{ left: 25%; animation-duration: 7.0s; animation-delay: 1.0s; }}
        .c3 {{ left: 45%; animation-duration: 6.0s; animation-delay: 2.5s; }}
        .c4 {{ left: 68%; animation-duration: 8.0s; animation-delay: 0.5s; }}
        .c5 {{ left: 88%; animation-duration: 5.5s; animation-delay: 1.5s; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  CORAZONES FLOTANTES
# ─────────────────────────────────────────────
def mostrar_corazones() -> None:
    st.markdown(
        """
        <div class="corazon c1">❤️</div>
        <div class="corazon c2">🌸</div>
        <div class="corazon c3">🌺</div>
        <div class="corazon c4">💗</div>
        <div class="corazon c5">💕</div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  LOGICA PRINCIPAL
# ─────────────────────────────────────────────
def main() -> None:
    # 1. Fondo
    img_b64 = None
    try:
        img_b64 = obtener_base64("dia_de_la_madre_image.jpg")
    except FileNotFoundError:
        pass

    # 2. Estilos (una sola vez)
    inyectar_estilos(img_b64)

    # 3. Corazones decorativos
    mostrar_corazones()

    # 4. Parametro de URL  ?hijo=sofia
    parametros  = st.query_params
    nombre_nino = parametros.get("hijo", "").strip()

    if nombre_nino:
        nombre_display = nombre_nino.capitalize()

        # Nombre
        st.markdown(
            f'<div class="tarjeta">'
            f'<div class="texto-nino">Un mensaje de {nombre_display} 🌸</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Audio
        ruta_audio = f"audios/{nombre_nino.lower()}.m4a"

        if os.path.exists(ruta_audio):
            with open(ruta_audio, "rb") as af:
                audio_bytes = af.read()

            st.audio(audio_bytes, format="audio/mp4")

            # Frase
            st.markdown(
                '<div class="frase-poetica">'
                '"No hay sonido mas dulce que la voz de quien te llama Mama"'
                '</div>',
                unsafe_allow_html=True,
            )

            # Boton centrado con columnas
            _, col_btn, _ = st.columns([1, 3, 1])
            with col_btn:
                st.download_button(
                    label="💌 Guardar este hermoso recuerdo",
                    data=audio_bytes,
                    file_name=f"mensaje_de_{nombre_nino.lower()}.m4a",
                    mime="audio/mp4",
                    use_container_width=True,
                )
        else:
            st.error(f"No se encontro el audio de {nombre_display}.")

    else:
        # Vista sin parametro
        st.markdown(
            '<div class="tarjeta">'
            '<div class="texto-nino">¡Feliz Dia de la Madre! ❤️</div>'
            '<div class="frase-poetica">'
            'Escanea el codigo QR de tu hijo/a<br>para ver su mensaje especial.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()