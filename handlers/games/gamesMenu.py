from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.main import bot
from aiogramproject.logs import logger


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'games_jobs')
    async def games_job_menu(query: CallbackQuery):
        await GamesMenu.send_menu_dota(query)


class GamesMenu:
    @staticmethod
    async def send_menu_dota(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_jobs_menu")
        but2 = InlineKeyboardButton(text="🥮 Коин-Флип", callback_data="coin-flip")
        but3 = InlineKeyboardButton(text="🎲 Угадайка", callback_data="choose_number")
        but4 = InlineKeyboardButton(text="⚔️ Дуэль", callback_data="duel")
        builder.row(but2, but3, but4, width=2)
        builder.row(but1)
        try:
            await query.answer("Вы переместились в меню Игр 🎮")
            await bot.edit_message_text(message_id=query.message.message_id,
                                        chat_id=query.message.chat.id,
                                        reply_markup=builder.as_markup(),
                                        text=f"* Меню Игр* \n "
                                             f"Здесь вы можете поучавствовать в разных играх \n `Желаем вам удачи!`",
                                        parse_mode=ParseMode.MARKDOWN)
        except Exception as err:
            await logger.error(f"games.menu.py - Произошла ошибка {err}")
