from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards import reply, inline
from keyboards.reply import main_keyboard
from responses.apiformation import get_button_text, get_botword_text
from keyboards.inline import inlinecontactsocial, area_information, gift_inline



router = Router()



@router.message(F.text.lower().in_(["хай", "хелоу", "привет", "салам", 'hello', 'how are you?', 'salam', 'кандай','Кандай', 'hi']))
async def greetings(message: Message):
    response_text = await get_botword_text(pkwords='Greetings')  
    await message.reply(response_text)




@router.message()
async def echo(message: Message):
    msg = message.text.lower()
    

    if msg == (await get_button_text(pkname='Connect')).lower():
        await message.answer(await get_botword_text(pkwords='Contacts'), reply_markup=await inlinecontactsocial())


    elif msg == (await get_button_text(pkname='AreaInfo')).lower():
        await message.answer(f'<b>{await get_button_text(pkname="AreaInfo")}:\n{await get_botword_text(pkwords="InfoOctoberArea")}</b>', parse_mode= 'HTML',reply_markup=await area_information())


    elif msg == (await get_button_text(pkname='Gift')).lower():
        await message.answer(await get_botword_text(pkwords='Questionnaire'), reply_markup=await gift_inline())


    elif msg == await get_button_text(pkname='ChoiceLang'):
        await message.answer(await get_botword_text(pkwords='ChangeLang'), reply_markup=await main_keyboard())


    elif msg == (await get_button_text(pkname='Back')).lower():
        await message.answer(await get_botword_text(pkwords='GoToMenu'), reply_markup=await main_keyboard())







