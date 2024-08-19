from aiogram import Router,types
from aiogram.filters import CommandStart
from keyboards.reply import main_keyboard
from responses.apiformation import get_botword_text



router = Router()



@router.message(CommandStart())
async def start(message: types.Message):
    response_text = await get_botword_text(botword_id=2)  
    keyboard = await main_keyboard()
    await message.reply(response_text, reply_markup=keyboard)

