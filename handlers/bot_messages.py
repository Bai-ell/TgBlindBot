from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import reply, inline
from keyboards.reply import main_keyboard
from responses.apiformation import get_button_text, get_botword_text, change_language
from keyboards.inline import inlinecontactsocial, area_information, gift_inline
import aioredis





router = Router()



@router.message(F.text.lower().in_(["хай", "хелоу", "привет", "салам", 'hello', 'how are you?', 'salam', 'кандай','Кандай', 'hi']))
async def greetings(message: Message):
    response_text = await get_botword_text(pkwords='Greetings', user_id=message.from_user.id)  
    await message.reply(response_text)




@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    

    if msg == (await get_button_text(pkname='Connect', user_id=message.from_user.id)).lower():
        await message.answer(await get_button_text(pkname='Connect', user_id=message.from_user.id), reply_markup=await inlinecontactsocial(user_id=message.from_user.id))


    elif msg == (await get_button_text(pkname='AreaInfo', user_id=message.from_user.id)).lower():
        await message.answer(f'<b>{await get_button_text(pkname="AreaInfo", user_id=message.from_user.id)}:\n{await get_botword_text(pkwords="InfoOctoberArea",user_id=message.from_user.id)}</b>', parse_mode= 'HTML',reply_markup=await area_information(user_id=message.from_user.id))


    elif msg == (await get_button_text(pkname='Gift', user_id=message.from_user.id)).lower():
        await message.answer(await get_botword_text(pkwords='Questionnaire', user_id=message.from_user.id), reply_markup=await gift_inline(user_id=message.from_user.id))


    elif msg == await get_button_text(pkname='ChoiceLang', user_id=message.from_user.id):
        new_lang = change_language(message.from_user.id)
        await message.answer(await get_botword_text(pkwords='ChangeLang', user_id=message.from_user.id), reply_markup=await main_keyboard(user_id=message.from_user.id))


    elif msg == (await get_button_text(pkname='Back', user_id=message.from_user.id)).lower():
        await message.answer(await get_botword_text(pkwords='GoToMenu', user_id=message.from_user.id), reply_markup=await main_keyboard(user_id=message.from_user.id))







