from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button, style='primary', remove_keyboard=True
                ))
    if kwargs:
        for button, text in kwargs.items():
            if text.startswith('http://') or text.startswith('https://') or text.startswith('t.me/'):
                buttons.append(InlineKeyboardButton(
                    text=LEXICON[button] if button in LEXICON else button,
                    url=text,
                    style='primary', remove_keyboard=True))
            else:
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button, style='primary', remove_keyboard=True))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(remove_keyboard=True)
