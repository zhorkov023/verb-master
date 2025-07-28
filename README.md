# Spanish Verb Conjugation Telegram Bot

A Telegram bot for practicing Spanish verb conjugations with Russian verb translations and organized tense groups.

## Features

- **Multiple tense group selection**: Choose one or multiple groups of tenses to practice
- **Russian verb translations**: Spanish verbs translated to Russian for context
- **Continuous practice mode**: Keeps asking questions until you stop
- **40+ common Spanish verbs**: Comprehensive verb database
- **Multiple tenses**: Presente, Pretérito Perfecto, Pretérito Imperfecto, Pretérito Indefinido, Condicional, Futuro
- **All persons**: yo, tú, él/ella, nosotros, vosotros, ellos/ellas
- **Accent-tolerant**: Accepts answers with or without accents
- **Instant feedback**: Shows correct answers with verb translations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the bot token you receive

### 3. Set Bot Token

Create a file `settings/config.env` and add your bot token:

```bash
mkdir -p settings
echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > settings/config.env
```

Replace `your_bot_token_here` with the actual token from BotFather.

**Alternative: Environment Variable**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

### 4. Run the Bot

```bash
python main.py
```

## Usage

### Bot Commands

- `/start` - Welcome message and instructions
- `/practice` - Start a new conjugation challenge
- `/help` - Show help information

### Tense Groups

The bot organizes tenses into logical groups:

1. **Настоящее время (Presente)** - Present tense only
2. **Прошедшие времена (Tiempos Pasados)** - All past tenses
3. **Будущее и условное (Futuro y Condicional)** - Future and conditional
4. **Все времена (Todos los tiempos)** - All tenses mixed

### Example Interaction

```
User: /practice
Bot: 🎯 Selecciona tiempos para practicar:
     
     Seleccionado: Nada seleccionado
     
     ☐ Presente
     ☐ Tiempos Pasados  
     ☐ Futuro y Condicional
     [🎯 Empezar práctica] [🔄 Resetear]

User: [Clicks "Presente" and "Tiempos Pasados"]
Bot: 🎯 Selecciona tiempos para practicar:
     
     Seleccionado: Presente, Tiempos Pasados
     
     ✅ Presente
     ✅ Tiempos Pasados
     ☐ Futuro y Condicional
     [🎯 Empezar práctica] [🔄 Resetear]

User: [Clicks "🎯 Empezar práctica"]
Bot: 🔤 Conjugar el verbo:
     hablar (говорить) en Presente para tú
     Escribe tu respuesta:

User: hablas
Bot: ¡Correcto! ✅
     hablar (говорить) → hablas
     
     Siguiente pregunta:
     🔤 Conjugar el verbo:
     comer (есть) en Pretérito Perfecto para nosotros
     Escribe tu respuesta:

User: [Clicks "🛑 Parar práctica"]
Bot: 🛑 Práctica detenida. Usa /practice para empezar de nuevo.
```

## Project Structure

```
verb_trainer2/
├── main.py                 # Main application entry point
├── config.py               # Configuration settings and messages
├── verb_engine.py          # Core logic for verb challenges
├── bot_handlers.py         # Telegram bot command handlers
├── verbs_data.json         # Database of Spanish verbs and conjugations
├── verb_translations.json  # Russian translations for Spanish verbs
├── requirements.txt        # Python dependencies
├── test_bot.py            # Test suite for bot functionality
└── README.md              # This file
```

## Verb Database

The bot includes 40+ common Spanish verbs with complete conjugations for:

- **Presente**: hablo, hablas, habla, hablamos, habláis, hablan
- **Pretérito Perfecto**: he hablado, has hablado, ha hablado, etc.
- **Pretérito Imperfecto**: hablaba, hablabas, hablaba, etc.
- **Pretérito Indefinido**: hablé, hablaste, habló, etc.
- **Condicional**: hablaría, hablarías, hablaría, etc.
- **Futuro**: hablaré, hablarás, hablará, etc.

## Adding More Verbs

To add more verbs, edit `verbs_data.json` following the existing format:

```json
{
  "new_verb": {
    "presente": ["conjugation1", "conjugation2", "conjugation3", "conjugation4", "conjugation5", "conjugation6"],
    "preterito_perfecto": ["he conjugated", "has conjugated", "ha conjugated", "hemos conjugated", "habéis conjugated", "han conjugated"],
    "preterito_imperfecto": ["conjugation1", "conjugation2", "conjugation3", "conjugation4", "conjugation5", "conjugation6"],
    "preterito_indefinido": ["conjugation1", "conjugation2", "conjugation3", "conjugation4", "conjugation5", "conjugation6"],
    "condicional": ["conjugation1", "conjugation2", "conjugation3", "conjugation4", "conjugation5", "conjugation6"],
    "futuro": ["conjugation1", "conjugation2", "conjugation3", "conjugation4", "conjugation5", "conjugation6"]
  }
}
```

## Troubleshooting

### Bot doesn't respond
- Check that your bot token is correctly set
- Ensure the bot is running (`python main.py`)
- Check the console for error messages

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're in the correct directory

### JSON errors
- Validate your `verbs_data.json` file if you've made changes
- Check for missing commas or brackets

## License

This project is open source and available under the MIT License.
