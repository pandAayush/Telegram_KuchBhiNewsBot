import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard
#ENABLES LOGGING
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
					level = logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "your_app_token" #the actual token from heroku goes here

app = Flask(__name__)
@app.route('/')

def index():
	return 'Hello!'

#USING FLASK
@app.route(f'/{TOKEN}', methods = ['GET', 'POST'])

def webhook():
	update = Update.de_json(request.get_json(), bot) #Creates an update object
	#Process the update recieved
	dp.process_update(update)
	return 'ok'


def start(bot, update):
	print(update)
	author = update.message.from_user.first_name
	#msg = update.messagetext
	reply = "Hi! {}".format(author)
	bot.send_message(chat_id = update.message.chat_id, text = reply)

def _help(bot, update):
	help_text = "I'm trying to help. I'm not very good."
	bot.send_message(chat_id = update.message.chat_id, text = help_text)

def news(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = 'Choose a Category...',
		reply_markup = ReplyKeyboardMarkup(keyboard = topics_keyboard, one_time_keyboard = True))

def reply_text(bot, update): #formerly echo_text
	#eply = update.message.text #used to echo
	#bot.send_message(chat_id = update.message.chat_id, text = reply)
	
	intent, reply = get_reply(update.message.text, update.message.chat_id)

	if intent == 'get_news':
		try:	
			reply_text = "Ok. News coming up..."
			
			articles = fetch_news(reply)
			bot.send_message(chat_id = update.message.chat_id, text = reply_text)
			
			for article in articles:
				bot.send_message(chat_id = update.message.chat_id, text = article['link'])
			
		except:
			bot.send_message(chat_id = update.message.chat_id, text = 'couldnt get news. I have failed you master Wayne')

	else:
		try:
			bot.send_message(chat_id = update.message.chat_id, text = reply)
		except:
			bot.send_message(chat_id = update.message.chat_id, text = 'Im not very good at small talk')

def echo_sticker(bot, update):
	bot.send_sticker(chat_id = update.message.chat_id, 
		sticker = update.message.sticker.file_id)

def error(bot, update):
	logger.error("Update '%s' caused an error '%s'", update, update.error)

if __name__ == "__main__":
	#main()

	#updater = Updater(TOKEN) #Use for polling
	bot = Bot(TOKEN)
	bot.set_webhook("https://a75c4b676927.ngrok.io/" + TOKEN) #
	
	dp = Dispatcher(bot, None) #Second para. used to handle multiple queries using a queue
	dp.add_handler(CommandHandler("start", start)) #handles /start command
	dp.add_handler(CommandHandler("help", _help)) #Handles /help command
	dp.add_handler(CommandHandler("news", news))
	dp.add_handler(MessageHandler(Filters.text, reply_text)) #Handles Text Messages
	dp.add_handler(MessageHandler(Filters.sticker, echo_sticker)) #Handles Sticker messages
	dp.add_error_handler(error) #Handles errors

	app.run(port = 8443)
	#updater.start_polling()
	#logger.info("Started polling...")
	#updater.idle()
