from aiogram import Bot, Dispatcher 
from asyncio import run

dp = Dispatcher()

bot = Bot('7707356933:AAF36G6W9l_ntaKkXRrQpU4n_65gpvReY_4')

async def start():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(start())

async def bot_order(order_user, bot):
    try:
        # Your async telegram bot logic here
        await bot.send_message(6089066974, f"Order User: {order_user}")
    except Exception as e:
        print(f"Error sending telegram message: {e}")