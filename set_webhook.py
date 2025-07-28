import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = input("Введите URL вашего Vercel приложения (например: https://your-app.vercel.app/api/webhook): ")

def set_webhook():
    """Set webhook for Telegram bot."""
    if not BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env файле")
        return
    
    if not WEBHOOK_URL:
        print("❌ Ошибка: URL webhook не указан")
        return
    
    # Set webhook
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("ok"):
            print("✅ Webhook успешно установлен!")
            print(f"📍 URL: {WEBHOOK_URL}")
        else:
            print(f"❌ Ошибка при установке webhook: {result.get('description')}")
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")

def get_webhook_info():
    """Get current webhook info."""
    if not BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("\n📋 Информация о webhook:")
            print(f"URL: {webhook_info.get('url', 'Не установлен')}")
            print(f"Pending updates: {webhook_info.get('pending_update_count', 0)}")
            if webhook_info.get('last_error_date'):
                print(f"Последняя ошибка: {webhook_info.get('last_error_message')}")
        else:
            print(f"❌ Ошибка: {result.get('description')}")
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")

if __name__ == "__main__":
    print("🤖 Настройка Telegram Bot Webhook для Vercel")
    print("=" * 50)
    
    # Show current webhook info
    get_webhook_info()
    
    # Set new webhook
    print("\n🔧 Установка нового webhook...")
    set_webhook()
    
    # Show updated info
    print("\n📋 Обновленная информация:")
    get_webhook_info()
