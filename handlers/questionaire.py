from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
# from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk
from datetime import datetime
from responses.apiformation import send_questionnaire_data, get_gift_options
from idhandlers.idclass import MyCallbackData, GiftCallbackData
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import logging


router = Router()


    
    
    
    
class Form(StatesGroup):
    name = State()
    phone_number = State()
    date_of_birth = State()
    address = State()





@router.callback_query(F.data.startswith("gift:"))
async def choose_gift(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.name)
    gift_id = callback_query.data.split(':')[1]
    print(gift_id)
    await state.update_data(gift_id=gift_id)
    reply_markup = profile(callback_query.from_user.first_name)
    await callback_query.message.answer(
        "Вы выбрали подарок. Давайте начнем, введите свое имя",
        reply_markup=reply_markup  # Использование ожидания результата
)

@router.message(Form.name)
async def form_name(message: Message, state: FSMContext)-> None:
    await state.set_state(Form.phone_number)
    await state.update_data(name=message.text)
    await message.answer("Теперь введи свой номер телефона")



@router.message(Form.phone_number)
async def form_phone_number(message: Message, state: FSMContext)-> None:
    if message.text.isdigit():
        await state.set_state(Form.date_of_birth)
        await state.update_data(phone_number=message.text)
        await message.answer("Отлично! Теперь введи свою дату рождения в формате YYYY-MM-DD")
    else:
        await message.answer("Пожалуйста, введи корректный номер телефона.")

@router.message(Form.date_of_birth)
async def form_date_of_birth(message: Message, state: FSMContext)-> None:
    try:
        await state.set_state(Form.address)
        datetime.strptime(message.text, '%Y-%m-%d')
        await state.update_data(date_of_birth=message.text)
        await message.answer("Теперь введи свой адрес проживания")
    except ValueError:
        await message.answer("Пожалуйста, введи дату в формате YYYY-MM-DD.")

@router.message(Form.address)
async def form_address(message: Message, state: FSMContext)-> None:
    if not message.text.strip():
        await message.answer("Пожалуйста, введи корректный адрес.")
        return
    

    await state.update_data(address=message.text)
    
    # Получение всех сохраненных данных
    data = await state.get_data()
    name = data.get("name")
    phone_number = data.get("phone_number")
    date_of_birth = data.get("date_of_birth")
    address = data.get("address")
    gift_id = data.get("gift_id")  # Получение ID подарка
    
    # Формирование сообщения с данными анкеты
    message_text = (
        f"Спасибо! Ваша анкета успешно отправлена.\n"
        f"Вы выбрали подарок с ID: {gift_id}.\n"
        f"Имя: {name}\n"
        f"Телефон: {phone_number}\n"
        f"Дата рождения: {date_of_birth}\n"
        f"Адрес: {address}"
    )
    
    # Пример функции для отправки данных анкеты (реализуйте по своему усмотрению)
    saved_data = await send_questionnaire_data(name, phone_number, date_of_birth, address, gift_id)
    
    await state.clear()
    
    if saved_data:
        await message.answer(message_text)
    else:
        await message.answer("Произошла ошибка при отправке анкеты. Пожалуйста, попробуйте еще раз.")
