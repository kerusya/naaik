from telegram.ext import MessageHandler, CommandHandler, filters
from config.telegram_bot import application 
from handlers.message_handlers import chatgpt_reply, generate_excuse, decompose_jira
from handlers.command_handlers import start_reply
from config.openai_client import client 

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


CHOOSING, GIVE_ME_LINK, FREE_REQUEST, TOPIC, SEND_JIRA, SEND_REQUEST, SEND_EXCUSE, END = range(8)

reply_keyboard = [
    ["Свободная форма", "jira", "Отмазки"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начvало разговора, просьба ввести данные."""
    await update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=markup,
    )
    return CHOOSING

async def regular_choice_free(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрос информации о выбранном предопределенном выборе."""
    text = update.message.text
    await update.message.reply_text(f"Введите запрос в произвольной форме")
    return FREE_REQUEST

async def regular_choice_excuse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрос информации о выбранном предопределенном выборе."""
    text = update.message.text
    await update.message.reply_text(f"Введите тему для отмазки")
    return TOPIC

async def regular_choice_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрос информации о выбранном предопределенном выборе."""
    text = update.message.text
    await update.message.reply_text(f"Пришлите название таски в jira")
    return GIVE_ME_LINK

async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f"Введите тему для отмазки")
    return TYPING_REASON

async def end_of_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    bot.send_message(chat_id , text = "THSADAN")
    #await update.message.reply_text(f"Выбери новую задачу или заверши общение клавишей Done")
    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Вывод собранной информации и завершение разговора."""
    await update.message.reply_text(
        f"Спасибо за общение, надеюсь тебя не уволили!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [
            MessageHandler(filters.Regex("^(Свободная форма)$"), regular_choice_free),
            MessageHandler(filters.Regex("^jira$"), regular_choice_link),
            MessageHandler(filters.Regex("^Отмазки$"), regular_choice_excuse),
        ],
        TOPIC: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                generate_excuse,
            )
        ],
        FREE_REQUEST: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                chatgpt_reply,
            )
        ], 
        GIVE_ME_LINK: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                decompose_jira,
            )
        ],
        END: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                end_of_query,
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
)

application.add_handler(conv_handler)
# Запуск бота
application.run_polling()