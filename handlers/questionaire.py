from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk, main_keyboard
from keyboards.inline import create_gift_keyboard
from idhandlers.idclass import MyCallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from responses.apiformation import get_gift_options, send_questionnaire_data, send_data_to_google_sheet, connect_to_google_sheet, get_botword_text, get_button_text




import logging


router = Router()


    



@router.callback_query(MyCallbackData.filter(F.action == "questionnaire"))
async def start_questionnaire(callback: types.CallbackQuery, state: FSMContext):
    keyboard = await create_gift_keyboard()
    await callback.message.answer(await get_botword_text(pkwords='ChoiceGiftQuestionnaire'), reply_markup=keyboard)
    await state.set_state(Form.gift_type)


@router.callback_query(lambda c: c.data.startswith('gift:'))
async def process_gift_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    gift_id = callback.data.split(':')[1]
    
    # Сохраняем выбранный подарок в состоянии
    await state.update_data(gift_id=gift_id)
    await callback.message.answer(await get_botword_text(pkwords='AnswerName'), reply_markup=await profile(callback.from_user.first_name))
    




@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone_number)
    await message.answer(await get_botword_text(pkwords='AnswerPhoneNumber'), reply_markup=rmk)



@router.message(Form.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(Form.date_of_birth)
    await message.answer(await get_botword_text(pkwords='AnswerDateOfBirth'))
    



@router.message(Form.date_of_birth)
async def process_date_of_birth(message: types.Message, state: FSMContext):
    await state.update_data(date_of_birth=message.text)
    await state.set_state(Form.address)
    await message.answer(await get_botword_text(pkwords='AnswerAdress'))



@router.message(Form.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    gift_id = data.get("gift_id")
    gift = next((gift for gift in await get_gift_options() if gift['id'] == int(gift_id)), None)
    try:
        if gift['gift_type_ru']:
            gift_name = gift['gift_type_ru']
    except KeyError:
        gift_name = gift['gift_type_kg']
    name = data.get("name")
    phone_number = data.get("phone_number")
    date_of_birth = data.get("date_of_birth")  
    address = data.get("address")

    await send_questionnaire_data(name, phone_number, date_of_birth, address, gift_name)

    
   
    await message.answer(
        f"{await get_botword_text(pkwords='EndQuestionnaire')}\n"
        f"{await get_botword_text(pkwords='Gift')}: {gift_name}\n"
        f"{await get_botword_text(pkwords='Name')}: {name}\n"
        f"{await get_botword_text(pkwords='Phone')}: {phone_number}\n"
        f"{await get_botword_text(pkwords='BirthDate')}: {date_of_birth}\n"
        f"{await get_botword_text(pkwords='Address')}: {address}"
    )
    await message.answer(
        await get_botword_text(pkwords='SendQuestionnaire'), reply_markup= await main_keyboard()
    )
    
    json_file_path = '/Users/apple/Work/GetLead/OpenSourceWork/TgBlindBot/responses/tgtest.json'
    sheet_name = 'TestTgBot' 
    sheet = await connect_to_google_sheet(json_file_path, sheet_name)
    await send_data_to_google_sheet(sheet, [name, phone_number, date_of_birth, address, gift_name])
    
 
    await state.clear()