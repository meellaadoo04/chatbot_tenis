# Chatbot Master´s tenis

He creado este chatbot entrenado con preguntas y respuestas sobre tenis sobre Azure Language Studio mediante el leguaje de python y libreria streamlit. 

Sobre el le podras hacer las preguntas mas basicas como quien es Nadal a preguntas mas tecnicas como que es un ace. De todas maneras ya por defecto te aparecen algunas preguntas que puedes hacerle 

El bot te repondera en base a la pregunta que le hayas relizado ademas de añadirle:
- Intenciones 
- Expresiones
- Entidades
El bot detectara automaticamente estas caracteristicas de la pregunta del usuario gracias a un entrenamiento previo realizado en Azure Languaje Studio que puedes comprobar aqui:
https://language.cognitive.azure.com/clu/projects/Clock/build

### En Local
1. Instalar las dependecias necesarias del requirements.txt
 ```bash
  pip install -r requirements.txt
```

2. Ejecutar el comando para iniciar la aplicacion
 ```bash
  python .\chatBot.py
```

3. Nos dara una url en local a traves de la terminal donde ya podremos acceder a la pagina y accederemos a ella con una interfaz tal que asi:
![image](https://github.com/user-attachments/assets/81f73439-a830-40b0-8628-a4b4ea397183)



### A traves de esta URL 

De esta manera tambien podremos acceder a la pagina a traves de una url que proporciona streamlit

[https://meellaadoo04-chatbot-tenis-chatbot-aypyk3.streamlit.app/](https://meellaadoo04-chatbot-tenis-chatbot-aypyk3.streamlit.app/)


