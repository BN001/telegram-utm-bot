import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ВСТАВЬ СВОЙ ТОКЕН
BOT_TOKEN = "7952847290:AAHJMwn5Bpj3I2bd9xuI61PfOdL9kH18H_s"

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
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
