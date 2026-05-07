import streamlit as st
import base64
import os

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="¡Feliz Día de la Madre!",
    page_icon="❤️",
    layout="centered",         # 'centered' limita el ancho máximo (~730 px)
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def obtener_base64(ruta_archivo: str) -> str:
    """Convierte un archivo binario a cadena base64."""
    with open(ruta_archivo, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ─────────────────────────────────────────────
#  ESTILOS GLOBALES  (Mobile-First)
# ─────────────────────────────────────────────
def inyectar_estilos(img_base64: str | None = None) -> None:
    """
    Inyecta todos los estilos CSS una sola vez.
    Separar CSS del HTML mejora la legibilidad y evita duplicar <style>.
    """

    # Fondo: imagen si existe, degradado de respaldo si no
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
           top center: el borde superior de la imagen siempre
           coincide con el borde superior del viewport.
           Esto hace que la posición de cada zona de la imagen
           sea predecible sin importar el tamaño de pantalla. */
        .stApp {{
            background: {fondo_css} top center / cover no-repeat;
            background-attachment: scroll; /* 'fixed' rompe en iOS Safari */
        }}

        /* ─────────────────────────────────────────
           CONTENEDOR PRINCIPAL — apunta a la zona
           blanca vacía de la imagen (~42 % – 77 %).

           padding-top: 44vh  → empieza justo debajo
           del título "Feliz Día Mamita" (~42 % altura).
           max-height: 33vh   → no se desborda hacia
           las flores inferiores (~77 % altura).
        ───────────────────────────────────────── */
        .block-container {{
            padding-top: 44vh !important;
            padding-bottom: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            text-align: center;
            z-index: 10;
            max-width: 420px !important;
            margin: 0 auto !important;
        }}

        /* En pantallas más pequeñas (< 380 px de alto,
           p.ej. iPhone SE horizontal) bajamos un poco */
        @media (max-height: 600px) {{
            .block-container {{
                padding-top: 40vh !important;
            }}
        }}

        /* Tablet / desktop: la imagen deja más aire */
        @media (min-width: 600px) {{
            .block-container {{
                padding-top: 46vh !important;
                max-width: 520px !important;
            }}
        }}

        /* ── TARJETA — sin fondo, la imagen ya es blanca ahí ── */
        .tarjeta {{
            background: transparent;
            padding: 0 8px 12px;
            margin-bottom: 4px;
        }}

        /* ── NOMBRE DEL NIÑO ── */
        .texto-nino {{
            color: #c2185b;
            font-size: clamp(18px, 5.5vw, 26px);
            font-weight: 700;
            margin-bottom: 6px;
            line-height: 1.3;
        }}

        /* ── FRASE POÉTICA ── */
        .frase-poetica {{
            color: #880e4f;
            font-size: clamp(12px, 3.8vw, 15px);
            font-style: italic;
            margin-top: 6px;
            margin-bottom: 2px;
            line-height: 1.5;
        }}

        /* ── BOTÓN DE DESCARGA ──
           Streamlit genera un <a> dentro de un div con
           data-testid="stDownloadButton".
           Lo sobreescribimos para que ocupe todo el ancho
           disponible y sea fácil de tocar en móvil. */
        div[data-testid="stDownloadButton"] {{
            display: flex;
            justify-content: center;
            margin-top: 8px;
        }}

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stDownloadButton"] > a {{
            background: linear-gradient(135deg, #e91e8c, #f06292) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 14px 32px !important;      /* área de toque generosa */
            font-size: clamp(14px, 4vw, 16px) !important;
            font-weight: 600 !important;
            width: 100% !important;             /* ancho completo en móvil */
            max-width: 320px !important;
            cursor: pointer !important;
            box-shadow: 0 4px 20px rgba(233, 30, 140, 0.35) !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
            text-align: center !important;
            display: block !important;
        }}

        div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stDownloadButton"] > a:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 24px rgba(233, 30, 140, 0.5) !important;
        }}

        /* ── REPRODUCTOR DE AUDIO ── */
        audio {{
            width: 100% !important;
            border-radius: 12px;
            margin-top: 6px;
            margin-bottom: 0;
        }}

        /* Streamlit envuelve st.audio en stAudio */
        div[data-testid="stAudio"] {{
            margin-top: 4px !important;
            margin-bottom: 0 !important;
        }}

        /* ── MENSAJE ERROR / WARNING ── */
        div[data-testid="stAlert"] {{
            border-radius: 12px;
        }}

        /* ─────────────────────────────────────────
           ANIMACIÓN DE CORAZONES FLOTANTES
        ───────────────────────────────────────── */
        @keyframes lluvia {{
            0%   {{ transform: translateY(-10vh) scale(0.5); opacity: 0.8; }}
            100% {{ transform: translateY(105vh)  scale(1.2); opacity: 0; }}
        }}

        .corazon {{
            position: fixed;          /* fixed > absolute para no desplazar layout */
            pointer-events: none;     /* no interfiere con clics del usuario */
            font-size: 22px;
            animation: lluvia linear infinite;
            z-index: 0;
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
#  CORAZONES FLOTANTES  (HTML separado del CSS)
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
#  LÓGICA PRINCIPAL
# ─────────────────────────────────────────────
def main() -> None:
    # 1. Cargar imagen de fondo (opcional)
    img_b64 = None
    try:
        img_b64 = obtener_base64("dia_de_la_madre_image.jpg")
    except FileNotFoundError:
        pass  # Se usará el degradado CSS de respaldo

    # 2. Inyectar estilos UNA sola vez
    inyectar_estilos(img_b64)

    # 3. Corazones decorativos (posición fija, no afectan al layout)
    mostrar_corazones()

    # 4. Leer parámetro de URL  (?hijo=sofia)
    parametros = st.query_params
    nombre_nino = parametros.get("hijo", "").strip()

    if nombre_nino:
        # ── Vista personalizada ──────────────────
        nombre_display = nombre_nino.capitalize()

        # Tarjeta de bienvenida
        st.markdown(
            f"""
            <div class="tarjeta">
                <div class="texto-nino">Un mensaje de {nombre_display} 🌸</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Audio
        ruta_audio = f"audios/{nombre_nino.lower()}.m4a"

        if os.path.exists(ruta_audio):
            with open(ruta_audio, "rb") as af:
                audio_bytes = af.read()

            # Reproductor nativo
            st.audio(audio_bytes, format="audio/mp4")

            # Frase poética
            st.markdown(
                '<div class="frase-poetica">'
                '"No hay sonido más dulce que la voz de quien te llama Mamá"'
                "</div>",
                unsafe_allow_html=True,
            )

            # ── BOTÓN DE DESCARGA ──────────────────
            # Se centra automáticamente gracias a los estilos CSS.
            # Usamos st.columns para alinearlo en escritorio también.
            col_izq, col_btn, col_der = st.columns([1, 3, 1])
            with col_btn:
                st.download_button(
                    label="💌 Guardar este hermoso recuerdo",
                    data=audio_bytes,
                    file_name=f"mensaje_de_{nombre_nino.lower()}.m4a",
                    mime="audio/mp4",
                    use_container_width=True,   # ancho del contenedor (col_btn)
                )
        else:
            st.error(f"No se encontró el audio de {nombre_display}.")

    else:
        # ── Vista genérica (sin parámetro) ───────
        st.markdown(
            """
            <div class="tarjeta">
                <div class="texto-nino">¡Feliz Día de la Madre! ❤️</div>
                <div class="frase-poetica">
                    Escanea el código QR de tu hijo/a<br>para ver un mensaje especial.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()