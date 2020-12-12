import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from utils import get_reply , fetch_news,topics_keyboard


#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1348740172:AAGmW608fz1UkOG3a-NYmiBP7dVRGGZPEPc"

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods = ['GET','POST'])
def webhook():
    #webhook view which recieves updated from telegram
    #Creating update object from json-format request data
    update = Update.de_json(request.get_json(),bot)
    #process update
    dp.process_update(update)
    return "ok"


def start(update,context):
    author = update.message.from_user.first_name
    reply = "Hi! {}".format(author)
    context.bot.send_message(chat_id=update.message.chat_id, text=reply)

def _help(bot,update):
    help_txt = "Hey! This is a help text."
    bot.send_message(chat_id=update.message.chat_id, text=help_text)

#def news(bot,update):
 #   bot.send_message(chat_id=update.message.chat_id,text="Choose a category",reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True)
    
def reply_text(update,context):
    intent, reply = get_reply(update.message.text,update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            context.bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=reply)
    

def echo_sticker(update,context):
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' caused error '%s'",update,update.error)


    
    

if __name__ == "__main__":
    bot = Bot(TOKEN)
    #bot.set_webhook("https://b9e67895c519.ngrok.io/"+TOKEN )
    #dp = Dispatcher(bot,None)
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",_help))
    #dp.add_handler(CommandHandler("news",news))
    dp.add_handler(MessageHandler(Filters.text,reply_text))
    dp.add_handler(MessageHandler(Filters.sticker,echo_sticker))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
    #app.run(port=8443)
    
