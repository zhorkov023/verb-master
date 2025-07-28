import os

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Verb practice settings
PERSONS = {
    0: "yo",
    1: "tú", 
    2: "él/ella",
    3: "nosotros",
    4: "vosotros",
    5: "ellos/ellas"
}

PERSONS_RUSSIAN = {
    0: "я",
    1: "ты", 
    2: "он/она",
    3: "мы",
    4: "вы",
    5: "они"
}

TENSES = {
    "presente": "Presente",
    "preterito_perfecto": "Pretérito Perfecto",
    "preterito_imperfecto": "Pretérito Imperfecto",
    "preterito_indefinido": "Pretérito Indefinido",
    "condicional": "Condicional",
    "futuro": "Futuro"
}

TENSES_RUSSIAN = {
    "presente": "Настоящее время",
    "preterito_perfecto": "Прошедшее совершенное",
    "preterito_imperfecto": "Прошедшее несовершенное",
    "preterito_indefinido": "Простое прошедшее",
    "condicional": "Условное наклонение",
    "futuro": "Будущее время"
}

# Tense groups for practice selection
TENSE_GROUPS = {
    "present": {
        "name": "Настоящее время",
        "name_es": "Presente",
        "tenses": ["presente"]
    },
    "past": {
        "name": "Прошедшие времена",
        "name_es": "Tiempos Pasados",
        "tenses": ["preterito_perfecto", "preterito_imperfecto", "preterito_indefinido"]
    },
    "future_conditional": {
        "name": "Будущее и условное",
        "name_es": "Futuro y Condicional",
        "tenses": ["futuro", "condicional"]
    },
    "all": {
        "name": "Все времена",
        "name_es": "Todos los tiempos",
        "tenses": ["presente", "preterito_perfecto", "preterito_imperfecto", "preterito_indefinido", "condicional", "futuro"]
    }
}

# Messages
WELCOME_MESSAGE = """
¡Hola! 👋 Soy tu entrenador de verbos españoles.

Comandos disponibles:
/start - Mostrar este mensaje
/practice - Practicar conjugaciones
/help - Ayuda

¡Empecemos a practicar! Usa /practice para comenzar.
"""

HELP_MESSAGE = """
🔤 **Cómo usar el bot:**

1. Usa /practice para comenzar
2. Selecciona grupos de tiempos para estudiar
3. Te daré un verbo en infinitivo y te pediré que lo conjugues
4. Escribe tu respuesta
5. Te diré si es correcta y continuaremos con una nueva pregunta

**Ejemplo:**
Bot: Conjugar "hablar" (говорить) en Presente para "tú"
Tú: hablas
Bot: ¡Correcto! ✅

¡Buena suerte! 🍀

**Características:**
- Las respuestas se aceptan con y sin acentos
- La práctica continúa automáticamente hasta que la detengas
- Usa el botón "🛑 Parar práctica" para terminar
"""
