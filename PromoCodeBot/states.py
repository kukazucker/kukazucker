from unicodedata import category
from aiogram.dispatcher.filters.state import State, StatesGroup

class Promocodes(StatesGroup):              # state for choosing a promocode
    category = State()
