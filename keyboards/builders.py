from aiogram.utils.keyboard import ReplyKeyboardBuilder

user_languages = {}

async def profile(text):
    builder = ReplyKeyboardBuilder()
    
    if isinstance(text, str):
        text = [text]
        
    [builder.button(text=txt) for txt in text]  
    return builder.as_markup(resize_keyboard = True, une_time_keyboard = True)

