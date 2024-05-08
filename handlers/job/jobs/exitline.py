from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.handlers.job.jobs.farmjungle import obj_job
from aiogramproject.handlers.job.randomforall.randomfunc import random_choice_with_probabilities, probabilities
from aiogramproject.logs import logger
from aiogramproject.main import bot
from aiogramproject.handlers.job.jobs.media.photo_patches.pathches import photo_path


class ExitLine:
    def __init__(self, job_name):
        self.set_job_name = job_name

    async def take_award_from_exit_line(self, query):
        user_id = query.from_user.id
        job_name, status_job, take_award = await TakeInfo.take_status_job(user_id)

        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="Начать ✔️", callback_data="start_exit_line")
        but2 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_jobs_all")
        builder.row(but2, but1, width=2)

        try:
            current_time = datetime.now()
            time_difference = current_time - obj_job.last_execution[user_id]

            if job_name == self.set_job_name and status_job == "processing" and not take_award:
                if time_difference.total_seconds() < 14400:
                    remaining_time_seconds = 14400 - time_difference.total_seconds()
                    remaining_hours = int(remaining_time_seconds // 3600)
                    remaining_minutes = int((remaining_time_seconds % 3600) // 60)
                    await query.answer(
                        f"Награда будет доступна через {remaining_hours} часов {remaining_minutes} минут")
                    return

                await bot.edit_message_reply_markup(message_id=query.message.message_id,
                                                    chat_id=query.message.chat.id,
                                                    reply_markup=builder.as_markup())
                result = random_choice_with_probabilities(probabilities)
                if result != "loss_30":
                    prize = 1800
                    balance = await TakeInfo.take_balance(query)
                    new_balance = balance + prize
                    await query.answer(f"Вы успешно забрали награду за работу {self.set_job_name} {prize}{emoji}")
                    await TakeInfo.update_balance_and_add_to_daily(user_id, new_balance)
                    await update_cache(user_id, new_balance)
                    await TakeInfo.create_job(user_id, None, "finished", True)
                else:
                    await query.answer(f"Вы потерпели неудачу в работе {self.set_job_name}")
                    await TakeInfo.create_job(user_id, None, "finished", True)
        except Exception as err:
            await logger.error(f"exitline.py - Произошла ошибка {err}")

    async def start_exit_line(self, query):
        user_id = query.from_user.id
        job_set_name = self.set_job_name
        job_name, status_job, take_award = await TakeInfo.take_status_job(user_id)

        if job_name is None and status_job == "finished":
            current_time = datetime.now()
            obj_job.last_execution[user_id] = current_time
            await TakeInfo.create_job(user_id, job_set_name, "processing", False)
            await query.answer(f"Вы успешно начали работу - {job_set_name}")
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_exit_line")
            but2 = InlineKeyboardButton(text="⬅️ Назад", callback_data="back_from_jobs_all")
            builder.row(but2, but1, width=2)
            await bot.edit_message_reply_markup(message_id=query.message.message_id,
                                                chat_id=query.message.chat.id,
                                                reply_markup=builder.as_markup())
        else:
            await query.answer("Похоже вы уже заняты другой работой")


job_methods_exit_line = ExitLine("Exit Line")


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == "exit_from_line_menu")
    async def exit_line(query: CallbackQuery):
        user_id = query.from_user.id
        try:
            emoji = await TakeInfo.take_hidden_new_value(query)
            if emoji is None:
                emoji = "💎"
            builder = InlineKeyboardBuilder()
            job_name, status_job, take_award = await TakeInfo.take_status_job(user_id)
            if status_job == "processing" and job_name == "Exit Line":
                but1 = InlineKeyboardButton(text="Получить ✔️", callback_data="take_award_from_exit_line")
            else:
                but1 = InlineKeyboardButton(text="Начать ✔️", callback_data="start_exit_line")
            but2 = InlineKeyboardButton(text="⬅ Назад", callback_data="back_from_jobs_all")
            builder.row(but2, but1, width=2)
            photo = FSInputFile(photo_path["exitline"])
            await bot.delete_message(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id)
            await bot.send_photo(chat_id=query.message.chat.id,
                                 photo=photo,
                                 caption=f"Вы попали на работу по *Выходу на Лайн* \n Риск этой работы составляет *30%*"
                                         f"\n За каждый час вы получаете +450 {emoji} \n Время работы - 4 часов \n "
                                         f"Желаем вам удачи",
                                 parse_mode=ParseMode.MARKDOWN,
                                 reply_markup=builder.as_markup())
        except Exception as err:
            await logger.error(f"exitline.py - Ошибка в сообщении {err}")

    @dp.callback_query(lambda query: query.data == "start_exit_line")
    async def start_farms_jungle(query: CallbackQuery):
        await job_methods_exit_line.start_exit_line(query)

    @dp.callback_query(lambda query: query.data == "take_award_from_exit_line")
    async def take_award_from_jungle_job(query: CallbackQuery):
        await job_methods_exit_line.take_award_from_exit_line(query)
