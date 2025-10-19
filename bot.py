import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from agent import run_adk_async

# Konfiguracja logowania
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Obsługuje komendę /start."""
    await update.message.reply_text("Cześć! Jestem Twoim agentem. Wyślij mi polecenie, a ja je wykonam.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Przetwarza wiadomości tekstowe od użytkownika."""
    user_input = update.message.text
    user_id = str(update.effective_user.id)
    logger.info(f"Otrzymano wiadomość od {user_id}: {user_input}")

    response = await run_adk_async(session_id=user_id, instruction=user_input)
    await update.message.reply_text(response)

async def handle_photo(update: Update, context: CallbackContext) -> None:
    """Przetwarza przesłane zdjęcia."""
    user_id = str(update.effective_user.id)
    photo_file = await update.message.photo[-1].get_file()
    
    # Utworzenie katalogu uploads, jeśli nie istnieje
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file_path = os.path.join("uploads", f"{user_id}_{photo_file.file_unique_id}.jpg")
    await photo_file.download_to_drive(file_path)

    logger.info(f"Zdjęcie od {user_id} zostało zapisane w {file_path}")

    # Przekazanie informacji do agenta
    instruction = f"Otrzymałem zdjęcie. Ścieżka do pliku: {os.path.abspath(file_path)}"
    response = await run_adk_async(session_id=user_id, instruction=instruction)
    await update.message.reply_text(response)

def main() -> None:
    """Główna funkcja uruchamiająca bota."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.critical("Brak tokena bota Telegrama. Ustaw zmienną środowiskową TELEGRAM_BOT_TOKEN.")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("Bot Telegrama został uruchomiony i nasłuchuje na wiadomości...")
    application.run_polling()

if __name__ == "__main__":
    main()