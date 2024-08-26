from responses.apiformation import get_button_text, get_botword_text

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)





async def main_keyboard(): 
    
    # Создаем клавиатуру
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=await get_button_text(pkname='AreaInfo')),
                KeyboardButton(text=await get_button_text(pkname='Connect'))
            ],
            [
                KeyboardButton(text=await get_button_text(pkname='Gift')),
                KeyboardButton(text=await get_button_text(pkname='ChoiceLang'))
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder= await get_button_text(pkname='ChoiceMenu'),
    )
    return main

async def main():
    keyboard = await main_keyboard()
    
    
rmk = ReplyKeyboardRemove()