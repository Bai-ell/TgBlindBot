from responses.apiformation import get_button_text, get_botword_text

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)





async def main_keyboard():
    area_information = await get_button_text(2)  # Получаем текст кнопки с id=2
    connection = await get_button_text(3)
    give = await get_button_text(4)
    menu_choice = await get_button_text(5)
    language = await get_botword_text(botword_id=16)
    
    # Создаем клавиатуру
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=area_information),
                KeyboardButton(text=connection)
            ],
            [
                KeyboardButton(text=give),
                KeyboardButton(text=language)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder= menu_choice,
    )
    return main

async def main():
    keyboard = await main_keyboard()
    
    
rmk = ReplyKeyboardRemove()