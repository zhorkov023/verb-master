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

# Global application instance
application = None

def get_or_create_application():
    """Get or create Application instance (synchronous)."""
    global application
    
    if application is None:
        # Create the Application instance
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("practice", practice_command))
        application.add_handler(CallbackQueryHandler(handle_tense_group_selection))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        logger.info("Application created")
    
    return application

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
            
            # Process the update with proper event loop management
            self.process_update_sync(body)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "ok"})
            self.wfile.write(response.encode('utf-8'))
                
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({"error": str(e)})
            self.wfile.write(response.encode('utf-8'))

    def process_update_sync(self, body):
        """Process Telegram update with proper event loop management."""
        try:
            # Get application
            app = get_or_create_application()
            
            # Create Update object from the webhook data
            update = Update.de_json(body, app.bot)
            
            # Create new event loop for this request
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Initialize application if needed
                if not app.running:
                    loop.run_until_complete(app.initialize())
                
                # Process the update
                loop.run_until_complete(app.process_update(update))
                
            finally:
                # Clean up the loop
                try:
                    # Cancel all pending tasks
                    pending = asyncio.all_tasks(loop)
                    for task in pending:
                        task.cancel()
                    
                    # Wait for tasks to complete cancellation
                    if pending:
                        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    
                    # Close the loop
                    loop.close()
                except Exception as cleanup_error:
                    logger.warning(f"Error during loop cleanup: {cleanup_error}")
            
        except Exception as e:
            logger.error(f"Error in process_update_sync: {e}")
            raise
