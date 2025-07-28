from http.server import BaseHTTPRequestHandler
import json
import logging
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import bot handlers
import sys
sys.path.append('..')
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for testing."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = json.dumps({"status": "Telegram Bot Webhook is running"})
        self.wfile.write(response.encode('utf-8'))
        return

    def do_POST(self):
        """Handle POST requests from Telegram webhook."""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the request body
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            body = json.loads(post_data.decode('utf-8'))
            
            # Process the update asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                loop.run_until_complete(self.process_update(body))
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"status": "ok"})
                self.wfile.write(response.encode('utf-8'))
                
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"error": str(e)})
            self.wfile.write(response.encode('utf-8'))

    async def process_update(self, body):
        """Process Telegram update."""
        try:
            # Create Update object from the webhook data
            update = Update.de_json(body, application.bot)
            
            # Process the update
            await application.process_update(update)
            
        except Exception as e:
            logger.error(f"Error in process_update: {e}")
            raise
