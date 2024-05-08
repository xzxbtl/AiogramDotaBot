from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.main import bot


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'duel')
    async def send_menu_duel(query: CallbackQuery):
        await Duels.take_duel_menu(query)


class Duels:
    @staticmethod
    async def take_duel_menu(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but0 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_menu_dota")
        builder.row(but0)
        await bot.edit_message_text(message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=builder.as_markup(),
                                    text="*В разработке* \n `developing...` ⚙️",
                                    parse_mode=ParseMode.MARKDOWN)
