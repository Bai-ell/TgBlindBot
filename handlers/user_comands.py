from aiogram import Router,types
from aiogram.filters import CommandStart
from keyboards.reply import main_keyboard
from responses.apiformation import get_botword_text



router = Router()



@router.message(CommandStart())
async def start(message: types.Message):
    response_text = await get_botword_text(pkwords='Greetings',user_id=message.from_user.id)  
    keyboard = await main_keyboard(user_id=message.from_user.id)
    await message.reply(response_text, reply_markup=keyboard)



