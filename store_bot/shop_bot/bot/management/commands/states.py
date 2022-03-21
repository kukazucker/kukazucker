from aiogram.dispatcher.filters.state import State, StatesGroup

class getItem(StatesGroup):        # for admin dashboard
    chapter = State()
    aciton = State()
    id = State()

class Item(StatesGroup):           # for loop in items
    count = State()
    chapter = State()

class User(StatesGroup):           # for "Change Profile"
    first_name = State()
    last_name = State()
    birth_day = State()

class setUser(StatesGroup):        # status and balance
    param = State()
    id = State()
    value = State()

class Product(StatesGroup):        # to create a product
    title = State()
    description = State()
    price = State()

class RefLink(StatesGroup):        # to create a link
    title = State()
    description = State()
    link = State()

class Announcement(StatesGroup):   # to create a announcement
    title = State()
    text = State()
