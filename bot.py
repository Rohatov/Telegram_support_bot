import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '7117772615:AAFFXd16wQ702UOkYxb_ykHRCZfTEUbwv_g'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
group_chat_id = -1002028167154
temp_data = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Sizga qanday yordam berolaman")



@dp.message_handler(content_types=types.ContentType.TEXT, chat_id=group_chat_id)
async def handle_message_from_group(message: types.Message):
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        original_message_id = message.reply_to_message.message_id
        user_id = temp_data.get(original_message_id)
        if user_id:
            await bot.send_message(chat_id=user_id, text=message.text)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def forward_to_admins(message: types.Message):
    message_id = message.message_id  
    user_id = message.from_user.id 
    forwarded_message = await bot.forward_message(chat_id=group_chat_id, from_chat_id=user_id, message_id=message_id)
    await message.answer("Sizning Habaringiz Muvaffaqiyatli Yuborildi Tez orada Hodimlarimiz Javob Berishadi")
    temp_data[forwarded_message.message_id] = user_id


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
