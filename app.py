import os
import streamlit as st
import base64
from openai import OpenAI

# ---------- CONFIGURACIÓN DE LA PÁGINA ----------
st.set_page_config(
    page_title="Análisis de Imagen 🤖🏞️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- ESTILOS VISUALES PERSONALIZADOS ----------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        }

        .main {
            background: rgba(255, 255, 255, 0.08);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        h1, h2, h3 {
            color: #E3F2FD;
            text-align: center;
            font-weight: 600;
        }

        .stTextInput > div > div > input {
            background-color: rgba(255,255,255,0.1);
            color: white;
            border-radius: 10px;
        }

        .stFileUploader {
            background-color: rgba(255,255,255,0.1);
            padding: 1rem;
            border-radius: 10px;
        }

        .stButton > button {
            background: linear-gradient(90deg, #00b09b, #96c93d);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #96c93d, #00b09b);
            transform: scale(1.03);
        }

        .stExpander {
            background-color: rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
            color: white !important;
        }

        .stMarkdown {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- FUNCIONES ----------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ---------- INTERFAZ ----------
st.title("🧠 Análisis de Imagen con IA")

ke = st.text_input('🔑 Ingresa tu Clave API')
os.environ['OPENAI_API_KEY'] = ke

api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("📷 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("🖼️ Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

show_details = st.toggle("📝 Agregar detalles adicionales", value=False)

if show_details:
    additional_details = st.text_area(
        "Escribe aquí contexto o detalles sobre la imagen:",
        disabled=not show_details
    )

analyze_button = st.button("🔍 Analizar imagen")

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🧩 Analizando..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe lo que ves en la imagen en español."
        
        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional del usuario:\n{additional_details}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            }
        ]
        
        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    if not uploaded_file and analyze_button:
        st.warning("Por favor, sube una imagen antes de analizar.")
    if not api_key:
        st.warning("Por favor, ingresa tu clave API.")

