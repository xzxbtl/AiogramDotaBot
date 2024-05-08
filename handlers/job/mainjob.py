from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.main import bot
from aiogramproject.base.TakeInfoBase import TakeInfo
from aiogramproject.logs import logger


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'Job')
    async def send_menu_dota(query: CallbackQuery):
        try:
            await query.answer("Вы переместились в Заработок 💸")
            await JobMenu.menu_dota(query)
        except Exception as err:
            logger.error(f"Произошла ошибка: {err}")

    @dp.callback_query(lambda query: query.data == "all_Jobs")
    async def all_jobs(query: CallbackQuery):
        await JobsMenu.jobs_menu(query)

    @dp.callback_query(lambda query: query.data == "back_from_jobs_menu")
    async def back_from_jobs_menu(query: CallbackQuery):
        try:
            await query.answer("Вы вернулись в меню работ")
            await JobMenu.menu_dota(query)
        except Exception as err:
            logger.error(f"main job.py - Ошибка при перемещении в меню работ {err}")


class JobMenu:
    @staticmethod
    async def menu_dota(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="Работы 💼", callback_data="all_Jobs")
        but2 = InlineKeyboardButton(text="Игры 🎮", callback_data="games_jobs")
        but3 = InlineKeyboardButton(text="Статус работ 📊", callback_data="status_jobs")
        but4 = InlineKeyboardButton(text="⬅ Назад", callback_data="Menu")
        builder.row(but1, but2, but3, but4, width=3)
        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    text=f"*Вы попали в Заработок* 🔥\n Здесь вы можете устроится на работу для "
                                         f"*заработка*"
                                         f"\n Доступные работы зависят от ваших *статусов* \n Помните, что некоторые "
                                         f"работы имеют *риск* на провал",
                                    reply_markup=builder.as_markup(),
                                    parse_mode=ParseMode.MARKDOWN)


class JobsMenu:
    @staticmethod
    async def jobs_menu(query: CallbackQuery):
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        builder = InlineKeyboardBuilder()
        but8 = InlineKeyboardButton(text="⬅ Назад", callback_data="back_from_jobs_menu")
        if status != "Divine ☠️" and status != "Titan 🔥":
            but1 = InlineKeyboardButton(text="Пофармить в лесу 🌴", callback_data="farm_creeps_menu")
            but2 = InlineKeyboardButton(text="Выйти на лайн 🚸", callback_data="exit_from_line_menu")
            but3 = InlineKeyboardButton(text="Напасть на саппорта 🪓", callback_data="attack_enemy_support")
            but4 = InlineKeyboardButton(text="Сломать вражеский вард ⚒️", callback_data="destroy_enemy_ward_menu")
            builder.row(but1, but2, but3, but4, but8, width=2)
        else:
            but1 = InlineKeyboardButton(text="Пофармить в лесу 🌴", callback_data="farm_creeps_menu")
            but2 = InlineKeyboardButton(text="Выйти на лайн 🚸", callback_data="exit_from_line_menu")
            but3 = InlineKeyboardButton(text="Напасть на саппорта 🪓", callback_data="attack_enemy_support")
            but4 = InlineKeyboardButton(text="Сломать вражеский вард ⚒️", callback_data="destroy_enemy_ward_menu")
            but5 = InlineKeyboardButton(text="Убить вражеского кора 🩸", callback_data="kill_enemy_core")
            but6 = InlineKeyboardButton(text="Сломать тавер 💣", callback_data="destroy_tower_menu")
            but7 = InlineKeyboardButton(text="Заколить команду на файт ⚔️", callback_data="call_team_for_fight_menu")
            builder.row(but1, but2, but3, but4, but5, but6,but7, width=2)
            builder.row(but8, width=1)

        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        await bot.send_message(chat_id=query.message.chat.id,
                               reply_markup=builder.as_markup(),
                               text=f"*Выберите интересующую вас работу* \n "
                                    f"Помните, что каждая работа имеет своей "
                                    f"шанс *риска* \n Но этот риск оправдан "
                                    f"возможностью *большей* награды \n Удачи <3",
                               parse_mode=ParseMode.MARKDOWN)
