from config.telegram_bot import application 
from handlers.message_handlers import chatgpt_reply, generate_excuse, decompose_jira
import handlers.support_functions as spf 

from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

CHOOSING, GIVE_ME_LINK, FREE_REQUEST, TOPIC, SEND_JIRA, SEND_REQUEST, SEND_EXCUSE = range(7)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", spf.start)],
    states={
        spf.CHOOSING: [
            MessageHandler(filters.Regex("^(Свободная форма)$"), spf.regular_choice_free),
            MessageHandler(filters.Regex("^jira$"), spf.regular_choice_link),
            MessageHandler(filters.Regex("^Отмазки$"), spf.regular_choice_excuse),
        ],
        spf.TOPIC: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                generate_excuse,
            )
        ],
        spf.FREE_REQUEST: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                chatgpt_reply,
            )
        ], 
        spf.GIVE_ME_LINK: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                decompose_jira,
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), spf.done)],
)

application.add_handler(conv_handler)
# Запуск бота
application.run_polling()