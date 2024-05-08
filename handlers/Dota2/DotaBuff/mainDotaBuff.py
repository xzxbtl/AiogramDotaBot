from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogramproject.main import bot
from aiogram import types, F
from aiogramproject.handlers.Dota2.DotaBuff.requestsOpenDota import TakeInfoUser, SteamConvector
from aiogramproject.logs import logger


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'DotaBuff')
    async def handle_main_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы переместились в DotaBuff")
        try:
            builder = InlineKeyboardBuilder()
            but = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Dota2")
            builder.add(but)
            reply_message = await bot.edit_message_text(text="Укажите steam ID интересующего вас пользователя: "
                                                             "\n ID64! : по типу 765611989... \n Или ID3 из по "
                                                             "профиля 1255185187... ",
                                                        message_id=query.message.message_id,
                                                        chat_id=query.message.chat.id, reply_markup=builder.as_markup())
            dp['initial_message_id'] = reply_message.message_id
        except Exception as err:
            await logger.error(f"mainDotaBuff - Произошла ошибка {err}")

    @dp.message((F.text.startswith('7') & F.text.len() >= 6) | (F.text.startswith('1') & F.text.len() >= 6) | (F.text.startswith('2') & F.text.len() >= 6) | (F.text.startswith('3') & F.text.len() >= 6) | (F.text.startswith('3') & F.text.len() >= 6) | (F.text.startswith('4') & F.text.len() >= 6) | (F.text.startswith('5') & F.text.len() >= 6) | (F.text.startswith('6') & F.text.len() >= 6) | (F.text.startswith('8') & F.text.len() >= 6) | (F.text.startswith('9') & F.text.len() >= 6) | (F.text.startswith('0') & F.text.len() >= 6))
    async def take_id(message: types.Message):
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="🔑 Аккаунт", callback_data="Account_info")
        but2 = types.InlineKeyboardButton(text="🏆 Последние 10 матчей", callback_data="LastGames")
        but3 = types.InlineKeyboardButton(text="⚔️ Частые герои", callback_data="LastHeroes")
        but4 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Dota2")
        builder.row(but1, but2, but3, but4, width=3)
        await message.delete()
        reply_message = await bot.edit_message_text(text="Выберите доступные параметры",
                                                    message_id=dp['initial_message_id'],
                                                    chat_id=message.chat.id,
                                                    reply_markup=builder.as_markup())
        dp['menu_with_buttons'] = reply_message.message_id
        dp['user_id'] = message.text

    @dp.callback_query(lambda query: query.data == "Account_info")
    async def take_info_account(query: types.CallbackQuery):
        user_id = dp['user_id']
        try:
            if user_id.startswith('7'):
                convector = SteamConvector(user_id)
                take_user_winrate = TakeInfoUser(convector.steamid64_to_steamid32())
            else:
                take_user_winrate = TakeInfoUser(user_id)

            text_profile = take_user_winrate.take_user_winrate()
            builder = InlineKeyboardBuilder()
            but1 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_to_menu_id")
            builder.add(but1)
            reply_message = await bot.edit_message_text(text=text_profile,
                                                        message_id=dp["menu_with_buttons"],
                                                        chat_id=query.message.chat.id,
                                                        reply_markup=builder.as_markup())
            dp['menu_account'] = reply_message.message_id
        except Exception as err:
            logger.info(f"mainDotaBuff.py - Произошла ошибка! Возможно вы указали некорректный ID\n Ошибка : {err}")
            await query.answer("Возможно вы указали некорректный ID | Или профиль скрыт")

    @dp.callback_query(lambda query: query.data == "Back_to_menu_id")
    async def back_to_menu_with_info(query: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="🔑 Аккаунт", callback_data="Account_info")
        but2 = types.InlineKeyboardButton(text="🏆 Последние 10 матчей", callback_data="LastGames")
        but3 = types.InlineKeyboardButton(text="⚔️ Частые герои", callback_data="LastHeroes")
        but4 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Dota2")
        builder.row(but1, but2, but3, but4, width=3)

        await bot.edit_message_text(text="Выберите доступные параметры",
                                    message_id=dp['menu_account'],
                                    chat_id=query.message.chat.id,
                                    reply_markup=builder.as_markup())

    @dp.callback_query(lambda query: query.data == "LastHeroes")
    async def last_matches_profile(query: types.CallbackQuery):
        user_id = dp['user_id']
        try:
            convector = SteamConvector(user_id)
            take_user_winrate = TakeInfoUser(convector.steamid64_to_steamid32())
            text_profile = take_user_winrate.get_heroes_stats()
            text = "\n\n".join(text_profile)
            builder = InlineKeyboardBuilder()
            but1 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_to_menu_id")
            builder.add(but1)
            reply_message = await bot.edit_message_text(text=text,
                                                        message_id=dp["menu_with_buttons"],
                                                        chat_id=query.message.chat.id,
                                                        reply_markup=builder.as_markup())
            dp['menu_account'] = reply_message.message_id
        except Exception as err:
            logger.info(f" mainDotaBuff.py- Произошла ошибка! Возможно вы указали некорректный ID\n Ошибка : {err}")
            await query.answer("Возможно вы указали некорректный ID | Или профиль скрыт")

    @dp.callback_query(lambda query: query.data == "LastGames")
    async def last_matches_profile(query: types.CallbackQuery):
        user_id = dp['user_id']
        try:
            convector = SteamConvector(user_id)
            take_user_winrate = TakeInfoUser(convector.steamid64_to_steamid32())
            text_profile = take_user_winrate.take_last_matches()
            text = "\n\n".join(text_profile)
            builder = InlineKeyboardBuilder()
            but1 = types.InlineKeyboardButton(text="⬅️ Назад", callback_data="Back_to_menu_id")
            builder.add(but1)
            reply_message = await bot.edit_message_text(text=text,
                                                        message_id=dp["menu_with_buttons"],
                                                        chat_id=query.message.chat.id,
                                                        reply_markup=builder.as_markup())
            dp['menu_account'] = reply_message.message_id
        except Exception as err:
            logger.info(f" mainDotaBuff.py- Произошла ошибка! Возможно вы указали некорректный ID\n Ошибка : {err}")
            await query.answer("Возможно вы указали некорректный ID | Или профиль скрыт")
