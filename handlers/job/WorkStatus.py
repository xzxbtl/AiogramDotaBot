from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.main import bot
from aiogramproject.base.TakeInfoBase import TakeInfo
from aiogramproject.logs import logger


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'status_jobs')
    async def send_menu_dota(query: CallbackQuery):
        user_id = query.from_user.id
        try:
            await query.answer("Вы переместились в Статус Работ 📊")
            job_name, status_job, take_award = await TakeInfo.take_status_job(user_id)
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_jobs_menu")
            if job_name == "Destroy Tower":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_destroy_tower")
                builder.row(but1, but2)
            elif job_name == "Attack Support":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_attack_support")
                builder.row(but1, but2)
            elif job_name == "Call Fight":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_call_fight")
                builder.row(but1, but2)
            elif job_name == "Destroy Ward":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_destroy_ward")
                builder.row(but1, but2)
            elif job_name == "Exit Line":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_exit_line")
                builder.row(but1, but2)
            elif job_name == "Farming Jungle":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_jungle")
                builder.row(but1, but2)
            elif job_name == "Kill Carry":
                but2 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_kill_carry")
                builder.row(but1, but2)
            else:
                builder.row(but1)
            await bot.edit_message_text(message_id=query.message.message_id,
                                        chat_id=query.message.chat.id,
                                        text=f"Вы попали в меню по *вашим работам* \n \nНа данный момент вы заняты "
                                             f"*работой*: " \
                                             f"`{ 'Работы нет' if job_name is None else job_name}` \n \n"
                                             f"Помните, чтобы начать новую работу, необходимо дождаться выполнения "
                                             f"*предыдущей работы* \n \n"
                                             f"Здесь по кнопке вы также можете получить *награду* за работу!",
                                        parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=builder.as_markup())

        except Exception as err:
            logger.error(f"Произошла ошибка: {err}")
