from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from idhandlers.idclass import MyCallbackData 
from responses.apiformation import get_button_text, get_botword_text, get_contacts_data, get_links_data, get_gift_options






async def inlinecontactsocial():
    contacts = await get_botword_text(botword_id=4)
    socials = await get_botword_text(botword_id=5)
    builder_contacts = InlineKeyboardBuilder()
    builder_contacts.button(
        text=contacts,  # Здесь уже должен быть текст, а не корутина
        callback_data=MyCallbackData(action='contact', value=1).pack()
    )
    builder_contacts.button(
        text=socials,  # Здесь тоже должен быть текст
        callback_data=MyCallbackData(action='socials', value=2).pack()
    )
    return builder_contacts.as_markup()


async def area_information():
    mtb = await get_botword_text(botword_id=12)
    med = await get_botword_text(botword_id=14)
    oou = await get_botword_text(botword_id=13)
    buttons_data = [
        (mtb, 'mtb'),
        (med, 'med'),
        (oou, 'oou')
    ]
    builder_area = InlineKeyboardBuilder()
    for text, action in buttons_data:
        builder_area.button(
            text=text,
            callback_data=MyCallbackData(action=action, value=1).pack()
        )
    return builder_area.as_markup()





async def contacts():
    contacts = await get_contacts_data()
    messages = []
    for contact in contacts:
        message = (
            f"<b>{contact['name']}:</b> {contact['link']}\n"
        )
        messages.append(message)
    full_message = "\n".join(messages)
    return full_message




async def links():
    links = await get_links_data()
    builder = InlineKeyboardBuilder()
    max_buttons_per_row = 2  
    for i in range(0, len(links), max_buttons_per_row):
        row_links = links[i:i + max_buttons_per_row]
        buttons = [
            InlineKeyboardButton(text=link['name'], url=link['link'])
            for link in row_links
        ]
        builder.row(*buttons)
    go_back = await get_button_text(button_id=6)
    back_button = InlineKeyboardButton(
        text=go_back,
        callback_data=MyCallbackData(action='go_back', value=1).pack()
    )
    builder.add(back_button)
    markup = builder.as_markup()
    return markup



async def mtbinline():
    # Получение текста для кнопок
    mtb6 = await get_botword_text(botword_id=8)
    mtb7 = await get_botword_text(botword_id=9)
    mtb8 = await get_botword_text(botword_id=10)
    mtb9 = await get_botword_text(botword_id=11)
    mtb10 = await get_botword_text(botword_id=17)
    mtb611 = await get_botword_text(botword_id=18)

    buttons_data = [
        (mtb6, 'mtb6'),
        (mtb7, 'mtb7'),
        (mtb8, 'mtb8'),
        (mtb9, 'mtb9'),
        (mtb10, 'mtb10'),
        (mtb611, 'mtb11')
    ]
    builder = InlineKeyboardBuilder()
    max_buttons_per_row = 1
    for i in range(0, len(buttons_data), max_buttons_per_row):
        row_buttons = buttons_data[i:i + max_buttons_per_row]
        buttons = [
            InlineKeyboardButton(
                text=text,
                callback_data=MyCallbackData(action=action, value=1).pack()
            )
            for text, action in row_buttons
        ]
        builder.row(*buttons)
    return builder.as_markup()


async def mtbinlinehelper():
    menu_choice = await get_button_text(button_id=6)
    back = await get_button_text(button_id=7)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=menu_choice,
            callback_data=MyCallbackData(action="menu_choice", value=1).pack()
        ),
        InlineKeyboardButton(
            text=back,
            callback_data=MyCallbackData(action="back", value=1).pack()
        )
    )
    return builder.as_markup()
    
    
    
async def give_inline():
    
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text="Начать анкету",
            callback_data=MyCallbackData(action="questionnaire", value=1).pack()
        )
    )
    return builder.as_markup()


async def create_gift_keyboard():
    gift_options = await get_gift_options()  
    builder = InlineKeyboardBuilder()
    max_buttons_per_row = 1 
    for i in range(0, len(gift_options), max_buttons_per_row):
        row_gifts = gift_options[i:i + max_buttons_per_row]
        buttons = [
            InlineKeyboardButton(
                text=gift['gift_type_ru'],
                callback_data=f"gift:{gift['id']}" 
            )
            for gift in row_gifts
        ]
        builder.row(*buttons)
    markup = builder.as_markup()
    return markup