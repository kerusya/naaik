import json

from telegram import Update,KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # объект обновления
    update_obj = json.dumps(update.to_dict(), indent=4)

    # ответ
    #reply = "*update object*\n\n" + "```json\n" + update_obj + "\n```"
    reply = "Привет! Это бот для помощи. Он умеет \n Генерировать отмазки /generate\_excuse"

    # перенаправление ответа в Telegram
    await update.message.reply_text(reply, parse_mode="Markdown")

    print("assistant:", reply)