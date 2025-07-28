# Деплой Telegram бота на Vercel

## Подготовка к деплою

### 1. Установка Vercel CLI
```bash
npm install -g vercel
```

### 2. Логин в Vercel
```bash
vercel login
```

## Деплой проекта

### 1. Деплой на Vercel
Из корневой папки проекта выполните:
```bash
vercel
```

При первом деплое Vercel спросит:
- **Set up and deploy?** → Yes
- **Which scope?** → Выберите ваш аккаунт
- **Link to existing project?** → No
- **What's your project's name?** → verb-trainer-bot (или любое другое имя)
- **In which directory is your code located?** → ./

### 2. Настройка переменных окружения в Vercel

После успешного деплоя:

1. Зайдите в [Vercel Dashboard](https://vercel.com/dashboard)
2. Найдите ваш проект
3. Перейдите в **Settings** → **Environment Variables**
4. Добавьте переменную:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your_bot_token_here`
   - **Environment**: Production, Preview, Development

### 3. Повторный деплой
После добавления переменных окружения выполните:
```bash
vercel --prod
```

## Настройка Webhook

### 1. Получите URL вашего приложения
После деплоя Vercel покажет URL вашего приложения, например:
```
https://verb-trainer-bot.vercel.app
```

### 2. Установите webhook
Запустите скрипт для установки webhook:
```bash
python set_webhook.py
```

Введите URL в формате:
```
https://your-app-name.vercel.app/api/webhook
```

### 3. Проверка
После установки webhook ваш бот должен работать в Telegram!

## Проверка работы

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Попробуйте команду `/practice`

## Отладка

### Просмотр логов
```bash
vercel logs your-app-name
```

### Проверка webhook
Запустите `set_webhook.py` без параметров, чтобы увидеть текущий статус webhook.

### Проблемы с переменными окружения
Убедитесь, что:
1. Переменная `TELEGRAM_BOT_TOKEN` добавлена в Vercel Dashboard
2. Выполнен повторный деплой после добавления переменных
3. Переменная доступна во всех окружениях (Production, Preview, Development)

## Структура файлов для Vercel

```
verb_trainer2/
├── api/
│   └── webhook.py          # Vercel serverless function
├── .env                    # Локальные переменные (не деплоится)
├── .env.example           # Пример настроек
├── vercel.json            # Конфигурация Vercel
├── set_webhook.py         # Скрипт для установки webhook
├── requirements.txt       # Python зависимости
└── ... (остальные файлы проекта)
```

## Важные моменты

1. **Безопасность**: Файл `.env` не деплоится на Vercel (он в .gitignore)
2. **Переменные окружения**: В продакшене используются переменные из Vercel Dashboard
3. **Webhook URL**: Должен заканчиваться на `/api/webhook`
4. **Логи**: Используйте `vercel logs` для отладки проблем

## Обновление бота

Для обновления кода:
```bash
git add .
git commit -m "Update bot"
git push
vercel --prod
```

Vercel автоматически деплоит изменения при push в основную ветку (если настроена интеграция с Git).
