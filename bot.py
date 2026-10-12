import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message:
        await update.effective_message.reply_text(
            "Telegram ID Lookup Bot\n\n"
            "Send a numeric Telegram user ID, e.g. 7569969750.\n"
            "The bot can show a username/profile only if Telegram makes "
            "that user accessible to this bot. A numeric ID alone does "
            "not guarantee a username or phone number."
        )


async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    value = message.text.strip()
    if not value.isdigit():
        await message.reply_text("Please send a numeric Telegram user ID.")
        return

    user_id = int(value)
    if user_id <= 0 or user_id > 2**63 - 1:
        await message.reply_text("Invalid ID format.")
        return

    try:
        user = await context.bot.get_chat(user_id)
        username = f"@{user.username}" if user.username else "Not available"
        first_name = user.first_name or "Not available"
        last_name = user.last_name or "Not available"

        await message.reply_text(
            "LOOKUP RESULT\n\n"
            f"User ID: {user.id}\n"
            f"First name: {first_name}\n"
            f"Last name: {last_name}\n"
            f"Username: {username}\n"
            "Phone number: Not available through this lookup.\n\n"
            "A missing username means Telegram did not provide one; "
            "it cannot be inferred from the numeric ID."
        )
    except Exception as exc:
        logger.info("Lookup unavailable for %s: %s", user_id, exc)
        await message.reply_text(
            "Could not retrieve this profile. Telegram may not expose "
            "this user to the bot, or the ID may be invalid. A numeric "
            "ID alone does not guarantee a username."
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Unhandled bot error: %s", context.error)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lookup))
    app.add_error_handler(error_handler)
    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
