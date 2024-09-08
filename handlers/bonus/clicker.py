import json

from aiogram import Dispatcher, types, F
from aiogram.enums import ContentType
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.Dota2.StatusBonuses.forclicker import MoreAwardWithStatusClicker

web_app = WebAppInfo(url="https://xzxbtl.github.io/")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🖱️ Кликер", web_app=web_app)]
    ],
    resize_keyboard=True,
)


def register_handlers(dp: Dispatcher):
    @dp.message(F.content_type == ContentType.WEB_APP_DATA)
    async def handle_clicker(message: types.Message):
        score_str = message.web_app_data.data

        try:
            score = int(score_str)
        except ValueError:
            await message.answer("Ошибка: Некорректные данные.")
            return

        user_id = message.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        balance = await TakeInfo.take_balance(message)
        award_status_click = MoreAwardWithStatusClicker(status, score)
        prize_pool = await award_status_click.add_prize_pool()
        new_balance = balance + prize_pool
        emoji = await TakeInfo.take_hidden_new_value(message)
        if emoji is None:
            emoji = "💎"

        await TakeInfo.update_balance(user_id, new_balance)
        await update_cache(user_id, new_balance)
        await message.answer(f"Вам была выдана награда: {prize_pool} {emoji}", show_alert=False)
