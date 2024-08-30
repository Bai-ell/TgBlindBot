from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from keyboards.inline import contacts,  links, create_short_mta_keyboard, mtbinlinehelper, gift_inline
from idhandlers.idclass import MyCallbackData 
from keyboards.reply import main_keyboard  
from responses.apiformation import get_botword_text, get_institution_data, get_mta_data_by_id



router = Router()



@router.callback_query(MyCallbackData.filter(F.action.in_({'contact', 'socials', 'go_back'})))
async def handle_callback_query(query: CallbackQuery, callback_data: MyCallbackData):

    if callback_data.action == 'contact':
        await query.message.answer(await contacts(user_id=query.from_user.id), parse_mode='HTML', reply_markup=await main_keyboard(user_id=query.from_user.id))
    elif callback_data.action == 'socials':
        await query.message.answer(await get_botword_text(pkwords='Links',user_id=query.from_user.id), reply_markup=await links(user_id=query.from_user.id))
    elif callback_data.action =='go_back':
        await query.message.answer(await get_botword_text(pkwords='GoToMenu',user_id=query.from_user.id), reply_markup=await main_keyboard(user_id=query.from_user.id))







@router.callback_query(MyCallbackData.filter(F.action.in_({'mtb', 'med', 'oou'})))
async def handle_area_callback_query(query: CallbackQuery, callback_data: MyCallbackData):
    
    if callback_data.action == 'mtb':
        await query.message.answer(await get_botword_text(pkwords='Choice', user_id=query.from_user.id), reply_markup=await create_short_mta_keyboard(user_id=query.from_user.id))
    elif callback_data.action == 'med':
        await query.message.answer(f'<b>{await get_institution_data(institution_id=2, user_id=query.from_user.id)}</b>', parse_mode='HTML',reply_markup=await main_keyboard(user_id=query.from_user.id))
    elif callback_data.action == 'oou':
        await query.message.answer(f'<b>{await get_institution_data(institution_id=1,user_id=query.from_user.id)}</b>', parse_mode='HTML',reply_markup=await main_keyboard(user_id=query.from_user.id))


    
    
    
    
@router.callback_query(MyCallbackData.filter(F.action.in_(["menu_choice", "back"])))
async def handle_menu_and_back_buttons(query: CallbackQuery, callback_data: MyCallbackData):
    action = callback_data.action
    
    
    if action == "menu_choice":
        await query.message.answer(await get_botword_text(pkwords='GoToMenu', user_id=query.from_user.id), reply_markup=await main_keyboard(user_id=query.from_user.id) )
    elif action == "back":
        await query.message.answer(await get_botword_text(pkwords='Choice', user_id=query.from_user.id), reply_markup=await create_short_mta_keyboard(user_id=query.from_user.id))

    await query.answer()
    
    
@router.callback_query(MyCallbackData.filter(F.action.startswith("mta_")))
async def mtb_detailed_callback_handler(query: CallbackQuery, callback_data: MyCallbackData):
    mta_id = int(callback_data.action.split("_")[1])
    institution_text = await get_mta_data_by_id(mta_id, user_id=query.from_user.id)

    await query.message.answer(
        f'<b>{institution_text}</b>', 
        reply_markup=await mtbinlinehelper(user_id=query.from_user.id), 
        parse_mode='HTML'
    )
    await query.answer()