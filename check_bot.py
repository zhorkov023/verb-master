#!/usr/bin/env python3
"""
Quick check script to verify bot can start without errors
"""

import sys
from config import BOT_TOKEN

def check_bot_setup():
    """Check if bot is properly configured."""
    print("🔍 Checking bot setup...")
    
    # Check token
    if not BOT_TOKEN:
        print("❌ Bot token not found!")
        print("Please check settings/config.env file")
        return False
    
    print(f"✅ Bot token loaded (starts with: {BOT_TOKEN[:10]}...)")
    
    # Try to import bot handlers
    try:
        from bot_handlers import start_command, help_command, practice_command
        print("✅ Bot handlers imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import bot handlers: {e}")
        return False
    
    # Try to create application (without starting)
    try:
        from telegram.ext import Application
        app = Application.builder().token(BOT_TOKEN).build()
        print("✅ Telegram application created successfully")
    except Exception as e:
        print(f"❌ Failed to create Telegram application: {e}")
        return False
    
    print("🎉 Bot setup is correct! You can run: python3 main.py")
    return True

if __name__ == "__main__":
    success = check_bot_setup()
    sys.exit(0 if success else 1)
