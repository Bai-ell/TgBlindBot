from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import Form  # убедитесь, что состояния Form соответствуют вашему процессу
from keyboards.builders import profile
from keyboards.reply import rmk
from datetime import datetime
from responses.apiformation import send_questionnaire_data

router = Router()



@router.message(Command(""))
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer(
        "Давай начнем, введи свое имя",
        reply_markup=profile(f'{message.from_user.first_name}')
    )


@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone_number)
    await message.answer("Теперь введи свой номер телефона", reply_markup=rmk)


@router.message(Form.phone_number)
async def form_phone_number(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(phone_number=message.text)
        await state.set_state(Form.date_of_birth)
        await message.answer("Отлично! Теперь введи свою дату рождения в формате YYYY-MM-DD", reply_markup=rmk)
    else:
        await message.answer("Пожалуйста, введи корректный номер телефона.")


@router.message(Form.date_of_birth)
async def form_date_of_birth(message: Message, state: FSMContext):
    try:
        # Проверяем формат даты
        datetime.strptime(message.text, '%Y-%m-%d')
        await state.update_data(date_of_birth=message.text)
        await state.set_state(Form.address)
        await message.answer("Теперь введи свой адрес проживания", reply_markup=rmk)
    except ValueError:
        await message.answer("Пожалуйста, введи дату в формате YYYY-MM-DD.")


@router.message(Form.address)
async def form_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    
    # Получаем данные из состояния
    data = await state.get_data()
    name = data.get("name")
    phone_number = data.get("phone_number")
    date_of_birth = data.get("date_of_birth")
    address = data.get("address")
    

    saved_data = await send_questionnaire_data(name, phone_number, date_of_birth, address)
    
    await state.clear()
    
    if saved_data:
        await message.answer("Спасибо! Ваша анкета успешно отправлена.")
    else:
        await message.answer("Произошла ошибка при отправке анкеты. Пожалуйста, попробуйте еще раз.")


@router.message(Form.address)
async def incorrect_form_address(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введи корректный адрес.")
