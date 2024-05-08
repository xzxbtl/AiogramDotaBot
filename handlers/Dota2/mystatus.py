from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogramproject.main import bot
from aiogram import types
from aiogramproject.base.TakeInfoBase import TakeInfo
from aiogramproject.handlers.Dota2.statuList import StatusList

user_page_indices = {}
status_menu = StatusList.status_menu


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'MyStatus')
    async def handle_user_status_menu(query: types.CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        status_tuples = await TakeInfo.get_status_list(user_id)
        status_list = [status[0] for status in status_tuples]
        current_page_index = user_page_indices.get(user_id, 0)
        status_data = status_menu[current_page_index]
        builder = InlineKeyboardBuilder()

        if status_data["name"] in status_list:
            if current_page_index == 7:
                if status_data["name"] == status:
                    but1 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    but2 = types.InlineKeyboardButton(text="Меню ☰", callback_data="Dota2")
                    builder.row(but1, but2, width=1)
                else:
                    but1 = types.InlineKeyboardButton(text="Выбрать ✅", callback_data="choose_status")
                    but2 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    but3 = types.InlineKeyboardButton(text="Меню ☰", callback_data="Dota2")
                    builder.row(but2, but1, but3, width=2)

            else:
                if status_data["name"] != status:
                    but1 = types.InlineKeyboardButton(text="Выбрать ✅", callback_data="choose_status")
                    but2 = types.InlineKeyboardButton(text="Вперед ➡️", callback_data="Next_status_item")
                    but3 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    builder.row(but3, but1, but2, width=2)
                else:
                    but1 = types.InlineKeyboardButton(text="Вперед ➡️", callback_data="Next_status_item")
                    but2 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    builder.row(but2, but1, width=2)
        else:
            if status_data["name"] != "Herald":
                if current_page_index != 7:
                    but1 = types.InlineKeyboardButton(text="Недоступен ❌", callback_data="Status")
                    but2 = types.InlineKeyboardButton(text="Вперед ➡️", callback_data="Next_status_item")
                    but3 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    builder.row(but3, but1, but2, width=2)
                else:
                    but1 = types.InlineKeyboardButton(text="Недоступен ❌", callback_data="Status")
                    but3 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_status_item")
                    but2 = types.InlineKeyboardButton(text="Меню ☰", callback_data="Dota2")
                    builder.row(but3, but1, but2, width=2)
            else:
                but1 = types.InlineKeyboardButton(text="Выбрать ✅", callback_data="choose_status")
                but2 = types.InlineKeyboardButton(text="Вперед ➡️", callback_data="Next_status_item")
                but3 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Dota2")
                builder.row(but3, but1, but2, width=2)

        image_from_pc = FSInputFile(status_data["image_path"])
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.send_photo(
            chat_id=query.message.chat.id,
            photo=image_from_pc,
            caption=f"*{status_data['name']}*\n\n{status_data['description']}\n",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN
        )
        user_page_indices[user_id] = current_page_index

    @dp.callback_query(lambda query: query.data == 'Back_status_item')
    async def back_shop_item(query: types.CallbackQuery):
        user_id = query.from_user.id
        if user_id in user_page_indices and user_page_indices[user_id] > 0:
            user_page_indices[user_id] -= 1
            await bot.answer_callback_query(query.id)
            await handle_user_status_menu(query)

    @dp.callback_query(lambda query: query.data == 'Next_status_item')
    async def next_shop_item(query: types.CallbackQuery):
        user_id = query.from_user.id
        if user_id in user_page_indices and user_page_indices[user_id] < len(status_menu) - 1:
            user_page_indices[user_id] += 1
            await bot.answer_callback_query(query.id)
            await handle_user_status_menu(query)

    @dp.callback_query(lambda query: query.data == "choose_status")
    async def choose_status(query: types.CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        status_data = status_menu[user_page_indices[user_id]]
        if status_data["name"] != status:
            await bot.answer_callback_query(query.id)
            await TakeInfo.update_satus(user_id, status_data["name"])
            await query.answer(f"Вы успешно изменили статус на {status_data['name']}")
        else:
            await query.answer("У вас и так установлен этот статус!")
