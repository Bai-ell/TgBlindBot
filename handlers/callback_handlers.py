from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from keyboards.inline import contacts,  links, mtbinline, mtbinlinehelper
from idhandlers.idclass import MyCallbackData 
from keyboards.reply import main_keyboard  
from responses.apiformation import get_botword_text, get_institution_data, get_mta_data



router = Router()



@router.callback_query(MyCallbackData.filter(F.action.in_({'contact', 'socials', 'go_back'})))
async def handle_callback_query(query: CallbackQuery, callback_data: MyCallbackData):
    
    keyboard = await main_keyboard() 
    contact_info = await contacts()  
    links_keyboard = await links()
    
    liks_lang = await get_botword_text(botword_id=5)
    back_menu = await get_botword_text(botword_id=15)
    
    if callback_data.action == 'contact':
        await query.message.answer(contact_info, parse_mode='HTML', reply_markup=keyboard)
    elif callback_data.action == 'socials':
        await query.message.answer(liks_lang, reply_markup=links_keyboard)
    elif callback_data.action =='go_back':
        await query.message.answer(back_menu, reply_markup=keyboard)





@router.callback_query(MyCallbackData.filter(F.action.in_({'numbers', 'home'})))
async def handle_query_callback_second(query: CallbackQuery, callback_data: MyCallbackData):
    keyboard = await main_keyboard() 
    if callback_data.action == 'numbers':
        await query.message.answer('wow numbers')
    elif callback_data.action == 'home':
        await query.message.answer('you at home', reply_markup=keyboard)


@router.callback_query(MyCallbackData.filter(F.action.in_({'mtb', 'med', 'oou'})))
async def handle_area_callback_query(query: CallbackQuery, callback_data: MyCallbackData):
    keyboard = await main_keyboard() 
    mtbinlinereply = await mtbinline()
    
    med = await get_institution_data(institution_id=2)
    oou = await get_institution_data(institution_id=1)
    mtb_choice = await get_botword_text(botword_id=19)
    
    if callback_data.action == 'mtb':
        await query.message.answer(mtb_choice, reply_markup=mtbinlinereply)
    elif callback_data.action == 'med':
        await query.message.answer(f'<b>{med}</b>', parse_mode='HTML',reply_markup=keyboard)
    elif callback_data.action == 'oou':
        await query.message.answer(f'<b>{oou}</b>', parse_mode='HTML',reply_markup=keyboard)









@router.callback_query(MyCallbackData.filter(F.action.in_(["mtb6", "mtb7", "mtb8", "mtb9", "mtb10", "mtb11"])))
async def mtb_inline_callback_handler(query: CallbackQuery, callback_data: MyCallbackData):
    action = callback_data.action
    
    mtbhelper = await mtbinlinehelper()
    
    mtb6 = await get_mta_data(mta_id=1)
    mtb7 = await get_mta_data(mta_id=2)
    mtb8 = await get_mta_data(mta_id=3)
    mtb9 = await get_mta_data(mta_id=4)
    mtb10 = await get_mta_data(mta_id=5)
    mtb11 = await get_mta_data(mta_id=6)

    if action == "mtb6":
        await query.message.answer(f'<b>{mtb6}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    elif action == "mtb7":
        await query.message.answer(f'<b>{mtb7}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    elif action == "mtb8":
        await query.message.answer(f'<b>{mtb8}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    elif action == "mtb9":
        await query.message.answer(f'<b>{mtb9}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    elif action == "mtb10":
        await query.message.answer(f'<b>{mtb10}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    elif action == "mtb11":
        await query.message.answer(f'<b>{mtb11}</b>', reply_markup=mtbhelper, parse_mode='HTML')
    await query.answer()
    
    
    
    
@router.callback_query(MyCallbackData.filter(F.action.in_(["menu_choice", "back"])))
async def handle_menu_and_back_buttons(query: CallbackQuery, callback_data: MyCallbackData):
    action = callback_data.action
    
    menu_back = await get_botword_text(botword_id=15)
    keyboard = await main_keyboard() 
    mtbhelp = await mtbinline()
    
    if action == "menu_choice":
        await query.message.answer(menu_back, reply_markup=keyboard)
    elif action == "back":
        await query.message.answer("You pressed the back button.", reply_markup=mtbhelp)

    await query.answer()
    
    
    
    
    
