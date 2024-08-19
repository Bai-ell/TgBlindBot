from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import reply, inline
from keyboards.reply import main_keyboard
from responses.apiformation import get_button_text, get_botword_text
from keyboards.inline import inlinecontactsocial, area_information, give_inline



router = Router()



@router.message(F.text.lower().in_(["хай", "хелоу", "привет", "салам", 'hello', 'how are you?', 'salam', 'кандай','Кандай', 'hi']))
async def greetings(message: Message):
    response_text = await get_botword_text(botword_id=2)  
    await message.reply(response_text)


@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    

    inline1 = await inlinecontactsocial()
    keyboard = await main_keyboard()
    area_information_markup = await area_information()
    give_inline_murkap = await give_inline()
    
    connection_word = await get_button_text(button_id=3)
    area_word = await get_button_text(button_id=2)  
    give = await get_button_text(button_id=4)
    back = await get_button_text(button_id=6)
    
    choice_lang = await get_botword_text(botword_id=3)
    contacts = await get_botword_text(botword_id=4)
    area_info = await get_botword_text(botword_id=7)
    back_menu = await get_botword_text(botword_id=15)
    language = await get_botword_text(botword_id=16)
    
    

    if msg == connection_word.lower():
        await message.answer(contacts, reply_markup=inline1)
    elif msg == area_word.lower():
        await message.answer(f'<b>{area_word}:\n{area_info}</b>', parse_mode= 'HTML',reply_markup=area_information_markup) 
    elif msg == give.lower():
        await message.answer('aspidjfaoi', reply_markup=give_inline_murkap)
    elif msg == language:
        await message.answer(choice_lang, reply_markup=keyboard)
    elif msg == back.lower():
        await message.answer(back_menu, reply_markup=keyboard)







