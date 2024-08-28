from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    gift_type = State()
    name = State()
    phone_number = State()
    date_of_birth = State()
    address = State()
    
