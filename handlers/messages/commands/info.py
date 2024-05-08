from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder


def register_handlers(dp):
    @dp.message(Command("info"))
    async def cmd_info(message: Message, started_at: str):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="Задать вопрос ⁉", url="https://t.me/qxzxbtlqq")
        builder.row(but1)
        await message.answer(f"Бот был разработан пользователем : *xzxbtl* \n"
                             f"Айди : `6583339296`\n"
                             f"Написан на aiogram 3.4.2 | postgresql/sqlalchemy \n"
                             f"Последний запуск: {started_at}",
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=builder.as_markup())
