import aiohttp
import gspread
from google.oauth2.service_account import Credentials
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os,re
from decouple import config
from typing import List, Dict



QUESTIONNAIRE_CREATE = config('QUESTIONNAIRE_CREATE')
INSTITUTIONS = config('INSTITUTIONS')
SHORT_MTA_URL = config('SHORT_MTA_URL')
GIFT_URL = config('GIFT_URL')
BOTWORDS = config('BOTWORDS')
BUTTONS  =config('BUTTONS')
CONTACTS = config('CONTACTS')
MTA = config('MTA')
LINKS = config('LINKS')

user_languages = {}


def change_language(user_id):
    current_lang = user_languages.get(user_id, 'ru')  # По умолчанию 'ru'
    new_lang = 'kg' if current_lang == 'ru' else 'ru'
    user_languages[user_id] = new_lang
    return new_lang


async def fetch_mta_data_from_api() -> List[Dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get(MTA) as response:
            return await response.json()



async def get_botword_text(pkwords, user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BOTWORDS) as response:
            response.raise_for_status()
            botword_data = await response.json()
    
    specific_botword = next((item for item in botword_data if item["pkwords"] == pkwords), None)
    return specific_botword.get(f'botwords_{lang}', None) if specific_botword else None




async def get_short_mta_list(user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(SHORT_MTA_URL) as response:
            response.raise_for_status()
            short_mta_data = await response.json()
    
    return [
        {
            "id": item["id"],
            "string": item.get(f'string_{lang}')
        }
        for item in short_mta_data
    ]



async def get_button_text(pkname, user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BUTTONS) as response:
            response.raise_for_status()
            button_data = await response.json()
    
    specific_button = next((item for item in button_data if item["pkname"] == pkname), None)
    return specific_button.get(f"button_{lang}", None) if specific_button else None




async def get_contacts_data(user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(CONTACTS) as response:
            response.raise_for_status()
            data = await response.json()
            contacts = []
            for contact in data:
                name = contact.get(f'{lang}_name', 'Имя не доступно')
                contacts.append({
                    'name': name,
                    'link': contact['link']
                })
            return contacts




async def get_links_data(user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(LINKS) as response:
            response.raise_for_status()
            data = await response.json()
            links = []
            for link in data:
                name = link.get(f'{lang}_name', 'Имя не доступно')
                links.append({
                    'name': name,
                    'link': link['link']
                })
            return links




async def send_questionnaire_data(name, phone_number, date_of_birth, address, gift_name):
    payload = {
        'name': name,
        'phone_number': phone_number,
        'date_of_birth': date_of_birth,  # Дата как строка
        'address': address,
        'type_gift': gift_name
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(QUESTIONNAIRE_CREATE, json=payload) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                result = await response.json()
                return result
        except aiohttp.ClientResponseError as e:
            print(f"Ошибка при отправке данных анкеты: {e}")



async def get_institution_data(institution_id, user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(INSTITUTIONS) as response:
            response.raise_for_status()
            institution_data = await response.json()
    
    institution = next((item for item in institution_data if item["id"] == institution_id), None)
    return institution.get(f'string_{lang}', 'Информация отсутствует.') if institution else 'Информация отсутствует.'




async def get_mta_data_by_id(mta_id, user_id) -> str:
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(MTA) as response:
            response.raise_for_status()
            institution_data = await response.json()

    number_pattern = re.compile(r'№\s*(\d{1,2})')

    for item in institution_data:
        match = number_pattern.search(item.get(f'string_{lang}', ''))
        if match:
            found_number = int(match.group(1))
            if found_number == mta_id:
                result = item.get(f'string_{lang}', 'Информация отсутствует.')
                return result
    return 'Информация отсутствует.'





async def get_gift_options(user_id):
    lang = user_languages.get(user_id, 'ru')  # Получаем текущий язык пользователя
    
    async with aiohttp.ClientSession() as session:
        async with session.get(GIFT_URL) as response:
            response.raise_for_status()
            gift_data = await response.json()
    
    gift_options = []
    for item in gift_data:
        gift_options.append({
            'id': item['id'],
            f'gift_type_{lang}': item[f'gift_type_{lang}']
        })
    return gift_options







################Google sheet


def sync_connect_to_google_sheet(json_file_path, sheet_name):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(json_file_path, scopes=scopes)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1
    return sheet


def sync_send_data_to_google_sheet(sheet, data):
    sheet.append_row(data)


async def connect_to_google_sheet(json_file_path, sheet_name):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        sheet = await loop.run_in_executor(pool, sync_connect_to_google_sheet, json_file_path, sheet_name)
    return sheet


async def send_data_to_google_sheet(sheet, data):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, sync_send_data_to_google_sheet, sheet, data)
