from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.games.allgames.coinflip import RateValue
from aiogramproject.handlers.games.gamesMenu import GamesMenu
from aiogramproject.main import bot
from random import randint
import random

user_bet_values = {}


class RandomNumber:
    @staticmethod
    async def take_digital(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        builder = InlineKeyboardBuilder()
        but0 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_menu_dota")
        but1 = InlineKeyboardButton(text=f"{randint(1, 23)}", callback_data=f"success_award_guestion")
        but2 = InlineKeyboardButton(text=f"{randint(24, 50)}", callback_data="cancel_award_guestion")
        but3 = InlineKeyboardButton(text=f"{randint(32, 124)}", callback_data="cancel_award_guestion")
        list_buttons = [but1, but2, but3]
        random.shuffle(list_buttons)
        for button in list_buttons:
            builder.row(button, width=3)
        builder.row(but0)
        await bot.edit_message_text(message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=builder.as_markup(),
                                    text="Пожалуйста выберите число \n `у вас одна попытка` \n `Доступ к играм "
                                         f"начинается при 1000 {emoji}`",
                                    parse_mode=ParseMode.MARKDOWN)


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'choose_number')
    async def send_menu_coinflip(query: CallbackQuery):
        await RateValue.send_coin_menu(query, "guestion-game", 33)

    @dp.callback_query(lambda query: query.data == '1000_from_guestion-game')
    async def award_from_1000_guestion_game(query: CallbackQuery):
        await RandomNumber.take_digital(query)
        user_id = query.from_user.id
        user_bet_values[user_id] = 1000
        return user_bet_values[user_id]

    @dp.callback_query(lambda query: query.data == '3000_from_guestion-game')
    async def award_from_3000_guestion_game(query: CallbackQuery):
        await RandomNumber.take_digital(query)
        user_id = query.from_user.id
        user_bet_values[user_id] = 3000
        return user_bet_values[user_id]

    @dp.callback_query(lambda query: query.data == '7000_from_guestion-game')
    async def award_from_7000_guestion_game(query: CallbackQuery):
        await RandomNumber.take_digital(query)
        user_id = query.from_user.id
        user_bet_values[user_id] = 7000
        return user_bet_values[user_id]

    @dp.callback_query(lambda query: query.data == '20000_from_guestion-game')
    async def award_from_20000_guestion_game(query: CallbackQuery):
        await RandomNumber.take_digital(query)
        user_id = query.from_user.id
        user_bet_values[user_id] = 20000
        return user_bet_values[user_id]

    @dp.callback_query(lambda query: query.data == "success_award_guestion")
    async def success_question_award(query: CallbackQuery):
        user_id = query.from_user.id
        bet = user_bet_values.get(user_id)
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        new_balance = balance + bet * 3
        await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
        await update_cache(user_id, new_balance)
        await query.answer(f"Вы выиграли {bet * 3}{emoji}")
        await GamesMenu.send_menu_dota(query)

    @dp.callback_query(lambda query: query.data == "cancel_award_guestion")
    async def cancel_question_award(query: CallbackQuery):
        user_id = query.from_user.id
        bet = user_bet_values.get(user_id)
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        new_balance = balance - bet
        await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
        await update_cache(user_id, new_balance)
        await query.answer(f"Вы проиграли {bet}{emoji}")
        await GamesMenu.send_menu_dota(query)
