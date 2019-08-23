from datetime import datetime
from pytz import timezone

from pyrogram.client.filters.filters import Filters

from bot_client import client, pyrogram
from bot_helpers import name_asked, get_tz, get_address
from pokemons import pokemons_list
from db_interaction import save_pokemon_spawn_db

add_spawn = pyrogram.KeyboardButton(text='Добавить спавн покемона')
show_map = pyrogram.KeyboardButton(text='Ссылка на карту')
subscribe_for_notification = pyrogram.KeyboardButton(text='Уведомлять о новых спавнах')
keyboard = pyrogram.ReplyKeyboardMarkup(keyboard=[[add_spawn, show_map, subscribe_for_notification]])


@client.on_message(filters=Filters.create(lambda _, m: m.text == '/start'))
def _show_main_button(client: pyrogram.Client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text='Выберите действие', reply_markup=keyboard)


@client.on_message(filters=Filters.create(lambda _, m: m.text == 'Добавить спавн покемона'))
def ask_pokemon_name(client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text='Имя покемона:')
    name_asked(True)


@client.on_message(filters=Filters.create(lambda _, m: m.text == 'Ссылка на карту'))
def send_map(client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text='https://pokemon-spawn-map.herokuapp.com/map/')


Pokemon = None


@client.on_message(filters=Filters.create(lambda _, m: name_asked()))
def save_pokemon_name(client, message):
    chat_id = message.chat.id
    global Pokemon
    Pokemon = pokemon = message.text.capitalize()
    if pokemon in pokemons_list:
        # client.send_message(chat_id, text='Имя покемона сохранено')
        save_pokemon_spawn_button = pyrogram.KeyboardButton(text=f'Сохранить спавн покемона {pokemon}',
                                                            request_location=True)
        keyboard = pyrogram.ReplyKeyboardMarkup(keyboard=[[save_pokemon_spawn_button]])
        client.send_message(chat_id, text='Нажмите, чтобы передать координаты', reply_markup=keyboard)
        name_asked(False)
    else:
        client.send_message(chat_id, text='Проверьте правильность имени покемона')


def _return_to_main_keyboard(client, message, text):
    chat_id = message.chat.id
    client.send_message(chat_id, text=text, reply_markup=keyboard)


@client.on_message(filters=Filters.location)
def save_pokemon_spawn(client, message):
    location = message.location
    ###перенести на бекенд сайта
    tz_str = get_tz(location)

    dt = datetime.fromtimestamp(message.date).astimezone(timezone(tz_str))
    address = get_address(location)
    ###
    if Pokemon and address and save_pokemon_spawn_db(Pokemon, (location.latitude, location.longitude), dt, address):
        text = 'Спавн покемона будет добавлен на карту в течение 5-10 минут'
    else:
        text = 'Что то пошло не так'
    _return_to_main_keyboard(client, message, text)


client.run()
