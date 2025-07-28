import json
import logging
import os
from telegram import Update
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

# Create the Application instance
application = Application.builder().token(BOT_TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("practice", practice_command))
application.add_handler(CallbackQueryHandler(handle_tense_group_selection))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.add_error_handler(error_handler)

def handler(request):
    """Handle incoming webhook requests from Telegram."""
    import asyncio
    
    async def process_update():
        try:
            # Parse request body
            if hasattr(request, 'get_json'):
                # Flask-like request
                body = request.get_json()
            elif hasattr(request, 'json'):
                # Other request types
                body = await request.json() if asyncio.iscoroutinefunction(request.json) else request.json()
            else:
                # Raw body from Vercel
                body_str = request.get('body', '{}')
                if isinstance(body_str, str):
                    body = json.loads(body_str)
                else:
                    body = body_str
            
            # Create Update object from the webhook data
            update = Update.de_json(body, application.bot)
            
            # Process the update
            await application.process_update(update)
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"status": "ok"})
            }
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": str(e)})
            }
    
    # Handle GET requests for testing
    if request.get('httpMethod') == 'GET' or request.get('method') == 'GET':
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"status": "Telegram Bot Webhook is running"})
        }
    
    # Run the async handler for POST requests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(process_update())
        return result
    finally:
        loop.close()
