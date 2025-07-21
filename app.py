import os
# If you use v2rayN proxy routing, use below couple of lines to receive updates and send response through your proxy
os.environ["HTTP_PROXY"] = "socks5://127.0.0.1:10808"
os.environ["HTTPS_PROXY"] = "socks5://127.0.0.1:10808"

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import json
import io

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace with your bot token
BOT_TOKEN = "YOUR-BOT-TOKEN"

# Sample command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me a message or forward a post, and I\'ll return its JSON structure.')

# Message handler that returns JSON representation of the message as a file
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        message_dict = update.message.to_dict()
        json_str = json.dumps(message_dict, indent=2, ensure_ascii=False)

        # Create an in-memory file object
        json_bytes = io.BytesIO(json_str.encode('utf-8'))
        json_bytes.name = "message.json"
        json_bytes.seek(0)

        await update.message.reply_document(document=InputFile(json_bytes))

# Initialize the bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

# Start the bot
app.run_polling()
