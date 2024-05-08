from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogramproject.main import bot
from aiogram import types
from aiogramproject.logs import logger
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.Dota2.statuList import StatusList

status_menu = StatusList.status_menu
user_page_indices = {}


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'Dota2')
    async def handle_main_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы Переместились в Дота-Меню", show_alert=False)

        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        except Exception as err:
            logger.info(f"menu.py - Ошибка при удалении сообщения: {err}")

        await DotaMenu.menu_dota(query)

    @dp.callback_query(lambda query: query.data == 'Status')
    async def handle_status_menu_callback(query: types.CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        status_tuples = await TakeInfo.get_status_list(user_id)
        status_list = [status[0] for status in status_tuples]
        current_page_index = user_page_indices.get(user_id, 0)

        if current_page_index < len(status_menu):
            status_data = status_menu[current_page_index]

            builder = InlineKeyboardBuilder()

            if current_page_index == 7:
                if status_data["name"] != status and status_data["name"] not in status_list:
                    but1 = types.InlineKeyboardButton(text="Купить 💰", callback_data="Buy_status")
                    but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Back_shop_item")
                    but3 = types.InlineKeyboardButton(text="Меню ☰", callback_data="Dota2")
                    builder.row(but2, but1, but3, width=2)
                else:
                    but1 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Back_shop_item")
                    but2 = types.InlineKeyboardButton(text="Меню ☰", callback_data="Dota2")
                    builder.row(but1, but2, width=1)

            elif current_page_index == 0:
                but1 = types.InlineKeyboardButton(text="Вперед ➡", callback_data="Next_shop_item")
                but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Dota2")
                builder.row(but2, but1, width=2)

            else:
                if status_data["name"] != status and status_data["name"] not in status_list:
                    but1 = types.InlineKeyboardButton(text="Купить 💰", callback_data="Buy_status")
                    but2 = types.InlineKeyboardButton(text="Вперед ➡", callback_data="Next_shop_item")
                    but3 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Back_shop_item")
                    builder.row(but3, but1, but2, width=2)
                else:
                    but1 = types.InlineKeyboardButton(text="Вперед ➡", callback_data="Next_shop_item")
                    but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Back_shop_item")
                    builder.row(but2, but1, width=2)

            image_from_pc = FSInputFile(status_data["image_path"])
            await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

            await bot.send_photo(
                chat_id=query.message.chat.id,
                photo=image_from_pc,
                caption=f"*{status_data['name']}*\n\n{status_data['description']}\n\n*Цена*: {status_data['price']}"
                        f"{emoji}",
                reply_markup=builder.as_markup(),
                parse_mode=ParseMode.MARKDOWN
            )
            user_page_indices[user_id] = current_page_index

    @dp.callback_query(lambda query: query.data == 'Back_shop_item')
    async def back_shop_item(query: types.CallbackQuery):
        user_id = query.from_user.id
        if user_id in user_page_indices and user_page_indices[user_id] > 0:
            user_page_indices[user_id] -= 1
            await bot.answer_callback_query(query.id)
            await handle_status_menu_callback(query)

    @dp.callback_query(lambda query: query.data == 'Next_shop_item')
    async def next_shop_item(query: types.CallbackQuery):
        user_id = query.from_user.id
        if user_id in user_page_indices and user_page_indices[user_id] < len(status_menu) - 1:
            user_page_indices[user_id] += 1
            await bot.answer_callback_query(query.id)
            await handle_status_menu_callback(query)

    @dp.callback_query(lambda query: query.data == 'Buy_status')
    async def next_shop_item(query: types.CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        current_page_index = user_page_indices.get(user_id, 0)
        await TakeInfo.user_cache_info_profile(user_id)
        if status != status_menu[current_page_index]["name"]:
            if balance >= status_menu[current_page_index]["price"]:
                new_balance = balance - status_menu[current_page_index]["price"]
                status = status_menu[current_page_index]["name"]
                await TakeInfo.update_balance(user_id, new_balance)
                await update_cache(user_id, new_balance)
                await TakeInfo.update_satus(user_id, status)
                await TakeInfo.create_status(user_id, status)
                await query.answer(f"Поздравляем с успешным приобретением статуса {status}")
                status_menu[current_page_index]["is_purchased"] = True
            else:
                await query.answer(
                    f"У вас недостаточно валюты для покупки {status_menu[current_page_index]['name']} нужно еще: "
                    f"{status_menu[current_page_index]['price'] - balance}")
        else:
            await query.answer(f"У вас уже имеется данный статус")


class DotaMenu:
    @staticmethod
    async def menu_dota(callback: types.CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(callback)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but_first = types.InlineKeyboardButton(text="🔥 DotaBuff", callback_data="DotaBuff")
        but_second = types.InlineKeyboardButton(text="👀 Статус", callback_data="Status")
        but_third = types.InlineKeyboardButton(text="🛒 Магазин", callback_data="Shop")
        but_four = types.InlineKeyboardButton(text='<< Назад', callback_data='Back')
        but_five = types.InlineKeyboardButton(text='Мои статусы', callback_data='MyStatus')
        builder.row(but_first, but_second, but_third, but_five, width=3)
        builder.row(but_four, width=1)

        user_id = callback.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        await TakeInfo.user_cache_info_profile(user_id)
        hidden_id = await TakeInfo.take_hidden_id(callback)
        if hidden_id is True:
            user_id = '*********'

        return await bot.send_message(chat_id=callback.message.chat.id,
                                      text=f" *Статус Меню* `{username}` \n Ваш ID: `{user_id}` \n Ваш Баланс: "
                                           f"`{balance}` {emoji} \n Ваш статус: `{status}`",
                                      reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
