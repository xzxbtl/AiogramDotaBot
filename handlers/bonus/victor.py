from aiogram import Dispatcher, types
from aiogramproject.main import bot
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from collections import defaultdict
from aiogramproject.handlers.bonus.bonus import BonusMenu
from datetime import datetime
import random
from aiogramproject.logs import logger
from aiogramproject.handlers.bonus.quetionslist import Questions

questions = Questions.questions

win_file_path = r"C:\Users\xzxbtl\PycharmProjects\pythonfortests\aiogramproject\handlers\bonus\media\win.jpg"

random.shuffle(questions)


class ShowKeysValues:
    def __init__(self, *args):
        self.dicts = args

    @staticmethod
    def show_question_keys(dict_to_show: dict):
        key = next(iter(dict_to_show.keys()))
        return key

    def show_all_keys(self):
        for d in self.dicts:
            key = next(iter(d.keys()))
            return key


class Quiz:
    def __init__(self):
        self.last_execution = {}
        self.current_question_index = {}


obj_quiz = Quiz()

user_attempts = defaultdict(int)
user_winnings = {}
MAX_ATTEMPTS = 3


def register_handlers(dp: Dispatcher):
    @dp.callback_query(lambda query: query.data == 'Victorin')
    async def handle_clicker(query: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        but_first = types.InlineKeyboardButton(text="✅ Учавствовать",
                                               callback_data="Accept_Victor")
        but_second = types.InlineKeyboardButton(text='<< Вернуться',
                                                callback_data='Back_awards_menu')
        builder.row(but_first, but_second, width=1)

        await bot.edit_message_text("<b>Викторина по игре Дота 2</b>",
                                    reply_markup=builder.as_markup(),
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.HTML)

    @dp.callback_query(lambda query: query.data == 'Back_awards_menu')
    async def handle_bonus_menu_callback(query: types.CallbackQuery):
        await query.answer("Вы вернулись в Бонусное меню",
                           show_alert=False)
        try:
            await bot.delete_message(chat_id=query.from_user.id,
                                     message_id=query.message.message_id)
            await BonusMenu.bonus(query)
        except Exception as e:
            logger.info(f"victor.py - Ошибка при удалении сообщения: {e}")

    @dp.callback_query(lambda query: query.data == "Accept_Victor")
    async def handle_victor_menu(query: types.CallbackQuery):
        current_time = datetime.now()
        last_execution_time = obj_quiz.last_execution.get(query.from_user.id, None)

        if last_execution_time is not None:
            time_difference = current_time - last_execution_time
            if time_difference.total_seconds() < 43200:
                remaining_time_seconds = 43200 - time_difference.total_seconds()
                remaining_hours = int(remaining_time_seconds // 3600)
                remaining_minutes = int((remaining_time_seconds % 3600) // 60)
                await query.answer(
                    f"Награда недоступна еще {remaining_hours} часов {remaining_minutes} минут")
                return
        obj_quiz.last_execution[query.from_user.id] = current_time

        builder = InlineKeyboardBuilder()
        but_first = types.InlineKeyboardButton(text="Принять участие ✔️",
                                               callback_data="Accept_victor_dota2")
        but_second = types.InlineKeyboardButton(text="Отмена ❌",
                                                callback_data="Cancel_victor_dota2")
        builder.row(but_first, but_second, width=1)

        image_from_pc = FSInputFile(
            r"C:\Users\xzxbtl\PycharmProjects\pythonfortests\aiogramproject\handlers\bonus\media\main-victor.jpg")
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        await query.message.answer_photo(
            image_from_pc,
            caption=f"Добро пожаловать в викторину по *Dota 2* \n "
                    f"За каждый успешный ответ вы получаете `200` {emoji} \n "
                    f"У вас есть всего 3 попытки на прохождение \n "
                    f"Удачной игры <3",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN
        )
        await bot.delete_message(chat_id=query.from_user.id,
                                 message_id=query.message.message_id)

    @dp.callback_query(lambda query: query.data == "Cancel_victor_dota2")
    async def handle_victor_menu(query: types.CallbackQuery):
        await query.answer("Вы вернулись в Бонусное меню", show_alert=False)
        try:
            await bot.delete_message(chat_id=query.from_user.id,
                                     message_id=query.message.message_id)
            await BonusMenu.bonus(query)
        except Exception as e:
            await logger.info(f"victor.py - Ошибка при удалении сообщения: {e}")

    @dp.callback_query(lambda query: query.data == "Accept_victor_dota2")
    async def handle_question(query: types.CallbackQuery):
        current_user_id = query.from_user.id
        current_index = obj_quiz.current_question_index.get(current_user_id, 0)
        if current_index < len(questions):
            question_data = questions[current_index]

            buttons = [
                types.InlineKeyboardButton(text=question_data["Confirmed_answer"], callback_data="Confirmed_answer")
            ]
            for option in question_data["options"]:
                if option != question_data["Confirmed_answer"]:
                    button = types.InlineKeyboardButton(text=option,
                                                        callback_data=option)
                    buttons.append(button)
            random.shuffle(buttons)

            builder = InlineKeyboardBuilder()
            for button in buttons:
                builder.row(button, width=1)

            image_from_pc = FSInputFile(question_data["image_path"])
            await bot.delete_message(chat_id=query.from_user.id,
                                     message_id=query.message.message_id)
            await query.message.answer_photo(
                image_from_pc,
                caption=question_data["question"],
                reply_markup=builder.as_markup(),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.message.answer("Поздравляю! Вы ответили на все вопросы")

    @dp.callback_query(lambda query: query.data in [option for question in questions for option in question["options"]])
    async def handle_cancel_answered(query: types.CallbackQuery):
        user_id = query.from_user.id
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        user_attempts[user_id] += 1

        if user_attempts[user_id] <= MAX_ATTEMPTS:
            if user_attempts[user_id] == MAX_ATTEMPTS:
                await query.answer(f"Вы проиграли! Ваш текущий выигрыш: {user_winnings.get(user_id, 0)} {emoji}",
                                   show_alert=False)
                balance = await TakeInfo.take_balance(query)
                new_balance = balance + user_winnings.get(user_id, 0)
                await TakeInfo.update_balance(user_id, new_balance)
                await update_cache(user_id, new_balance)
                await bot.delete_message(chat_id=query.from_user.id,
                                         message_id=query.message.message_id)
                await BonusMenu.bonus(query)
            else:
                await query.answer(f"Неверно! Осталось попыток: {MAX_ATTEMPTS - user_attempts[user_id]}",
                                   show_alert=False)
        else:
            await query.answer(f"Извините, вы уже использовали все попытки!",
                               show_alert=False)

    @dp.callback_query(lambda query: query.data == "Confirmed_answer")
    async def handle_correct_answer(query: types.CallbackQuery):
        current_user_id = query.from_user.id
        current_index = obj_quiz.current_question_index.get(current_user_id, 0)

        user_id = query.from_user.id
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"

        if user_id not in user_winnings:
            user_winnings[user_id] = 0

        if query.data == "Confirmed_answer":
            current_index += 1
            obj_quiz.current_question_index[current_user_id] = current_index
            user_winnings[user_id] += 200
            await query.answer(f"Верно, вы получили: 200 {emoji}", show_alert=False)

            if current_index < len(questions):
                await handle_question(query)
            if current_index >= len(questions):
                builder = InlineKeyboardBuilder()
                but = types.InlineKeyboardButton(text="Вернуться ❌", callback_data="Cancel_victor_dota2")
                builder.add(but)
                await bot.delete_message(chat_id=query.from_user.id,
                                         message_id=query.message.message_id)
                image_from_pc = FSInputFile(win_file_path)
                await query.message.answer_photo(
                    image_from_pc,
                    caption=f"Вы успешно *прошли* Викторину \n "
                            f"Ваш выигрыш составил: `{user_winnings.get(user_id, 0)}` {emoji} \n"
                            f"*Спасибо*, что приняли участие",
                    reply_markup=builder.as_markup(),
                    parse_mode=ParseMode.MARKDOWN)
                balance = await TakeInfo.take_balance(query)
                new_balance = balance + user_winnings.get(user_id, 0)
                await TakeInfo.update_balance(user_id, new_balance)
                await update_cache(user_id, new_balance)
