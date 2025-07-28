# Быстрый старт для деплоя на Vercel

## 🚀 Пошаговая инструкция

### 1. Подготовка
```bash
# Установите Vercel CLI
npm install -g vercel

# Войдите в аккаунт
vercel login
```

### 2. Деплой
```bash
# Из корневой папки проекта
vercel

# Ответьте на вопросы:
# - Set up and deploy? → Yes
# - Project name → verb-trainer-bot
# - Directory → ./
```

### 3. Настройка переменных окружения
1. Откройте [Vercel Dashboard](https://vercel.com/dashboard)
2. Найдите ваш проект → Settings → Environment Variables
3. Добавьте:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your_bot_token_here`
   - **Environment**: All (Production, Preview, Development)

### 4. Повторный деплой
```bash
vercel --prod
```

### 5. Установка webhook
```bash
python set_webhook.py
```
Введите URL: `https://your-app-name.vercel.app/api/webhook`

### 6. Готово! 🎉
Ваш бот работает в Telegram!

---

## 🔧 Проверка настроек .env

Ваши текущие настройки .env выглядят правильно:

### ✅ Что настроено корректно:
- `.env` содержит `TELEGRAM_BOT_TOKEN`
- Файл исключен из Git через `.gitignore`
- `config.py` использует стандартный `load_dotenv()`
- Следует стандартным практикам Python проектов

### 📁 Структура файлов:
```
verb_trainer2/
├── api/webhook.py          ✅ Vercel endpoint
├── vercel.json            ✅ Конфигурация Vercel
├── set_webhook.py         ✅ Скрипт установки webhook
├── .env                   ✅ Локальные переменные
├── .env.example          ✅ Пример настроек
└── .gitignore            ✅ Исключает конфиденциальные файлы
```

## 🐛 Отладка

### Проверить webhook:
```bash
python set_webhook.py
```

### Посмотреть логи:
```bash
vercel logs your-app-name
```

### Проблемы с токеном:
- Убедитесь, что токен добавлен в Vercel Dashboard
- Проверьте, что выполнен `vercel --prod` после добавления переменных
