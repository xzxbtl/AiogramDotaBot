from aiogram import Dispatcher, types
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogramproject.handlers.bonus.bonus import BonusMenu
from aiogramproject.logs import logger
from aiogramproject.main import bot


def register_handlers(dp: Dispatcher):
    @dp.callback_query(lambda query: query.data == 'Invite')
    async def handle_invite_click(query: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        but = types.InlineKeyboardButton(text='<< Закрыть', callback_data='Back_awards')
        builder.add(but)
        await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        ref_link = await create_start_link(bot, str(query.from_user.id), encode=True)
        await query.message.answer(f"Поделитесь своей реферальной ссылкой: {ref_link}",
                                   reply_markup=builder.as_markup())

    @dp.callback_query(lambda query: query.data == 'Back_awards')
    async def handle_bonus_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы вернулись в Бонусное меню", show_alert=False)
        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
            await BonusMenu.bonus(query)
        except Exception as e:
            logger.info(f"link.py - Ошибка при удалении сообщения: {e}")
