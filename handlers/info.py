from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogramproject.main import bot


class InfoMenu:
    @staticmethod
    async def info_from_button(query: CallbackQuery, started_at: str):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="Задать вопрос ⁉", url="https://t.me/qxzxbtlqq")
        but3 = InlineKeyboardButton(text="<< Назад", callback_data="Menu")
        builder.row(but3, but1, width=2)
        await bot.edit_message_text(f"Бот был разработан пользователем : *xzxbtl* \n"
                                    f"Айди : `6583339296`\n"
                                    f"Написан на aiogram 3.4.2 | postgresql/sqlalchemy \n"
                                    f"Последний запуск: {started_at} \n\nВерсия бота: `1.1.0`",
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=builder.as_markup())


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'Info')
    async def info_from_button(query: CallbackQuery, started_at: str):
        await InfoMenu.info_from_button(query, started_at)

    @dp.callback_query(lambda query: query.data == 'support_project')
    async def supported_project(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but0 = InlineKeyboardButton(text="<< Назад", callback_data="Menu")
        builder.row(but0)
        await bot.edit_message_text(message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    text="*Поддержать меня можно через:* \n Сбербанк - `2202 2024 3890 4314` | `4279 "
                                         "3806 4570 7755` \n Тинькофф - `2200 7009 4703 1901` \n Буду рад каждой "
                                         "копейке! <3",
                                    reply_markup=builder.as_markup(),
                                    parse_mode=ParseMode.MARKDOWN)
