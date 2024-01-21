import asyncio
import os

import openpyxl
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.functions import add_plus, get_salary, add_user, save_file
from utils.database import Database

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ['TOKEN']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db = Database("data/db.sqlite3")
reply_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Raqamni Yuborish", request_contact=True)]],
                                     resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: types.Message):
    """
        start command,
        returns a greeting text and a button to send contact information
    """
    add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    await message.answer("Salom!Malumotni korish uchun pastdagi tugmani bosing!", reply_markup=reply_keyboard)


@dp.message(F.contact)
async def get_contact(message: types.Message):
    """
        accepts the contact,
        passes it through the add_plus function and passes it to the get_salary function and
        sends the result to the user
    """
    add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    contact = message.contact
    contact = add_plus(contact.phone_number)
    await message.answer("Raqam muvofaqiyatli royhatdan otdi!Hisob izlanmoqda...")
    info = get_salary(contact)
    await bot.send_message(message.chat.id, info, parse_mode="html")


@dp.message(F.document)
async def admin_work(message: types.Message):
    """
        First of all, the telegram ID is checked,
        if it matches the administrator’s telegram ID,
        it accepts the file and passes it to the save_file function
    """
    if message.chat.id == 819233688 or message.chat.id == 1031845328:
        document = message.document
        file_info = await bot.get_file(document.file_id)
        file_path = await bot.download_file(file_info.file_path)
        info = save_file(file_path)
        await bot.send_message(message.chat.id, info, parse_mode="html")
    else:
        await bot.send_message(message.chat.id, "<b>У вас нет прав для выполнения этой операции.</b>",
                               parse_mode="html")


@dp.message(Command("message"))
async def message_to_all(message: types.Message):
    """
        message command,
        first of all, the telegram ID is checked,
        if it matches the administrator’s telegram ID,
        accepts the text located after /message and sends it to all registered users
    """
    if message.from_user.id == 819233688:
        text = message.text[8:]
        users = db.get_users()
        for row in users:
            try:
                await bot.send_message(row[0], text)
                if row[1] != 1:
                    db.set_active(row[0], 1)
            except Exception as ex:
                db.set_active(row[0], 0)
                print(ex)


@dp.message(Command("users"))
async def user_list(message: types.Message):
    """
        first of all, the telegram ID is checked,
        if it matches the administrator’s telegram ID,
        then returns all users data
    """
    if message.from_user.id == 819233688:
        users = db.get_users()
        text = "\n".join([str(user) for user in users])
        await bot.send_message(819233688, text)


@dp.message()
async def answer_message(message: types.Message):
    """
        if the command or text is not recognized,
        it returns the text and a button to send contact information
    """
    await message.answer("'Raqamni yuborish' tugmasini bosing)", reply_markup=reply_keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
