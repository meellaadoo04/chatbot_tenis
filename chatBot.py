import streamlit as st
from dotenv import load_dotenv
import os
import time
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
            max-width: 100%;
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

        .stTextInput input {
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #4CAF50;            
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
            width: 164px;
            height: 110px;
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

# Título y descripción
st.markdown('<div class="chat-title">🎾 AI Tennis Assistant 🎾</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; font-size: 18px; color: #555; margin-bottom: 30px;">
        Este es un chat especializado en tenis. Puedes hacer preguntas sobre reglas, jugadores, torneos, técnicas y más. ¡Pregúntame lo que quieras saber sobre el mundo del tenis!
    </div>
    """, 
    unsafe_allow_html=True
)

# Preguntas predeterminadas
default_questions = [
    "¿Quien es Roger Federer?",
    "¿Quién tiene más títulos de Grand Slam?",
    "¿Cuanto suelen ganar los tenistas?",
    "¿Qué es un ace en tenis?",
]

# Mostrar preguntas predeterminadas como botones
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: #555; margin-bottom: 20px; ">
        ¿No sabes por dónde empezar? Prueba con estas preguntas:
    </div>
    """, 
    unsafe_allow_html=True
)

# Crear columnas para los botones de preguntas predeterminadas
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])  # 4 columnas para distribuir los botones

# Botones a la izquierda (primeras dos preguntas)
with col1:
    if st.button(default_questions[0], key="default_question_0"):
        st.session_state.input = default_questions[0]  # Autocompletar el campo de entrada
with col2:
    if st.button(default_questions[1], key="default_question_1"):
        st.session_state.input = default_questions[1]  # Autocompletar el campo de entrada

# Botones a la derecha (últimas dos preguntas)
with col3:
    if st.button(default_questions[2], key="default_question_2"):
        st.session_state.input = default_questions[2]  # Autocompletar el campo de entrada
with col4:
    if st.button(default_questions[3], key="default_question_3"):
        st.session_state.input = default_questions[3]  # Autocompletar el campo de entrada

# Inicializar el historial en session_state si no existe
if 'history' not in st.session_state:
    st.session_state.history = []

# Contenedor principal del chat
with st.container():
    # Historial del chat
    message_container = st.markdown('<div class="message-container">', unsafe_allow_html=True)

    # Campo de entrada centrado
    with st.form(key='question_form'):
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            user_question = st.text_input(
                "Escribe tu pregunta sobre tenis:", 
                key="input", 
                placeholder="¿Cuál es la regla del tie-break en tenis?"
            )
            # Botones de enviar y resetear en la misma fila
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_button = st.form_submit_button(label='Enviar →')
            with col2:
                reset_button = st.form_submit_button(label='Resetear Chat')  # Botón de resetear dentro del formulario

                if reset_button:  # Verifica si se presionó el botón de resetear
                    st.session_state.history = []  # Vaciar el historial de la conversación

    if submit_button and user_question:
        # Agregar la pregunta al historial
        st.session_state.history.append(('user', user_question))

        try:
            # Obtener respuesta de Azure
            response = ai_client.get_answers(
                question=user_question,
                project_name=ai_project_name,
                deployment_name=ai_deployment_name
            )

            # Agregar la respuesta al historial
            if response.answers:
                for candidate in response.answers:
                    st.session_state.history.append(('bot', candidate.answer))
            else:
                st.session_state.history.append(('bot', "No encontré información sobre eso. ¿Podrías reformular la pregunta?"))

        except Exception as e:
            st.session_state.history.append(('bot', f"Error al procesar la pregunta: {str(e)}"))

    # Mostrar el historial de preguntas y respuestas con retraso
    for i, (role, message) in enumerate(st.session_state.history):
        if role == 'user':
            st.markdown(f'<div class="message user-message">👤 {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message bot-message">🤖 {message}</div>', unsafe_allow_html=True)

        # Agregar un pequeño retraso entre cada mensaje
        time.sleep(0.5)

    # Cerrar contenedores HTML
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar message-container
    st.markdown('</div>', unsafe_allow_html=True)  # Cerrar chat-container