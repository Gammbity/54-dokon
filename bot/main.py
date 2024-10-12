from aiogram import Bot, Dispatcher, F
from asyncio import run
from . import functions
from aiogram.filters import CommandStart
from . import states

dp = Dispatcher()

async def start_bot(bot:Bot):
    await bot.send_message(6089066974, "Bot ishga tushdi ✅")

async def shutdown_answer(bot:Bot):
    await bot.send_message(6089066974, "Bot ishdan to'xtadi ❓")

async def start():

    dp.startup.register(start_bot)
    
    dp.message.register(functions.start_command, CommandStart())
    dp.message.register(functions.send_password, states.Registration.login)
    dp.message.register(functions.get_contact, states.Registration.phone)
    dp.callback_query.register(functions.recovery_password, F.data == 'password_recovery')

    dp.shutdown.register(shutdown_answer)

    bot = Bot('7288747513:AAGosDrwk8E_Owe8r1i_IzDc-6SY-lGePKM')

    await dp.start_polling(bot)

run(start())