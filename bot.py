"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from threading import Timer

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

id_bot = '' #preencher com id do bot
timers = {}
mural_ddg = "" #grupo a ser encaminhado
mural_teste = ""
url = "" #url heroku

PORT = int(os.environ.get('PORT', '8443'))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Oi! eu sou o dragão fofoqueiro da Garagem, você pode me contar qualquer coisa que eu vou encaminhar pro resto da garagem rapidinho!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""É simples demais: é só mandar uma mensagem!
Sua mensagem vai ser encaminhada pro Mural da Garagem e vamos responder nos nossos recadinhos. 

(Ou podemos manter só entre nós, se preferir. Só nos avisar)""")


def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.chat_id)
    
def forward_msg(update, context):
    if str(update.message.chat_id) not in [mural_ddg, mural_teste]: #se não for no mural, encaminha pro mural
        
        context.bot.forward_message(chat_id=mural_ddg,
                        from_chat_id=update.message.chat_id,
                        message_id=update.message.message_id)
   
        t = Timer(42, mensagem, args=[update,context])
        t.start()  
    
        if update.message.chat_id in timers:
            timers[update.message.chat_id].cancel()    
    
        timers[update.message.chat_id]=t
    else: #se for no mural, e for reply pro bot, encaminha pra pessoa
        if update.message.reply_to_message and update.message.reply_to_message.from_user.username == 'dragoes_bot':
            
            context.bot.forward_message(chat_id=update.message.reply_to_message.forward_from.id,
                        from_chat_id=mural_ddg,
                        message_id=update.message.message_id)
       
        
    

def mensagem(update,context):
    update.message.reply_text('Obrigado! Acabei de encaminhar :)')
    if update.message.chat_id in timers:
        timers.pop(update.message.chat_id)
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(url, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.all,forward_msg))



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()
   
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=url)
   
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook('https://dragoesbot.herokuapp.com/' + url)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
