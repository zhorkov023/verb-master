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

async def handler(request):
    """Handle incoming webhook requests from Telegram."""
    try:
        # Get the request body
        if request.method == "POST":
            body = await request.json()
            
            # Create Update object from the webhook data
            update = Update.de_json(body, application.bot)
            
            # Process the update
            await application.process_update(update)
            
            return {
                "statusCode": 200,
                "body": json.dumps({"status": "ok"})
            }
        else:
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Method not allowed"})
            }
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# For Vercel
def lambda_handler(event, context):
    """AWS Lambda handler for Vercel."""
    import asyncio
    
    class Request:
        def __init__(self, event):
            self.method = event.get('httpMethod', 'GET')
            self.body = event.get('body', '{}')
            
        async def json(self):
            return json.loads(self.body)
    
    request = Request(event)
    
    # Run the async handler
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(handler(request))
        return {
            'statusCode': result['statusCode'],
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': result['body']
        }
    finally:
        loop.close()
