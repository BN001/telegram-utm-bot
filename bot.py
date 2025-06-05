import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

# Строго заданное окончание
APPEND_PART = "/?ksWidget=true&m=12593029&merchantID=12593029&c"

def append_custom_part(url: str) -> str:
    # Убираем возможный слеш на конце
    url = url.rstrip("/")
    # Добавляем строго заданный хвост
    return url + APPEND_PART

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.startswith("http"):
        try:
            updated_url = append_custom_part(text)
            await update.message.reply_text(f"Готово:\n{updated_url}")
        except Exception:
            await update.message.reply_text("Произошла ошибка при обработке ссылки.")
    else:
        await update.message.reply_text("Пожалуйста, отправь ссылку.")

async def main():
    app = ApplicationBuilder().token("ТВОЙ_ТОКЕН_ЗДЕСЬ").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
