from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.games.gamesMenu import GamesMenu
from aiogramproject.main import bot
from aiogramproject.logs import logger
from random import randint


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'coin-flip')
    async def send_menu_coinflip(query: CallbackQuery):
        await RateValue.send_coin_menu(query, "coin-flip", 33)

    @dp.callback_query(lambda query: query.data == 'back_from_menu_dota')
    async def send_menu_back_games(query: CallbackQuery):
        await GamesMenu.send_menu_dota(query)

    @dp.callback_query(lambda query: query.data == '1000_from_coin-flip')
    async def award_from_1000_coin(query: CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        if balance >= 1000:
            await TakeAwardFromCoinFlip.award_from_coin(query, 1000)
        else:
            await query.answer("Недостаточна баланса")

    @dp.callback_query(lambda query: query.data == '3000_from_coin-flip')
    async def award_from_3000_coin(query: CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        if balance >= 3000:
            await TakeAwardFromCoinFlip.award_from_coin(query, 3000)
        else:
            await query.answer("Недостаточна баланса")

    @dp.callback_query(lambda query: query.data == '7000_from_coin-flip')
    async def award_from_7000_coin(query: CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        if balance >= 7000:
            await TakeAwardFromCoinFlip.award_from_coin(query, 7000)
        else:
            await query.answer("Недостаточна баланса")

    @dp.callback_query(lambda query: query.data == '20000_from_coin-flip')
    async def award_from_20000_coin(query: CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        if balance >= 20000:
            await TakeAwardFromCoinFlip.award_from_coin(query, 20000)
        else:
            await query.answer("Недостаточна баланса")


class TakeAwardFromCoinFlip:
    @staticmethod
    async def award_from_coin(query: CallbackQuery, bet):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        random_number = randint(0, 3)
        if random_number == 1:
            new_balance = balance + bet * 2
            await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
            await update_cache(user_id, new_balance)
            await query.answer(f"Вы выиграли {bet * 2}{emoji}")
        elif random_number == 0 or random_number == 3:
            new_balance = balance - bet
            await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
            await update_cache(user_id, new_balance)
            await query.answer(f"Вы проиграли {bet}{emoji}")


class RateValue:
    @staticmethod
    async def send_coin_menu(query, game, chance):
        user_id = query.from_user.id
        try:
            emoji = await TakeInfo.take_hidden_new_value(query)
            if emoji is None:
                emoji = "💎"
            builder = InlineKeyboardBuilder()
            but0 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_menu_dota")
            status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
            if 1000 <= balance and balance in range(1001,3000):
                but1 = InlineKeyboardButton(text=f"1000{emoji}", callback_data=f"1000_from_{game}")
                builder.row(but0, but1)
            elif 3000 <= balance and balance in range(3001,7000):
                but1 = InlineKeyboardButton(text=f"1000{emoji}", callback_data=f"1000_from_{game}")
                but2 = InlineKeyboardButton(text=f"3000{emoji}", callback_data=f"3000_from_{game}")
                builder.row(but1, but2, but0, width=1)
            elif 7000 <= balance and balance in range(7001,20000):
                but1 = InlineKeyboardButton(text=f"1000{emoji}", callback_data=f"1000_from_{game}")
                but2 = InlineKeyboardButton(text=f"3000{emoji}", callback_data=f"3000_from_{game}")
                but3 = InlineKeyboardButton(text=f"7000{emoji}", callback_data=f"7000_from_{game}")
                builder.row(but1, but2, but3, but0, width=1)
            elif balance >= 20000:
                but1 = InlineKeyboardButton(text=f"1000{emoji}", callback_data=f"1000_from_{game}")
                but2 = InlineKeyboardButton(text=f"3000{emoji}", callback_data=f"3000_from_{game}")
                but3 = InlineKeyboardButton(text=f"7000{emoji}", callback_data=f"7000_from_{game}")
                but4 = InlineKeyboardButton(text=f"20000{emoji}", callback_data=f"20000_from_{game}")
                builder.row(but1, but2, but3, but4, but0, width=1)
            else:
                builder.row(but0)

            await bot.edit_message_text(message_id=query.message.message_id,
                                        chat_id=query.message.chat.id,
                                        reply_markup=builder.as_markup(),
                                        text=f"Игра `{game.upper()}` \n Выберите нужную вам ставку \n "
                                             f"Риск *{chance}%* \n `Доступ к играм начинается при 1000 {emoji}`",
                                        parse_mode=ParseMode.MARKDOWN)
        except Exception as err:
            await logger.error(f"coinflip.py - Произошла ошибка {err}")
