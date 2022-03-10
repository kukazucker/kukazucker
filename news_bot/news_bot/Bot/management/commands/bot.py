import requests

from shutil import SameFileError

from django.core.management.base import BaseCommand
from news_bot.settings import BOT_TOKEN

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from Bot.models import Profile
from Bot.models import News

def log_errors(f):                                              # output to the console about the main errors
    def inner( *args, **kwargs ):
        try:
            return f( *args, **kwargs )
        except Exception as err:
            error_message = f'Error: {err}'
            print(error_message)
            raise err

    return inner


@log_errors
def answer( update: Update, context: CallbackContext ):         # get news from the user

    first_name = update.message.from_user.first_name            # collect data from a message
    news_content = update.message.caption                       # news text
    group_name = update.message.forward_from_chat.username      
    file_from_news = None                                       # file from a message
    file_news_id = update.message                               # id of the file

    if( update.message.video == None and update.message.document == None and update.message.photo == []):   # determine the file format to get unique_id
        file_news_id = None                                                                                 # there is no file

    elif( update.message.video == None and update.message.document == None ):                               # photo
        file_news_id = update.message.photo[-1].file_id   

    elif( update.message.photo == [] and update.message.document == None ):                                 # video
        file_news_id = update.message.video.file_id

    else:
        file_news_id = update.message.document.file_id                                                      # document


    if ( update.message.caption == None ):                                                                  # if there is no text in caption ( telebot.Message ) then find in text
        news_content = update.message.text
        

    try:
        if ( file_news_id != None ):                                                                        # if there is a file
            file_from_news = context.bot.get_file(file_news_id)                                             # get the path_file for telegram_api
            r = requests.get( f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_news_id}" )   # this request is for kind and file name
            data = r.json()                                                                                 # get in json format

            file_extension = data['result']['file_path']                                                    # get path for a file on the server
            file_extension = 'files/' + file_extension                                                      # folder files/ + path

            file_from_news.download(file_extension)                                                         # download file from telegram api
            file_from_news = file_extension                                                                 # the path for the django table
    
    except SameFileError as err:                                                                            # error if the file already exists
        update.message.reply_text( text = 'Error: I already have this file' )
        raise err

    except Exception as err:                                                                                # error if the file is too big
        update.message.reply_text( text = 'Error: This file is too big' )
        raise err

    p, _ = Profile.objects.update_or_create(                                                                # create a new user in DB
        user_id = update.message.from_user.id,
        defaults = {
            'first_name': first_name,
            'last_name': update.message.from_user.last_name,
            'username': update.message.from_user.username
        }
    )

    m = News.objects.create(                                                                                # create a new news in DB
        profile = p,
        channel = f'http://t.me/{group_name}',
        news_text = news_content,
        news_file = file_from_news,
        created_at = update.message.forward_date
    )

    reply_text = "Thank you for this news, {}! 😉 \n Let's send me something else!".format(update.message.from_user.first_name) # successful file upload
    update.message.reply_text( text = reply_text )

@log_errors
def first_answer( update: Update, context: CallbackContext ):                                               # welcome words
    update.message.reply_text( text = "Hello! Let's send me some news! 📩" )



class Command( BaseCommand ):
    help = 'Telegram-bot'

    def handle(self, *args, **options):                                                                     # configurations and handlers                                                    
        request_conf = Request(                                                                             
            connect_timeout=0.5,
            read_timeout=1.0
        )
        main_bot = Bot(
            request = request_conf,
            token=BOT_TOKEN
        )

        updater = Updater(
            bot = main_bot,
            use_context=True
        )

        welcome = CommandHandler('start', "first_answer")
        updater.dispatcher.add_handler(welcome)

        news_handler = MessageHandler(Filters.all, answer)
        updater.dispatcher.add_handler(news_handler)

        updater.start_polling()
        updater.idle()
