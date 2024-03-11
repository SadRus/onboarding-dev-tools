import httpx

from datetime import datetime
from dotenv import load_dotenv
from pydantic import ValidationError
from tg_api import (
    SyncTgClient,
    SendMessageRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    SendBytesPhotoRequest,
)

from env_settings import EnvSettings
from models import Order


load_dotenv()

ENV = EnvSettings()

httpx.request
with httpx.Client() as session:

    #  Отправить GET запрос с  JSON
    url = 'https://proxys.io/ru/api/v2/balance'
    params = {
        'key': '62c25238cb58a7fd87ee824292f3594d'
    }
    response = session.request('GET', url, params=params, json={'example': 'json'})
    response.raise_for_status()
    print(response.json())

    # Отправить POST запрос с JSON. Экспортировать данные в формат JSON с помощью Pydantic.
    order = Order(
        order_id=1,
        country_code='RU',
        expires_at=datetime.now(),
    )
    response = session.post("https://httpbin.org/post", json=order.json())
    response.raise_for_status()

    # Прочитать данные из JSON с помощью Pydantic (parse_raw)
    order_data = Order.parse_raw(response.json()['json'])
    print(order_data)


# Получить ошибку валидации модели
try:
    order = Order(
        order_id=-1,
        country_code='RU',
        expires_at=datetime.now(),
    )
except ValidationError as err:
    print(err)


# Документация Telegram Bot API
'''
разобраться как устроено взаимодействие бота с сервером Tg в режиме вебхука:
    - бот(код бота) не опрашивает тг сервер на наличие обновлений(polling)
    - тг сервер сам присылает Update на указанный вебхук(POST request)
    - Update мы обрабатываем с помощью бэкенда

что присылает боту сервер Tg по Update:
    update_id, message, edited_message, callback_query, message_reaction, inline_query...

установить вебхук
    curl https://api.telegram.org/bot${TG_BOT_TOKEN}/setWebhook
    curl -F "url=${PUBLIC_URL}/webhook/" https://api.telegram.org/bot${TG_BOT_TOKEN}/setWebhook
'''

# Отправить себе сообщение от имени бота с помощью библиотеки HTTPX
TG_BOT_TOKEN = ENV.TG.BOT_TOKEN
TG_CHAT_ID = ENV.TG.CHAT_ID

url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
data = {
    'chat_id': TG_CHAT_ID,
    'text': 'message by sendMessage endpoint'
}
response = httpx.post(url, json=data)
response.raise_for_status()


# TODO Product Flow

# Библиотека Tg API

with SyncTgClient.setup(TG_BOT_TOKEN):

    # Отправить себе текстовое сообщение от имени tg-бота
    tg_request = SendMessageRequest(
        text='Message from tg-api',
        chat_id=TG_CHAT_ID
    )
    tg_request.send()

    # Отправить себе текстовое сообщение с кнопками от имени tg-бота
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='one', callback_data='one'),
                InlineKeyboardButton(text='two', callback_data='two'),
            ]
        ]
    )
    tg_request = SendMessageRequest(
        text='Message with inline buttons',
        chat_id=TG_CHAT_ID,
        reply_markup=keyboard,
    )
    tg_request.send()

    # Отправить себе сообщение с картинкой от имени tg-бота
    with open('beconizer.jpg', 'rb') as file:
        photo_content = file.read()
    tg_request = SendBytesPhotoRequest(
        chat_id=TG_CHAT_ID,
        photo=photo_content,
    )
    tg_request.send()
