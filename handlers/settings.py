from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogramproject.base.TakeInfoBase import TakeInfo
from aiogramproject.main import bot


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'settings')
    async def info_from_button(query: CallbackQuery):
        builder = InlineKeyboardBuilder()

        but1 = InlineKeyboardButton(text="Показать ID ✔️", callback_data="hidden_user_id")
        but2 = InlineKeyboardButton(text="Сменить валюту 🔄", callback_data="swap_emoji")
        but3 = InlineKeyboardButton(text="<< Назад", callback_data="Menu")
        builder.row(but1, but2, but3, width=1)

        await bot.edit_message_text(f"Функция находится в разработке ⚡⚙️",
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=builder.as_markup())

    @dp.callback_query(lambda query: query.data == "hidden_user_id")
    async def hidden_user_id(query: CallbackQuery):
        user_id = query.from_user.id
        hidden_status = await TakeInfo.take_hidden_id(query)
        builder = InlineKeyboardBuilder()

        if hidden_status is None or hidden_status is False:
            new_hidden_status = True
            action_text = "скрыли"
            but1 = InlineKeyboardButton(text="Показать ID ✔️", callback_data="hidden_user_id")
            but2 = InlineKeyboardButton(text="Сменить валюту 🔄", callback_data="swap_emoji")
            but3 = InlineKeyboardButton(text="<< Назад", callback_data="Menu")
            builder.row(but1, but2, but3, width=1)

        else:
            new_hidden_status = False
            action_text = "показали"
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="Скрыть ID ❌", callback_data="hidden_user_id")
            but2 = InlineKeyboardButton(text="Сменить валюту 🔄", callback_data="swap_emoji")
            but3 = InlineKeyboardButton(text="<< Назад", callback_data="Menu")
            builder.row(but1, but2, but3, width=1)

        await TakeInfo.hide_user_id(user_id, new_hidden_status)
        await query.answer(f"Вы успешно {action_text} ID")
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text="Функции находятся в разработке ⚡⚙️",
                                    reply_markup=builder.as_markup())

    @dp.callback_query(lambda query: query.data == "swap_emoji")
    async def new_emoji_menu(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="🔥", callback_data="fire_emoji")
        but2 = InlineKeyboardButton(text="💸", callback_data="dollar_emoji")
        but3 = InlineKeyboardButton(text="⚡", callback_data="lightning")
        but4 = InlineKeyboardButton(text="💎", callback_data="diamond")
        but5 = InlineKeyboardButton(text="<< Назад", callback_data="settings")
        builder.row(but1, but2, but3, but4, but5, width=2)
        await bot.edit_message_text(message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    text="Выберите эмодзи валюты",
                                    reply_markup=builder.as_markup())

    async def handle_emoji(query: CallbackQuery, new_emoji: str):
        user_id = query.from_user.id
        hidden_status = await TakeInfo.take_hidden_id(query)
        if hidden_status is None:
            hidden_status = False
            await TakeInfo.hide_user_id(user_id, hidden_status)
        check_emoji = await TakeInfo.take_hidden_new_value(query)

        if check_emoji is None:
            await TakeInfo.new_emoji(user_id, new_emoji)
            await query.answer(f"Вы успешно установили валюту на {new_emoji}")
        elif check_emoji == new_emoji:
            await query.answer("У вас уже установлена данная валюта")
        else:
            await TakeInfo.new_emoji(user_id, new_emoji)
            await query.answer(f"Вы успешно обновили валюту на {new_emoji}")

    @dp.callback_query(lambda query: query.data == "fire_emoji")
    async def emoji_fire(query: CallbackQuery):
        await handle_emoji(query, "🔥")

    @dp.callback_query(lambda query: query.data == "dollar_emoji")
    async def dollar_emoji(query: CallbackQuery):
        await handle_emoji(query,  "💸")

    @dp.callback_query(lambda query: query.data == "lightning")
    async def lightning_emoji(query: CallbackQuery):
        await handle_emoji(query, "⚡️")

    @dp.callback_query(lambda query: query.data == "diamond")
    async def diamond_emoji(query: CallbackQuery):
        await handle_emoji(query, "💎")
