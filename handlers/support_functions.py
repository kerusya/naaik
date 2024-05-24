from telegram.ext import ContextTypes, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

CHOOSING, GIVE_ME_LINK, FREE_REQUEST, TOPIC, SEND_JIRA, SEND_REQUEST, SEND_EXCUSE = range(7)

reply_keyboard = [
    ["Свободная форма", "jira", "Отмазки"],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет это бот помощник.\n"
        "Я могу дать ответ в свободной форме, декомпозировать задачу в jira, придумать отмазку",
        reply_markup=markup,
    )
    return CHOOSING

async def regular_choice_free(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(f"Введите запрос в произвольной форме")
    return FREE_REQUEST

async def regular_choice_excuse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(f"Введите тему для отмазки")
    return TOPIC

async def regular_choice_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    await update.message.reply_text(f"Пришлите название таски в jira")
    return GIVE_ME_LINK

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Спасибо за общение, надеюсь, тебя не уволили!\nЕсли захочешь ещё пообщаться, просто нажми /start",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END