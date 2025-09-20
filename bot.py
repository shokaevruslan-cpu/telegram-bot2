import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from db import log_mood, get_mood_history, save_journal_entry, get_user_settings, set_user_notify

BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Я ваш психолог-бот.\n"
        "Помогу вести дневник настроения и поддерживать вас.\n"
        "Введите /help для меню."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["Мой дневник", "Записать настроение"],
        ["История настроений", "Добавить запись"],
        ["Настройки", "Поддержка"]
    ]
    await update.message.reply_text(
        "Выберите раздел:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    )

async def record_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите ваше настроение (от 1 до 10):")
    context.user_data["awaiting_mood"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if context.user_data.get("awaiting_mood"):
        try:
            mood_value = int(text)
            if 1 <= mood_value <= 10:
                log_mood(mood_value)
                await update.message.reply_text("Ваше настроение сохранено!", reply_markup=ReplyKeyboardRemove())
            else:
                await update.message.reply_text("Введите число от 1 до 10.")
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите число.")
        context.user_data["awaiting_mood"] = False
        return

    if text == "История настроений":
        history = get_mood_history()
        if not history:
            await update.message.reply_text("История пуста.")
        else:
            msg = "История:\n" + "\n".join([f"{row.timestamp}: {row.mood}" for row in history])
            await update.message.reply_text(msg)

    elif text == "Добавить запись":
        await update.message.reply_text("Напишите ваш дневниковый текст:")
        context.user_data["adding_journal"] = True
    elif context.user_data.get("adding_journal"):
        save_journal_entry(text)
        await update.message.reply_text("Запись сохранена!")
        context.user_data["adding_journal"] = False
    elif text == "Настройки":
        notify = get_user_settings(user_id)
        await update.message.reply_text(f"Уведомления {'включены' if notify else 'выключены'}")
    elif text == "Поддержка":
        await update.message.reply_text("Если вам нужна помощь, обратитесь к специалисту или друзьям.")
    else:
        await update.message.reply_text("Используйте меню или команду /help.")

# --- запуск ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
