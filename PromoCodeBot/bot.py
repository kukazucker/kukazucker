from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import states
import markups
import parse

bot = Bot(token='YOUR_TOKEN')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(state="*", commands=['start', 'update'])                # start page
async def welcome(message: types.Message, state: FSMContext):
    await state.finish()                                                    # finish any state
    await message.answer("Hello! You can get promocodes here -> /getpromo!", reply_markup=markups.deleteButtons)        # welcome message

@dp.message_handler(commands=['getpromo'])                                  # get promocodes
async def select_company(message: types.Message):
    await states.Promocodes.category.set()
    await message.answer("Please waiting...")
    markups.get_keyboard(parse.get_categories())                            # get categories from html
    await message.answer("Choose a category, please", reply_markup=markups.selectCompany)   # keyboard with a choice of categories

@dp.message_handler(state=states.Promocodes.category)                        # what category does the user want to see
async def get_promo(message:types.Message, state: FSMContext):
    async with state.proxy() as data:                                        # save selected category
        data['category'] = message.text  
    
    await message.answer("Please waiting...")
    promocodes = parse.get_promocodes(data['category'])                      # get all information about promocodes
    answer = ""
    for promocode in promocodes:
        answer += f"🛒Title: {promocode[0]}\n📝Description: {promocode[1]}\n🏷Code: {promocode[2]}\n⬇️Used: {promocode[3]}\n📌Link: {promocode[4]}\n\n"
    await message.answer(answer, reply_markup=markups.ReplyKeyboardRemove())
    await welcome(message, state)                                            # open start page


if __name__ == '__main__':
    executor.start_polling(dp)