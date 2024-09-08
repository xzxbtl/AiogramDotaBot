from datetime import datetime
from random import randint

from aiogram import Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.Dota2.StatusBonuses.fortime import PassiveAwardWithStatus
from aiogramproject.handlers.bonus.clicker import keyboard
from aiogramproject.handlers.start import MainMenu
from aiogramproject.main import bot
from aiogramproject.logs import logger


class Timely:
    def __init__(self):
        self.last_execution = {}


obj_timely = Timely()


def register_handlers(dp: Dispatcher):
    @dp.callback_query(lambda query: query.data == 'Bonus')
    async def handle_main_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы Переместились в Бонус-Меню", show_alert=False)

        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        except Exception as e:
            logger.info(f"bonus.py - Ошибка при удалении сообщения: {e}")

        await BonusMenu.bonus(query)

    @dp.callback_query(lambda query: query.data == 'Back')
    async def handle_main_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы вернулись в главное меню", show_alert=False)

        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        except Exception as e:
            logger.info(f"bonus.py - Ошибка при удалении сообщения: {e}")

        await MainMenu.main_menu(query)

    @dp.callback_query(lambda query: query.data == 'Daily')
    async def handle_daily_menu(query: types.CallbackQuery):
        user_id = query.from_user.id
        current_time = datetime.now()
        last_execution_time = obj_timely.last_execution.get(query.from_user.id)

        if last_execution_time is not None:
            time_difference = current_time - last_execution_time
            if time_difference.total_seconds() < 43200:
                remaining_time_seconds = 43200 - time_difference.total_seconds()
                remaining_hours = int(remaining_time_seconds // 3600)
                remaining_minutes = int((remaining_time_seconds % 3600) // 60)
                await query.answer(
                    f"Награда недоступна еще {remaining_hours} часов {remaining_minutes} минут")
                return

        obj_timely.last_execution[query.from_user.id] = current_time

        balance = await TakeInfo.take_balance(query)
        prize = randint(30, 100)
        new_balance = balance + prize
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        if balance is not None:
            await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
            await update_cache(user_id, new_balance)

        await query.answer(f"Вам была выдана награда: {prize} {emoji}")

    @dp.callback_query(lambda query: query.data == "take_hour_award")
    async def handle_hour_award(query: types.CallbackQuery):
        user_id = query.from_user.id
        prize_pool = 0
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        award = PassiveAwardWithStatus(status, prize_pool)
        award_def = await award.reward_for_time(user_id)
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        if award_def is None:
            await query.answer("Еще недоступно")
            return

        award_for_time = award_def + balance
        await TakeInfo.update_balance(user_id, award_for_time)
        await update_cache(user_id, award_for_time)
        await query.answer(f"Начислена награда за статус: {award_def} {emoji}")


class BonusMenu:
    @staticmethod
    async def bonus(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        builder = InlineKeyboardBuilder()
        if status == "Herald" or status == "Guardian":
            but_first = types.InlineKeyboardButton(text="🔥 Ежедневная награда", callback_data="Daily")
            but_second = types.InlineKeyboardButton(text="🤝 Приглашение друга", callback_data="Invite")
            but_four = types.InlineKeyboardButton(text="📣 Викторина", callback_data="Victorin")
            but_five = types.InlineKeyboardButton(text='<< Назад', callback_data='Back')
            builder.add(but_first)
            builder.row(but_second, but_four, but_five, width=2)
        else:
            but_first = types.InlineKeyboardButton(text="🔥 Ежедневная награда", callback_data="Daily")
            but_second = types.InlineKeyboardButton(text="🤝 Приглашение друга", callback_data="Invite")
            but_four = types.InlineKeyboardButton(text="📣 Викторина", callback_data="Victorin")
            but_five = types.InlineKeyboardButton(text='<< Назад', callback_data='Back')
            but_six = types.InlineKeyboardButton(text='Получить 🎁', callback_data='take_hour_award')
            builder.row(but_first, but_six, width=2)
            builder.row(but_second, but_four, but_five, width=2)

        await TakeInfo.user_cache_info_profile(user_id)
        hidden_id = await TakeInfo.take_hidden_id(callback)
        if hidden_id is True:
            user_id = '*********'

        emoji = await TakeInfo.take_hidden_new_value(callback)
        if emoji is None:
            emoji = "💎"

        return await bot.send_message(chat_id=callback.message.chat.id,
                                      text=f" *Бонус Меню* `{username}` \n Ваш ID: `{user_id}` \n Ваш Баланс: "
                                           f"`{balance}` {emoji}",
                                      reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
