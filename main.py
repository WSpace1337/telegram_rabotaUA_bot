#import
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import time
import config
import parserPy
import datetime

#main
logging.basicConfig(level=logging.INFO) #configure logging
bot = Bot(token = config.API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
#command

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет,я парсер сайта rabota.ua!\n Для того чтобы начать поиск\
    нужно вначале ввести /parse [название города].')

@dp.message_handler(state = '*', commands = 'cancel')
@dp.message_handler(Text(equals = 'cancel', ignore_case = True), state = '*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled', reply_markup = types.ReplyKeyboardRemove())

@dp.message_handler(commands = 'parse')
async def send_parse(message: types.Message):
    User_city = message.get_args()
    print(User_city)
    parserPy.parse(User_city)
    for parserPy.worker in parserPy.workers:
        await message.reply(f'{parserPy.worker["title"]} \nЗП:{parserPy.worker["price"]}👛\nГород:{parserPy.worker["location"]}\nОписание:{parserPy.worker["description"]} \
        \nВремя публикации:{parserPy.worker["time"]}\n\nLink: https://rabota.ua{parserPy.worker["link"]}')
        time.sleep(1)

#if/else:

#end
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
