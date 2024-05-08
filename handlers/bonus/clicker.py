from aiogram import Dispatcher, types
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from random import randint
from aiogramproject.handlers.Dota2.StatusBonuses.forclicker import MoreAwardWithStatusClicker


def register_handlers(dp: Dispatcher):
    @dp.callback_query(lambda query: query.data == 'Clicker')
    async def handle_clicker(query: types.CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        balance = await TakeInfo.take_balance(query)
        click_prize = randint(1, 3)
        award_status_click = MoreAwardWithStatusClicker(status, click_prize)
        prize_pool = await award_status_click.add_prize_pool()
        new_balance = balance + prize_pool
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        await TakeInfo.update_balance(user_id, new_balance)
        await update_cache(user_id, new_balance)
        await query.answer(f"Вам была выдана награда: {prize_pool} {emoji}", show_alert=False)
