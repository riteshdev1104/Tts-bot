import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from gtts import gTTS
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_FILE = "logs/messages.log"

# Logging setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Flask app for port binding
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Telegram TTS Bot Running!"

# Telegram bot logic
app = Application.builder().token(BOT_TOKEN).build()

user_settings = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send any text and I’ll convert it to speech.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = user_settings.get(user_id, {}).get("lang", "en")
    speed = user_settings.get(user_id, {}).get("speed", "normal")

    # TTS settings
    tts = gTTS(text=text, lang=lang, slow=(speed == "slow"))
    tts.save("voice.mp3")
    await update.message.reply_voice(voice=open("voice.mp3", "rb"))

    log_entry = f"[{datetime.now()}] User {user_id}: {text} | Lang: {lang}, Speed: {speed}"
    logging.info(log_entry)

async def set_speed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    speed = context.args[0] if context.args else "normal"
    user_settings.setdefault(update.effective_user.id, {})["speed"] = speed
    await update.message.reply_text(f"Voice speed set to: {speed}")

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.args[0] if context.args else "en"
    user_settings.setdefault(update.effective_user.id, {})["lang"] = lang
    await update.message.reply_text(f"Language set to: {lang}")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("speed", set_speed))
app.add_handler(CommandHandler("lang", set_lang))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Run both Flask and Telegram bot
import threading

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def run_telegram():
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
