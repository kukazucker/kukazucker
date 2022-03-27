from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

keyboard = InlineKeyboardMarkup()                                                # keyboard for extra amount of ref links, products and announcements
more10 = InlineKeyboardButton(text='10 more', callback_data='10', selective=True)
more20 = InlineKeyboardButton(text='20 more', callback_data='20', selective=True)
more30 = InlineKeyboardButton(text='30 more', callback_data='30', selective=True)
menu = InlineKeyboardButton(text='menu', callback_data='-1', selective=True)
keyboard.add(more10, more20, more30, menu)

set_user = ReplyKeyboardMarkup()                                                 # keyboard for personal account
orders = InlineKeyboardButton(text='Orders', callback_data='1', selective=True)
change = InlineKeyboardButton(text='Change Profile', callback_data='2', selective=True)
set_user.add(change, orders)

deleteButtons = ReplyKeyboardRemove()                                           # remove any keyboard

markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)              # exit 
markup.add("menu")

yesno = InlineKeyboardMarkup()                                                  # selecting yes or no (changing profile)
yes = InlineKeyboardButton(text='yes', callback_data='yes', selective=True)
no = InlineKeyboardButton(text='no', callback_data='no', selective=True)
yesno.add(yes, no)

crud = ReplyKeyboardMarkup()                                                    # keyboar for admin selecting
create = InlineKeyboardButton(text='Create', callback_data='1', selective=True)
delete = InlineKeyboardButton(text='Delete', callback_data='4', selective=True)
crud.add(create, delete)

dashboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)   # keyboard for admin dashboard
users = InlineKeyboardButton(text='Users', callback_data='1', selective=True)
refs = InlineKeyboardButton(text='Refs', callback_data='2', selective=True)
announs = InlineKeyboardButton(text='Announcements', callback_data='3', selective=True)
payments = InlineKeyboardButton(text='Products', callback_data='4', selective=True)
quit = InlineKeyboardButton(text='Quit', callback_data='5', selective=True)
dashboard.add(users, refs)
dashboard.add(announs, payments)
dashboard.add(quit)

user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)         # admin's choice: what to change 
balance = InlineKeyboardButton(text='Balance', callback_data='1', selective=True)
status = InlineKeyboardButton(text='Status', callback_data='2', selective=True)
user.add(balance, status)
