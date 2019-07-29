import json
from config_provider import get_pokemons_file_path

with open(get_pokemons_file_path(), 'r') as pokemon_json:
    pokemons_list = json.load(pokemon_json)['pokemons']