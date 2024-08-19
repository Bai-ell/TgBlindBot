from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    phone_number = State()
    date_of_birth  = State()
    address = State()



