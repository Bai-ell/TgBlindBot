import aiohttp


QUESTIONNAIRE_CREATE = 'http://127.0.0.1:8000/questionnaire/create/'
INSTITUTIONS = 'http://127.0.0.1:8000/institutions/institutions/'
SHORT_MTA_URL = 'http://127.0.0.1:8000/institutions/shortmta/'
GIFT_URL = 'http://127.0.0.1:8000/questionnaire/gifts'
BOTWORDS = 'http://127.0.0.1:8000/botwords/botwords/'
BUTTONS  = 'http://127.0.0.1:8000/buttons/buttons/'
CONTACTS = 'http://127.0.0.1:8000/links/contacts/'
MTA = 'http://127.0.0.1:8000/institutions/mta/'
LINKS ='http://127.0.0.1:8000/links/links/'



async def get_botword_text(pkwords):
    async with aiohttp.ClientSession() as session:
        async with session.get(BOTWORDS) as response:
            response.raise_for_status()
            botword_data = await response.json()
    
    specific_botword = next((item for item in botword_data if item["pkwords"] == pkwords), None)
    return specific_botword['botwords_ru'] if specific_botword else None


async def get_short_mta_list(language='ru'):
    async with aiohttp.ClientSession() as session:
        async with session.get(SHORT_MTA_URL) as response:
            response.raise_for_status()
            short_mta_data = await response.json()
    
    # Фильтрация данных по языку
    return [
        {
            "id": item["id"],
            "string": item.get(f'string_{language}')
        }
        for item in short_mta_data
    ]


async def get_button_text(pkname):
    async with aiohttp.ClientSession() as session:
        async with session.get(BUTTONS) as response:
            response.raise_for_status()
            button_data = await response.json()
    
    specific_button = next((item for item in button_data if item["pkname"] == pkname), None)
    return specific_button["button_ru"] if specific_button else None


async def get_contacts_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(CONTACTS) as response:
            response.raise_for_status()
            data = await response.json()
            contacts = []
            for contact in data:
                name = contact['ru_name']
                contacts.append({
                    'name': name,
                    'link': contact['link']
                })
            return contacts


async def get_links_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(LINKS) as response:
            response.raise_for_status()
            data = await response.json()
            links = []
            for link in data:
                name = link['ru_name']
                links.append({
                    'name': name,
                    'link': link['link']
                })
            return links



async def send_questionnaire_data(name, phone_number, date_of_birth, address):
    payload = {
        'name': name,
        'phone_number': phone_number,
        'date_of_birth': date_of_birth,  # формат YYYY-MM-DD
        'address': address
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(QUESTIONNAIRE_CREATE, json=payload) as response:
            response.raise_for_status()



async def get_institution_data(institution_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(INSTITUTIONS) as response:
            response.raise_for_status()
            institution_data = await response.json()
    institution = next((item for item in institution_data if item["id"] == institution_id), None)
    return institution.get('string_ru')


async def get_mta_data(mta_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(MTA) as response:
            response.raise_for_status()
            institution_data = await response.json()
    institution = next((item for item in institution_data if item["id"] == mta_id), None)
    return institution.get('string_ru')




async def get_gift_options():
    async with aiohttp.ClientSession() as session:
        async with session.get(GIFT_URL) as response:
            response.raise_for_status()
            gift_data = await response.json()


    gift_options = []
    for item in gift_data:
        gift_options.append({
            'id': item['id'],
            'gift_type_ru': item['gift_type_ru']
        })
    return gift_options