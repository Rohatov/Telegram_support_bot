import logging
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from asyncpg import Connection, Record, connect  
from database import get_connection, init_db
API_TOKEN = '7117772615:AAFFXd16wQ702UOkYxb_ykHRCZfTEUbwv_g'
group_chat_id = '-1002028167154'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Sizga qanday yordam berolaman")

@dp.message_handler(content_types=types.ContentType.TEXT, chat_id=group_chat_id)
async def handle_message_from_group(message: types.Message):
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        original_message_id = message.reply_to_message.message_id
        conn = await get_connection()
        try:
            row = await conn.fetchrow("SELECT user_id FROM message_mappings WHERE original_message_id = $1", original_message_id)
            if row:
                user_id = row['user_id']
                await bot.send_message(chat_id=user_id, text=message.text)
        finally:
            await conn.close()

@dp.message_handler(content_types=types.ContentType.TEXT)
async def forward_to_admins(message: types.Message):
    message_id = message.message_id
    user_id = message.from_user.id
    forwarded_message = await bot.forward_message(chat_id=group_chat_id, from_chat_id=user_id, message_id=message_id)
    await message.answer("Sizning Habaringiz Muvaffaqiyatli Yuborildi Tez orada Hodimlarimiz Javob Berishadi")
    conn = await get_connection()
    try:
        await conn.execute("INSERT INTO message_mappings (original_message_id, user_id) VALUES ($1, $2)", forwarded_message.message_id, user_id)
    finally:
        await conn.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    executor.start_polling(dp, skip_updates=True)
