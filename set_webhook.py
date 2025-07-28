import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = input("Enter your Vercel app URL (e.g., https://your-app.vercel.app/api/webhook): ")

def set_webhook():
    """Set webhook for Telegram bot."""
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if not WEBHOOK_URL:
        print("❌ Error: Webhook URL not specified")
        return
    
    # Set webhook
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("ok"):
            print("✅ Webhook successfully set!")
            print(f"📍 URL: {WEBHOOK_URL}")
        else:
            print(f"❌ Error setting webhook: {result.get('description')}")
    else:
        print(f"❌ HTTP error: {response.status_code}")

def get_webhook_info():
    """Get current webhook info."""
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("ok"):
            webhook_info = result.get("result", {})
            print("\n📋 Webhook information:")
            print(f"URL: {webhook_info.get('url', 'Not set')}")
            print(f"Pending updates: {webhook_info.get('pending_update_count', 0)}")
            if webhook_info.get('last_error_date'):
                print(f"Last error: {webhook_info.get('last_error_message')}")
        else:
            print(f"❌ Error: {result.get('description')}")
    else:
        print(f"❌ HTTP error: {response.status_code}")

if __name__ == "__main__":
    print("🤖 Setting up Telegram Bot Webhook for Vercel")
    print("=" * 50)
    
    # Show current webhook info
    get_webhook_info()
    
    # Set new webhook
    print("\n🔧 Setting up new webhook...")
    set_webhook()
    
    # Show updated info
    print("\n📋 Updated information:")
    get_webhook_info()
