from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

selectCompany = ReplyKeyboardMarkup()

def get_keyboard(categories):                                   # keyboard with categories
    for category in categories:
        selectCompany.add(f"{category}")

deleteButtons = ReplyKeyboardRemove()                           # delete any keyboard