import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from bot_handlers import (
    start_command,
    help_command,
    practice_command,
    handle_message,
    handle_tense_group_selection,
    error_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    # Check if bot token is set
    if not BOT_TOKEN:
        logger.error("Bot token not found! Please check that:")
        logger.error("1. The file '.env' exists in the project root")
        logger.error("2. It contains: TELEGRAM_BOT_TOKEN=your_bot_token_here")
        logger.error("3. Install python-dotenv: pip install python-dotenv")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("practice", practice_command))
    
    # Add callback query handler for inline keyboards
    application.add_handler(CallbackQueryHandler(handle_tense_group_selection))
    
    # Add message handler for text messages (answers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting Spanish Verb Trainer Bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
