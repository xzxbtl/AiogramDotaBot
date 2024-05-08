from aiogram import F
from aiogram.types import Message


def register_handlers(dp):
    @dp.message(F.text.lower() == "привет")
    async def hello_text(message: Message):
        await message.answer("И тебе привет!")

    @dp.message(F.photo)
    async def get_photo(message: Message):
        await message.answer("Классное фото")

    @dp.message(F.sticker)
    async def sticker(message: Message):
        await message.answer("Классный Стикер")

    @dp.message(F.animation)
    async def get_gif(message: Message):
        await message.answer("Вы прислали gif")
