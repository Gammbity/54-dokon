from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

password_recovery = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Password recovery", callback_data="password_recovery")
    ]
])

contact_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Kontakt yuborish", request_contact=True)
    ]
], resize_keyboard=True, one_time_keyboard=True)