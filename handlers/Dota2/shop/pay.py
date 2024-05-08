from aiogram.enums import ContentType
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogramproject.base.TakeInfoBase import TakeInfo, update_cache
from aiogramproject.main import bot
from aiogram import types, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'Shop')
    async def menu_for_orders(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text=f"10.000{emoji}", callback_data="10_000Value")
        but2 = types.InlineKeyboardButton(text=f"30.000{emoji}", callback_data="30_000Value")
        but3 = types.InlineKeyboardButton(text=f"50.000{emoji}", callback_data="50_000Value")
        but4 = types.InlineKeyboardButton(text=f"100.000{emoji}", callback_data="100_000Value")
        but5 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="Dota2")
        builder.row(but1, but2, but3, but4, but5, width=2)
        photo_path = r"C:\Users\xzxbtl\PycharmProjects\pythonfortests\aiogramproject\handlers\Dota2\shop\media\fortg" \
                     r".jpg"
        photo = FSInputFile(photo_path)
        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        mess = await bot.send_photo(photo=photo,
                                    caption="Здравствуйте, вы попали в магазин Валют \n "
                                            "Выберите интересный вам товар из предложенных",
                                    chat_id=query.message.chat.id,
                                    reply_markup=builder.as_markup())
        dp['menu_message'] = mess

    @dp.callback_query(lambda query: query.data == '10_000Value')
    async def order_10_000(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="Купить 💸", pay=True)
        but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="BackToShopMenu")
        builder.row(but1, but2, width=1)
        currency_amount = 25000
        payload = f"{currency_amount}_Value"
        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        await bot.send_invoice(
            chat_id=query.message.chat.id,
            title=f"Валюта приложения {emoji}",
            description="Валюта внутри бота",
            payload=payload,
            provider_token="381764678:TEST:81046",
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'{currency_amount} {emoji}',
                    amount=10000
                ),
            ],
            max_tip_amount=400000,
            suggested_tip_amounts=[50000, 100000, 150000, 200000],
            start_parameter='nztcoder',
            provider_data=None,
            photo_url="https://sun9-62.userapi.com/impg/XYKd1Rdp0OTPRU2ovuaGMYzc67wDXJMRf71gaw/l14fPuKklRA.jpg?size"
                      "=750x750&quality=95&sign=57c63025b3a0fc856b69ccda094d3c7c&type=album",
            photo_size=100,
            photo_width=800,
            photo_height=500,
            need_name=True,
            need_email=True,
            need_phone_number=False,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=True,
            is_flexible=False,
            disable_notification=False,
            protect_content=True,
            reply_to_message_id=None,
            allow_sending_without_reply=True,
            reply_markup=builder.as_markup(),
            request_timeout=15
        )

    @dp.callback_query(lambda query: query.data == '30_000Value')
    async def order_30_000(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="Купить 💸", pay=True)
        but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="BackToShopMenu")
        builder.row(but1, but2, width=1)
        currency_amount = 25000
        payload = f"{currency_amount}_Value"
        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        await bot.send_invoice(
            chat_id=query.message.chat.id,
            title=f"Валюта приложения {emoji}",
            description="Валюта внутри бота",
            payload=payload,
            provider_token="381764678:TEST:81046",
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'{currency_amount} {emoji}',
                    amount=25000
                ),
            ],
            max_tip_amount=400000,
            suggested_tip_amounts=[50000, 100000, 150000, 200000],
            start_parameter='nztcoder',
            provider_data=None,
            photo_url="https://sun9-62.userapi.com/impg/XYKd1Rdp0OTPRU2ovuaGMYzc67wDXJMRf71gaw/l14fPuKklRA.jpg?size"
                      "=750x750&quality=95&sign=57c63025b3a0fc856b69ccda094d3c7c&type=album",
            photo_size=100,
            photo_width=800,
            photo_height=500,
            need_name=True,
            need_email=True,
            need_phone_number=False,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=True,
            is_flexible=False,
            disable_notification=False,
            protect_content=True,
            reply_to_message_id=None,
            allow_sending_without_reply=True,
            reply_markup=builder.as_markup(),
            request_timeout=15
        )

    @dp.callback_query(lambda query: query.data == '50_000Value')
    async def order_50_000(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="Купить 💸", pay=True)
        but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="BackToShopMenu")
        builder.row(but1, but2, width=1)
        currency_amount = 50000
        payload = f"{currency_amount}_Value"
        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        await bot.send_invoice(
            chat_id=query.message.chat.id,
            title=f"Валюта приложения {emoji}",
            description="Валюта внутри бота",
            payload=payload,
            provider_token="381764678:TEST:81046",
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'{currency_amount} {emoji}',
                    amount=40000
                ),
            ],
            max_tip_amount=400000,
            suggested_tip_amounts=[50000, 100000, 150000, 200000],
            start_parameter='nztcoder',
            provider_data=None,
            photo_url="https://sun9-62.userapi.com/impg/XYKd1Rdp0OTPRU2ovuaGMYzc67wDXJMRf71gaw/l14fPuKklRA.jpg?size"
                      "=750x750&quality=95&sign=57c63025b3a0fc856b69ccda094d3c7c&type=album",
            photo_size=100,
            photo_width=800,
            photo_height=500,
            need_name=True,
            need_email=True,
            need_phone_number=False,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=True,
            is_flexible=False,
            disable_notification=False,
            protect_content=True,
            reply_to_message_id=None,
            allow_sending_without_reply=True,
            reply_markup=builder.as_markup(),
            request_timeout=15
        )

    @dp.callback_query(lambda query: query.data == '100_000Value')
    async def order_100_000(query: CallbackQuery):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        builder = InlineKeyboardBuilder()
        but1 = types.InlineKeyboardButton(text="Купить 💸", pay=True)
        but2 = types.InlineKeyboardButton(text="⬅ Назад", callback_data="BackToShopMenu")
        builder.row(but1, but2, width=1)
        currency_amount = 100000
        payload = f"{currency_amount}_Value"
        await bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        await bot.send_invoice(
            chat_id=query.message.chat.id,
            title=f"Валюта приложения {emoji}",
            description="Валюта внутри бота",
            payload=payload,
            provider_token="381764678:TEST:81046",
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'{currency_amount} {emoji}',
                    amount=70000
                ),
            ],
            max_tip_amount=400000,
            suggested_tip_amounts=[50000, 100000, 150000, 200000],
            start_parameter='nztcoder',
            provider_data=None,
            photo_url="https://sun9-62.userapi.com/impg/XYKd1Rdp0OTPRU2ovuaGMYzc67wDXJMRf71gaw/l14fPuKklRA.jpg?size"
                      "=750x750&quality=95&sign=57c63025b3a0fc856b69ccda094d3c7c&type=album",
            photo_size=100,
            photo_width=800,
            photo_height=500,
            need_name=True,
            need_email=True,
            need_phone_number=False,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=True,
            is_flexible=False,
            disable_notification=False,
            protect_content=True,
            reply_to_message_id=None,
            allow_sending_without_reply=True,
            reply_markup=builder.as_markup(),
            request_timeout=15
        )

    @dp.callback_query(lambda query: query.data == 'BackToShopMenu')
    async def BackToShopMenuButton(query: CallbackQuery):
        await menu_for_orders(query)

    @dp.pre_checkout_query()
    async def pre_check_query(pre_checkout_query: PreCheckoutQuery):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    async def success_payment(query: Message):
        emoji = await TakeInfo.take_hidden_new_value(query)
        if emoji is None:
            emoji = "💎"
        item_description = query.successful_payment.invoice_payload
        currency_amount = int(item_description.split('_')[0])
        user_id = query.from_user.id
        status, balance, username, confirmed = await TakeInfo.take_all_info_about_user(user_id)
        new_balance = balance + currency_amount
        await TakeInfo.update_balance(user_id, new_balance)
        await update_cache(user_id, new_balance)
        await query.answer(f"Начислена награда за покупку: {currency_amount} {emoji}")
