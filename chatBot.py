import streamlit as st
from dotenv import load_dotenv
import os
import time
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.conversations import ConversationAnalysisClient
from datetime import datetime, timedelta, date, timezone

# Cargar variables de entorno
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')
ls_prediction_endpoint = os.getenv('LS_CONVERSATIONS_ENDPOINT')
ls_prediction_key = os.getenv('LS_CONVERSATIONS_KEY')

# Crear clientes de Azure
qa_credential = AzureKeyCredential(ai_key)
qa_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=qa_credential)

conv_credential = AzureKeyCredential(ls_prediction_key)
conv_client = ConversationAnalysisClient(endpoint=ls_prediction_endpoint, credential=conv_credential)

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
    "Dime el ranking actual de Rafael Nadal",
    "¿Que torneo se juega en hieva?",
    "¿Cuantos titulos tiene Serena Williams?",
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
            # Obtener respuesta de Azure QnA
            response = qa_client.get_answers(
                question=user_question,
                project_name=ai_project_name,
                deployment_name=ai_deployment_name
            )

            # Obtener categoría de la pregunta usando Conversation Analysis
            conv_result = conv_client.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": user_question
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": 'Clock',
                        "deploymentName": 'tenis',
                        "verbose": True
                    }
                }
            )

            # Obtener la intención principal y las entidades
            top_intent = conv_result["result"]["prediction"]["topIntent"]
            entities = conv_result["result"]["prediction"]["entities"]

            # Agregar la respuesta del QnA al historial
            if response.answers:
                for candidate in response.answers:
                    st.session_state.history.append(('bot', f"🤖 {candidate.answer}"))
            else:
                st.session_state.history.append(('bot', "🎾 No encontré información sobre eso. ¿Podrías reformular la pregunta?"))

            # Construir el mensaje de categoría y entidades
            category_message = f"🔍 Categoría: <strong>{top_intent}</strong>\n\n"

            if entities:
                for entity in entities:
                    category_message += f"- **Entidad:** {entity['category']}  \n"
                    category_message += f"-  **Texto:** {entity['text']}  \n"
                    category_message += f" - **Posición:** {entity['offset']} - {entity['offset'] + entity['length']}  \n"
                    category_message += f" - **Confianza:** {entity['confidenceScore']:.2f}  \n\n"

                # Agregar el mensaje de categoría al historial
                if top_intent == "Get Jugador" and entities:
                    # Suponiendo que el nombre del jugador está en la entidad correspondiente
                    jugador_entity = next((entity for entity in entities if entity['category'] == "nombre jugador"), None)
                    
                    if jugador_entity:
                        jugador_nombre = jugador_entity['text'].replace(" ", "_")  # Reemplazar espacios por guiones bajos para la URL
                        wiki_url = f"https://es.wikipedia.org/wiki/{jugador_nombre}"  # URL de Wikipedia
                        # Mensaje con enlace a Wikipedia
                        st.session_state.history.append(('bot', f" {category_message}\n\n🔗 Puedes ver más información sobre {jugador_nombre} [aquí]({wiki_url})."))
                    else:
                        st.session_state.history.append(('bot', f"🔍 {category_message}"))


        except Exception as e:
            st.session_state.history.append(('bot', f"🚨 Ocurrió un error: {str(e)}"))

    # Mostrar el historial del chat
    for role, message in st.session_state.history:
        if role == 'user':
            st.markdown(f'<div class="message user-message">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message bot-message">{message}</div>', unsafe_allow_html=True)

    # Mantener el contenedor de mensajes al final
    message_container.markdown('</div>', unsafe_allow_html=True)
