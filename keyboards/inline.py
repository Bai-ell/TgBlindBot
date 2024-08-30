from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from idhandlers.idclass import MyCallbackData 
from responses.apiformation import get_button_text, get_botword_text, get_contacts_data, get_links_data, get_gift_options,fetch_mta_data_from_api
import re





async def inlinecontactsocial(user_id):
    builder_contacts = InlineKeyboardBuilder()
    builder_contacts.button(
        text=await get_botword_text(pkwords='Contacts', user_id=user_id),  
        callback_data=MyCallbackData(action='contact', value=1).pack()
    )
    builder_contacts.button(
        text=await get_botword_text(pkwords='Links', user_id=user_id),  
        callback_data=MyCallbackData(action='socials', value=2).pack()
    )
    return builder_contacts.as_markup()





async def area_information(user_id):

    buttons_data = [
        (await get_botword_text(pkwords='Mtb',user_id=user_id), 'mtb'),
        (await get_botword_text(pkwords='Med',user_id=user_id), 'med'),
        (await get_botword_text(pkwords='OOU',user_id=user_id), 'oou')
    ]
    builder_area = InlineKeyboardBuilder()
    for text, action in buttons_data:
        builder_area.button(
            text=text,
            callback_data=MyCallbackData(action=action, value=1).pack()
        )
    return builder_area.as_markup()








async def contacts(user_id):
    contacts = await get_contacts_data(user_id=user_id)
    messages = []
    for contact in contacts:
        message = (
            f"<b>{contact['name']}:</b> {contact['link']}\n"
        )
        messages.append(message)
    full_message = "\n".join(messages)
    return full_message







async def links(user_id):
    links = await get_links_data(user_id=user_id)
    builder = InlineKeyboardBuilder()
    max_buttons_per_row = 2  
    for i in range(0, len(links), max_buttons_per_row):
        row_links = links[i:i + max_buttons_per_row]
        buttons = [
            InlineKeyboardButton(text=link['name'], url=link['link'])
            for link in row_links
        ]
        builder.row(*buttons)
    back_button = InlineKeyboardButton(
        text=await get_button_text(pkname='Back', user_id=user_id),
        callback_data=MyCallbackData(action='go_back', value=1).pack()
    )
    builder.add(back_button)
    markup = builder.as_markup()
    return markup







async def create_short_mta_keyboard(user_id) -> InlineKeyboardMarkup:
    mta_list = await fetch_mta_data_from_api()
    builder = InlineKeyboardBuilder()

    # Регулярное выражение для поиска числа после знака №
    number_pattern = re.compile(r'№\s*(\d{1,2})')

    for mta in mta_list:
        # Поиск числа после знака №
        match = number_pattern.search(mta['string_ru'])
        if match:
            mta_id = int(match.group(1))
            builder.row(
                InlineKeyboardButton(
                    text=f"{await get_botword_text(pkwords='Mtb', user_id=user_id)} {mta_id}",
                    callback_data=MyCallbackData(action=f"mta_{mta_id}", value=1).pack()
                )
            )
    return builder.as_markup()






async def mtbinlinehelper(user_id):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=await get_button_text(pkname='Menu', user_id=user_id),
            callback_data=MyCallbackData(action="menu_choice", value=1).pack()
        ),
        InlineKeyboardButton(
            text=await get_button_text(pkname='Back', user_id=user_id),
            callback_data=MyCallbackData(action="back", value=1).pack()
        )
    )
    return builder.as_markup()
    
    
    



async def gift_inline(user_id):
    
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text=await get_botword_text(pkwords='StartQuestionnaire', user_id=user_id),
            callback_data=MyCallbackData(action="questionnaire", value=1).pack()
        )
    )
    return builder.as_markup()


    




async def create_gift_keyboard(user_id):
    gift_options = await get_gift_options(user_id=user_id)  
    builder = InlineKeyboardBuilder()
    max_buttons_per_row = 1 
    for i in range(0, len(gift_options), max_buttons_per_row):
        row_gifts = gift_options[i:i + max_buttons_per_row]
        try:

            buttons = [
                InlineKeyboardButton(
                        text=gift['gift_type_ru'],
                        
                        callback_data=f"gift:{gift['id']}" 
                )
                for gift in row_gifts
            ]
        except KeyError:
            buttons = [
                InlineKeyboardButton(
                        text=gift['gift_type_kg'],
                        
                        callback_data=f"gift:{gift['id']}" 
                )
                for gift in row_gifts
            ]
        builder.row(*buttons)
    markup = builder.as_markup()
    return markup