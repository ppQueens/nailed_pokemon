from pyrogram.client.filters.filters import Filters

from bot_client import client, pyrogram
from bot_helpers import name_asked
from pokemons import pokemons_list
from db_interaction import save_pokemon_spawn_db

main_button = pyrogram.KeyboardButton(text='Добавить спавн покемона')
keyboard = pyrogram.ReplyKeyboardMarkup(keyboard=[[main_button]])


@client.on_message(filters=Filters.create(lambda _, m: m.text == '/start'))
def _show_main_button(client: pyrogram.Client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text='Выберите действие', reply_markup=keyboard)


@client.on_message(filters=Filters.create(lambda _, m: m.text == 'Добавить спавн покемона'))
def ask_pokemon_name(client, message):
    chat_id = message.chat.id
    client.send_message(chat_id, text='Имя покемона:')
    name_asked(True)

Pokemon = None
@client.on_message(filters=Filters.create(lambda _, m: name_asked()))
def save_pokemon_name(client, message):
    chat_id = message.chat.id
    global Pokemon
    POKEMON = pokemon = message.text.capitalize()
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
    if Pokemon and save_pokemon_spawn_db(Pokemon, (location.latitude, location.longitude)):
        text = 'Спавн покемона помечен на карте'
    else:
        text = 'Спавн покемона помечен на карте'

    _return_to_main_keyboard(client, message, text)


client.run()
