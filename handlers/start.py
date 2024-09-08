from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Dispatcher, types
from aiogram.enums import ParseMode
from aiogram import Bot

from aiogramproject.handlers.bonus.clicker import keyboard
from aiogramproject.logs import logger
from aiogramproject.base.main.core import async_engine
from aiogramproject.base.models import users_table
from aiogramproject.env.config_reader import config
from aiogramproject.base.TakeInfoBase import TakeInfo

bot = Bot(token=config.bot_token.get_secret_value())


def register_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        user_id = message.from_user.id
        async with async_engine.connect() as conn:
            query = users_table.select().where(users_table.c.user_id == user_id)
            result = await conn.execute(query)
            row = result.fetchone()
        if row is not None:
            await MainMenu.main_menu_letter(message)
            await bot.send_message(chat_id=message.chat.id,
                                   text="Приложения Бота",
                                   reply_markup=keyboard)
        else:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text="Нажмите на кнопку, если готовы продолжить ✅",
                callback_data="message_second",
            )
            )
            reply_message = await message.answer(
                "Здравствуйте, рады вас видеть",
                reply_markup=builder.as_markup(),
            )
            dp['initial_message_id'] = reply_message.message_id

    @dp.callback_query(lambda query: query.data == 'message_second')
    async def process_age_selection(callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text="👶🏻 6-10", callback_data="age_6_10"),
            types.InlineKeyboardButton(text="👦🏻 10-14", callback_data="age_10_14"),
            types.InlineKeyboardButton(text="👨‍🎓 14-18", callback_data="age_14_18"),
            types.InlineKeyboardButton(text="👨🏻‍💼 18+", callback_data="age_18_plus")
        )

        await bot.edit_message_text(chat_id=callback.message.chat.id, text="Пожалуйста, выберите ваш возраст:",
                                    reply_markup=builder.as_markup(), message_id=dp['initial_message_id'])

    @dp.callback_query(lambda query: query.data.startswith('age_'))
    async def process_selected_age(callback: types.CallbackQuery):
        age_mapping = {
            "age_6_10": "Дети 6-10 лет",
            "age_10_14": "Подростки 10-14 лет",
            "age_14_18": "Подростки 14-18 лет",
            "age_18_plus": "Взрослые 18+ лет"
        }
        age_key = callback.data
        age_description = age_mapping.get(age_key)
        if age_description:
            # сохранение возрастной категории в базе данных
            status = "Herald"
            balance = 0
            user_id = callback.from_user.id
            username = callback.from_user.username
            if username is not None:
                username = callback.from_user.username
            else:
                username = user_id
            async with async_engine.connect() as conn:
                stmt = users_table.insert().values(
                    username=username,
                    user_id=user_id,
                    age=age_description,
                    Confirmed=True,
                    Status=status,
                    Balance=balance
                )
                await conn.execute(stmt)
                await conn.commit()

            await callback.answer(f"Вы выбрали возрастную категорию: {age_description}")
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=dp['initial_message_id'])
            await MainMenu.main_menu(callback)
        else:
            logger.error(f"start.py - Ошибка при выборе категории возраста")

    @dp.callback_query(lambda query: query.data == 'Menu')
    async def handle_main_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы вернулись в главное меню", show_alert=False)

        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        except Exception as err:
            logger.info(f"start.py - Ошибка при удалении сообщения: {err}")

        await MainMenu.main_menu(query)


class MainMenu:
    @staticmethod
    async def main_menu(callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        but_first = types.InlineKeyboardButton(text="☰ Главное меню", callback_data="Menu")
        but_second = types.InlineKeyboardButton(text="🎮 Dota 2", callback_data="Dota2")
        but_third = types.InlineKeyboardButton(text="💸 Заработок", callback_data="Job")
        but_four = types.InlineKeyboardButton(text="🎁 Бонус", callback_data="Bonus")
        but_five = types.InlineKeyboardButton(text='🛠 Настройки', callback_data='settings')
        but_six = types.InlineKeyboardButton(text="📋 Инфо", callback_data="Info")
        but_seven = types.InlineKeyboardButton(text="Поддержать проект 💪", callback_data="support_project")
        builder.add(but_first)
        builder.row(but_second, but_third, width=2)
        builder.row(but_four, but_five, but_seven, width=2)
        builder.row(but_six)

        user_id = callback.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        await TakeInfo.user_cache_info_profile(user_id)
        hidden_id = await TakeInfo.take_hidden_id(callback)
        if hidden_id is True:
            user_id = '*********'

        emoji = await TakeInfo.take_hidden_new_value(callback)
        if emoji is None:
            emoji = "💎"

        return await bot.send_message(chat_id=callback.message.chat.id,
                                      text=f" 📕 *Главное меню* `{username}` \n "
                                           f"Ваш ID: `{user_id}` \n "
                                           f"Ваш статус: `{status}` \n "
                                           f"Ваш Баланс: `{balance}` {emoji}",
                                      reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    async def main_menu_letter(message: types.Message):
        builder = InlineKeyboardBuilder()
        but_first = types.InlineKeyboardButton(text="☰ Главное меню", callback_data="Menu")
        but_second = types.InlineKeyboardButton(text="🎮 Dota 2", callback_data="Dota2")
        but_third = types.InlineKeyboardButton(text="💸 Заработок", callback_data="Job")
        but_four = types.InlineKeyboardButton(text="🎁 Бонус", callback_data="Bonus")
        but_five = types.InlineKeyboardButton(text='🛠 Настройки', callback_data='settings')
        but_six = types.InlineKeyboardButton(text="📋 Инфо", callback_data="Info")
        but_seven = types.InlineKeyboardButton(text="Поддержать проект 💪", callback_data="support_project")
        builder.add(but_first)
        builder.row(but_second, but_third, width=2)
        builder.row(but_four, but_five, but_seven, width=2)
        builder.row(but_six)

        user_id = message.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        await TakeInfo.user_cache_info_profile(user_id)
        hidden_id = await TakeInfo.take_hidden_id(message)
        if hidden_id is True:
            user_id = '*********'

        emoji = await TakeInfo.take_hidden_new_value(message)

        if emoji is None:
            emoji = "💎"

        return await bot.send_message(chat_id=message.chat.id,
                                      text=f" 📕 *Главное меню* `{username}` \n "
                                           f"Ваш ID: `{user_id}` \n "
                                           f"Ваш статус: `{status}` \n "
                                           f"Ваш Баланс: `{balance}` {emoji}",
                                      reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
