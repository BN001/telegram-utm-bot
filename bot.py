import re
import logging
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_kaspi_link(link: str) -> str | None:
    if "kaspi.kz" not in link:
        return None

    # Удаляем параметры начиная с /?
    link = re.sub(r"/\?.*$", "", link)

    # Убираем конечный слэш
    if link.endswith("/"):
        link = link[:-1]

    # Добавляем нужный суффикс
    suffix = "/?ksWidget=true&m=12593029&merchantID=12593029&c"
    return link + suffix

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне ссылку на товар Kaspi, я её обработаю.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    processed = process_kaspi_link(text)
    if processed:
        await update.message.reply_text(f"Обработанная ссылка:\n{processed}")
    else:
        await update.message.reply_text("Это не ссылка на kaspi.kz или формат ссылки неправильный.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущен")
    try:
        await app.run_polling()
    except KeyboardInterrupt:
        print("Бот остановлен вручную")

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
