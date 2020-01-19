import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHAT_USER_NAME = os.getenv("CHAT_USER_NAME")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
PORT = int(os.environ.get("PORT", 5000))

# checks if message is from the authorized user only
def check_user_name(update):
    username = update.message.from_user.username
    return (username == CHAT_USER_NAME)

# checks if chat id is matching the defined chat id 
def check_chat_id(update):
    chat_id = str(update.message.chat.id)
    return (chat_id == CHAT_ID)

# send a rejection message to unauthorized users
def send_unauthorized_message(update):
    update.message.reply_text('Sorry you are not authorized to use this bot');

# handle /start command. If authorized user, send the chat id
def start(update, context):
    if check_user_name(update):
        update.message.reply_text('Hi {}!, This is your Chat ID: {}'.format(update.message.from_user.first_name, update.message.chat.id))
    else:
        send_unauthorized_message(update);

# handle echo messages
def echo(update, context):
    if check_user_name(update) and check_chat_id(update):
            update.message.reply_text('Haha nice!')
    else:
        send_unauthorized_message(update);

# error handler
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    logger.info('Starting bot')
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, BOT_TOKEN))
    updater.idle()

if __name__ == '__main__':
    main()
