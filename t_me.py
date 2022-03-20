from contextlib import ContextDecorator
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ParseMode
import html
import json
import logging
import traceback


#log para debugar depois
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s, level=logging.INFO')
updater = Updater(token='5232423052:AAE9WdIoZNubH3XjA-6M35u_OD5uOxXWXwM', use_context=True)
dispatcher = updater.dispatcher
logger = logging.getLogger(__name__)

DEVELOPER_CHAT_ID = 1030433131

#receptores "comandos aceitos"

def error_handler(update: object, context: CallbackContext) -> None:
    """Registra o erro e envia uma mensagem ao desenvolvedor."""
    # Registra o erro antes de tudo para debugar melhor.
    logger.error(msg="Ocorreu um erro e eu não soube como me comportar:", exc_info=context.error)

    # traceback.format_exception retorna a mensagem de erro padrão do python , mas como uma lista de string
    # maior do que o normal por isso organizamos em uma lista tb_list.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Constrói uma mensagem de erro mais bonita.

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'Ocorreu um erro e eu não soube como me comportar:\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )
   # Envia a mensagem de erro para o desenvolvedor.
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def erro(update: Update, context: CallbackContext) -> None:
    context.bot.wrong_method_name()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Eai Nerd! digite /comandos para ver o que eu posso fazer.")

def horarios(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Os horários estão aqui: <a href='https://wsecurity.tech/wp-content/uploads/2022/03/horarios.png'> Horários SI </a>", parse_mode=ParseMode.HTML)

def comandos(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Os comandos são:\n<pre> /start\n /site\n /horarios\n /sugestao\n /python\n</pre>", parse_mode=ParseMode.HTML)

def site(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Site do curso: <a href='https://www.si.plc.ifmt.edu.br'>SI-IFMT</a>", parse_mode=ParseMode.HTML)

def sugestao(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Envie sua sugestão para o nerd master @wilsntn ele ficará muito feliz em implementar!")

def python(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Python é a melhor linguagem de programação! Sabe por que? Porque eu fui feito em Python e eu sou o melhor!")

#função para que toda vez que for enviado um comando apos a / o bot captura
dispatcher.add_error_handler(error_handler)

erro_handler = CommandHandler('erro', erro)
dispatcher.add_handler(erro_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

comandos_handler = CommandHandler('comandos', comandos)
dispatcher.add_handler(comandos_handler)

python_handler = CommandHandler('python', python)
dispatcher.add_handler(python_handler)

sugestao_handler = CommandHandler('sugestao', sugestao)
dispatcher.add_handler(sugestao_handler)

horarios_handler = CommandHandler('horarios', horarios)
dispatcher.add_handler(horarios_handler)

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