from contextlib import ContextDecorator
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent


#log para debugar depois
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s, level=logging.INFO')
updater = Updater(token='5232423052:AAE9WdIoZNubH3XjA-6M35u_OD5uOxXWXwM', use_context=True)
dispatcher = updater.dispatcher

#receptores "comandos aceitos"
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi tudo bem?")

def site(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Acesse: https://www.wsecurity.tech!")

#função para que toda vez que for enviado um /start o bot captura
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

site_handler = CommandHandler('site', site)
dispatcher.add_handler(site_handler)

#função para que o bot entenda todas as mensagens que não são comandos..
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat_id, text=update.message.text)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

#para o bot diferenciar maiusculas
from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

#para o bot responder comandos não reconhecidos
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Eu não conheço esse comando! Fale com o meu dono! @wilsntn")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()