import streamlit as st
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Cargar variables de entorno
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Crear cliente de Azure
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

# Configurar página
st.set_page_config(page_title="AI Tennis Q&A", page_icon="🎾", layout="centered")


# Subtítulo
st.markdown('<div style="text-align: center; font-size: 24px; color: #4CAF50;">Tu asistente personal para preguntas sobre tenis</div>', unsafe_allow_html=True)


# Título del chat
st.markdown(
    """
    <style>
        .chat-container {
            background-color: #f4f4f4;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: auto;
            margin-top: 1px;
        }

        .chat-title {
            font-size: 55px;  /* Título más grande */
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 30px;
        }

        .message-container {
            max-height: 400px;
            overflow-y: auto;
            padding-right: 20px;
            margin-bottom: 20px;
        }

        .message {
            margin: 10px 0;
            padding: 12px;
            border-radius: 10px;
            max-width: 75%;
            word-wrap: break-word;
        }

        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: 25%;
            align-self: flex-start;
        }

        .bot-message {
            background-color: #e9e9e9;
            color: black;
            margin-right: 25%;
            align-self: flex-end;
        }

        .metadata {
            font-size: 12px;
            color: #888;
            margin-top: 5px;
        }

        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }

        .stTextInput input {
            font-size: 16px;
            padding: 12px;
            border-radius: 25px;
            border: 1px solid #ddd;
            width: 70%;
            margin-right: 10px;
        }

        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 25px;
            padding: 12px 25px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .stButton button:hover {
            background-color: #45a049; /* Cambio al pasar el ratón */
        }

        .stButton button:focus {
            outline: none; /* Quitar el contorno al hacer click */
        }
    </style>
    """, unsafe_allow_html=True
)

# Título
st.markdown('<div class="chat-title">🎾 AI Tennis Assistant</div>', unsafe_allow_html=True)

# Contenedor principal del chat
with st.container():
    #chat_container = st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Historial del chat
    message_container = st.markdown('<div class="message-container">', unsafe_allow_html=True)

    # Campo de entrada centrado
    with st.form(key='question_form'):
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            user_question = st.text_input("Escribe tu pregunta sobre tenis:", key="input", placeholder="¿Cuál es la regla del tie-break en tenis?")
            submit_button = st.form_submit_button(label='Enviar →')

    if submit_button and user_question:
        # Mostrar pregunta del usuario
        st.markdown(f'<div class="message user-message">👤 {user_question}</div>', unsafe_allow_html=True)

        try:
            # Obtener respuesta de Azure
            response = ai_client.get_answers(
                question=user_question,
                project_name=ai_project_name,
                deployment_name=ai_deployment_name
            )

            # Mostrar respuestas
            if response.answers:
                for candidate in response.answers:
                    # Respuesta principal
                    st.markdown(f'<div class="message bot-message">🤖 {candidate.answer}</div>', unsafe_allow_html=True)

                    # Metadatos
                    metadata_html = f"""
                    <div class="metadata">
                        <div>🔍 Confianza: {(candidate.confidence * 100):.1f}%</div>
                        <div>📚 Fuente: {candidate.source}</div>
                    </div>
                    """
                    st.markdown(metadata_html, unsafe_allow_html=True)
            else:
                st.markdown('<div class="message bot-message">🤖 No encontré información sobre eso. ¿Podrías reformular la pregunta?</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error al procesar la pregunta: {str(e)}")

    # Cerrar contenedores HTML
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar message-container
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar chat-container


