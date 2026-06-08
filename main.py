import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes
from bot.handlers.ai_chat import ai_chat_handler  
from bot.handlers.welcome import welcome_flow    
# This imports your original custom layout with the Spiderman image and buttons
from bot.handlers.start import start_handler     

# Setup logging to view issues directly in Render logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("CRITICAL: TELEGRAM_TOKEN environment variable is missing on the server backend!")
    
    # Initialize the background bot framework application
    app = ApplicationBuilder().token(token).build()
    
    # Register your actual custom start layout handler loop
    app.add_handler(CommandHandler("start", start_handler))
    
    app.add_handler(ChatMemberHandler(welcome_flow, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat_handler))
    
    print("🚀 Bot process sequence starting loop... listening to Telegram endpoints cleanly!")
    app.run_polling()

if __name__ == '__main__':
    main()
