from django.core.management.base import BaseCommand
from shop_bot.settings import BOT_TOKEN

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor, exceptions

import bot.management.commands.markups as nav
import bot.management.commands.crud as crud
import bot.management.commands.item as item
import bot.management.commands.states as states

bot = Bot( token=BOT_TOKEN )
main_storage = MemoryStorage()
dispatcher = Dispatcher( bot, storage=main_storage )

##################################################### MENU #####################################################


@dispatcher.message_handler(state="*", commands=['start'])                          
@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def start(message: types.Message, state: FSMContext):

    menu = ("Hey! I'm a bot and I'll help you buy something here\n"
            "Here you can buy our products and read the\n"
            "latest news! You can also get special referral links here\n"
            "with their help you can buy our products cheaper! Of course\n"
            "you can see here your balance and top up your wallet! \n"
            "⬇️Below you can see our commands. Enjoy your use!⬇️\n"
            "/menu - you can cancel your action or just see this menu\n"
            "/products - here you can find our products\n"
            "/announcements - here you can find our announcements\n"
            "/refs - here you can find your new and not very referral links\n"
            "/profile - here you can find your personal information\n"
           )
    await bot.send_message(message.from_user.id, menu, reply_markup=nav.deleteButtons)

##################################################### SERVICE #####################################################


@dispatcher.message_handler(state="*", commands='menu')
async def welcome(message: types.Message, state: FSMContext):
    menu = ("/menu - you can cancel your action or just see this menu\n"
            "/products - here you can find our products\n"
            "/announcements - here you can find our announcements\n"
            "/refs - here you can find your new and not very referral links\n"
            "/profile - here you can find your personal information\n"
           )
    await bot.send_message(message.from_user.id, menu, reply_markup=nav.deleteButtons)

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


##################################################### REF LINKS, ANNOUNCEMENTS, PRODUCTS #####################################################


@dispatcher.message_handler(state="*", commands=['refs', 'announcements', 'products'])            # this function get list of links, products, announcements
async def refAmount(message: types.Message, state: FSMContext):                                   # and show user part or the whole sheet
    await states.Item.count.set()   
    async with state.proxy() as data:
        data['count'] = 0
        data['chapter'] = message.text[1:]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("new", "all")

    await message.answer(f"How many {data['chapter']} want you see?", reply_markup=markup)

@dispatcher.message_handler(state=states.Item.count)                                             # this is loop: or user wants see all or
async def get_ref(message: types.Message, state: FSMContext, amount_items=1):                    # just new products
    try:
        async with state.proxy() as data:
            if(amount_items == -1):
                await welcome(message, state)
                
            elif(message.text == 'all'):
                answer = item.get_list(data['chapter'], data['count'], -1)
                await message.answer(answer) and await welcome(message, state)
            
            else:                                                                               # he can also click on the button to see
                answer = item.get_list(data["chapter"], data["count"], amount_items)            # more products and so on
                await bot.send_message(message.from_user.id, answer, reply_markup=nav.keyboard) 
                data['count'] += amount_items

    except exceptions.MessageTextIsEmpty:                                                       # if they are over, an error pops up
        await bot.send_message(message.from_user.id, "Sorry, i have't more links!")
        await welcome(message, state)                                                           # call start menu
    
        
@dispatcher.callback_query_handler(state=states.Item.all_states)
async def gg(message: types.Message, state: FSMContext):
    num = int(message.data)
    message.text = 'more'
    await get_ref(message, state, num)

#################################################### PROFILE #####################################################


@dispatcher.message_handler(state="*", commands=['profile'])                                    # here user can see his balance
async def get_profile(message: types.Message, state: FSMContext):   
    user_info = item.get_item('users', '/2')
    await message.answer(user_info, reply_markup=nav.set_user)

@dispatcher.message_handler(text='Change Profile')                                              # also he can change his personal data
async def user_set(message: types.Message):                                                     
    await states.User.first_name.set()
    await message.answer("Your first name:")

@dispatcher.message_handler(state=states.User.first_name)
async def user_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await states.User.next()
    await message.answer("Your last name:")

@dispatcher.message_handler(state=states.User.last_name)
async def user_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await states.User.next()
    await message.answer("Your Birth Day(YYYY-MM-DD):")

@dispatcher.message_handler(state=states.User.birth_day)
async def user_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birth_day'] = message.text
        user_data = {
            "first_name": f"{data['first_name']}",
            "last_name": f"{data['last_name']}",
            "birth_day": f"{data['birth_day']}"
        }
    id = 2

    answer = crud.updateItem('users', f'{id}', user_data)                                      # update user personal data 
    await message.answer(answer)    
    await welcome(message, state)                                                              # call menu

##################################################### ADMIN #####################################################


@dispatcher.message_handler(state="*", commands='5431420a9fd08dfu90')                          # admin dashboard
async def admin_dashboard(message: types.Message):
    await states.getItem.chapter.set()
    await message.answer(f"Hello {message.from_user.first_name}! What do you want to see?", reply_markup=nav.dashboard)

@dispatcher.message_handler(state=states.getItem.chapter)                                       # select the section he wants to work with
async def getAllUserPayments(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chapter'] = message.text.lower()
    if(message.text == 'Quit'):
        await welcome(message, state)
    elif(data['chapter'] == 'users'):
        await user_set(message)
    elif(data['chapter'] == 'products'):
        await prod_set(message)
    elif(data['chapter'] == 'refs'):
        await refs_set(message)
    elif(data['chapter'] == 'announcements'):
        await announce_set(message)
        
##################################################### FORMS #####################################################

 
########################### Announcement Form ###########################
async def announce_set(message: types.Message):
    await states.Announcement.title.set()
    await message.reply("Write the title of the announcement", reply_markup=types.ReplyKeyboardRemove())

@dispatcher.message_handler(state=states.Announcement.title)
async def set_recipient(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await states.Announcement.next()
    await message.reply("Please, write announcement text here. Maximal length = 2000 characters")

@dispatcher.message_handler(state=states.Announcement.text)
async def set_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    announ_data = {
        "title": data['title'],
        "text": data['text']
    }

    crud.createItem('anouncements', 'yes', announ_data)
    all_chat_id = item.get_chatID()                                                                     # get all chat_id's
    for chat_id in all_chat_id:                                                                         # this loop sends announcements to all users
        await bot.send_message(f'{chat_id}', "Title: {data['title']}\n Text: {data['text']}")
        
    await message.answer(f"You have created new announcement:\nTitle: {data['title']}\n Text: {data['text']}")

    await state.finish()
    await welcome(message, state)


########################### RefLinks Form ###########################

async def refs_set(message: types.Message):                                                              # create a referal link
    await states.RefLink.title.set()
    await message.answer("Whats title of the ref link?")                                                 

@dispatcher.message_handler(state=states.RefLink.title)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await states.RefLink.next()
    await message.answer("Please, write announcement text here. Maximal length = 2000 characters")

@dispatcher.message_handler(state=states.RefLink.description)
async def set_descr(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await states.RefLink.next()
    await message.answer("Please, send me url link")


@dispatcher.message_handler(state=states.RefLink.link)
async def set_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text

    data = {
        "name": data["title"],
        "description": data["description"],
        "link": data["link"]
    }

    reflink = crud.createItem('refs', 'yes', data)

    await message.answer(reflink)
    await welcome(message, state)

########################### Product Form ###########################

async def prod_set(message: types.Message):
    await states.Product.title.set()
    await message.answer("Product name:")

@dispatcher.message_handler(state=states.Product.title)
async def set_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text.lower()

    await states.Product.next()
    await message.answer("Description:")

@dispatcher.message_handler(state=states.Product.description)
async def set_descr(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text.lower()

    await states.Product.next()
    await message.answer("Price:")

@dispatcher.message_handler(state=states.Product.price)
async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text.lower()

    upd_data = {
        f"name": f"{data['title']}",
        f"description": f"{data['description']}",
        f"price": f"{data['price']}"
    }
    answer = crud.createItem('products', 'yes', upd_data)

    await message.answer(answer)
    await welcome(message, state)

##################################################### UPDATE STATUS AND BALANCE #####################################################


async def user_set(message: types.Message):
    await states.setUser.param.set()
    await message.answer('What do you want to change', reply_markup=nav.user)

@dispatcher.message_handler(state=states.setUser.param)
async def get_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['param'] = message.text.lower()
        if(data['param'] == 'balance'):
            list = item.get_list(f"users", 0, -1)                                           # -1 means 'all users'
            data['chapter'] = 'users'                                                       # chapter for selecting the table where the 
        else:                                                                               # information will be updated
            list = item.get_list(f"payments", 0, -1)
            data['chapter'] = 'payments'

    await states.setUser.next()
    await message.answer(list)                                                              # display all payments or users
    await message.answer('Write id of item', reply_markup=nav.deleteButtons)

@dispatcher.message_handler(state=states.setUser.id)                                        
async def set_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text.lower()
    await states.setUser.value.set()
    if(data["param"] == 'balance'):
        await message.answer('Enter new balance:', reply_markup=nav.deleteButtons)
    else:
        await message.answer('Enter new status:', reply_markup=nav.deleteButtons)

@dispatcher.message_handler(state=states.setUser.value)
async def set_value(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
    
    update_data = {                                                                         # dynamic data: or balance: value, or status: value  
        f"{data['param']}": f"{data['value']}"
    }

    answer = crud.updateItem(f"{data['chapter']}", data['id'], update_data)
    await message.answer(answer)
    await welcome(message, state)

##################################################### SETUP #####################################################


@dispatcher.message_handler()
async def start(message: types.Message, state: FSMContext):
    await welcome(message, state)

class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):

        executor.start_polling(dispatcher)