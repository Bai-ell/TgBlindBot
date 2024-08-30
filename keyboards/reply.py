from responses.apiformation import get_button_text, get_botword_text

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)





async def main_keyboard(user_id): 
    
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=await get_button_text(pkname='AreaInfo', user_id=user_id)),
                KeyboardButton(text=await get_button_text(pkname='Connect', user_id=user_id))
            ],
            [
                KeyboardButton(text=await get_button_text(pkname='Gift', user_id=user_id)),
                KeyboardButton(text=await get_button_text(pkname='ChoiceLang', user_id=user_id))
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder= await get_button_text(pkname='ChoiceMenu', user_id=user_id),
    )
    return main

async def main():
    keyboard = await main_keyboard()
    
    
rmk = ReplyKeyboardRemove()