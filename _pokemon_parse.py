import requests
import json
from bs4 import BeautifulSoup

url = 'https://pokemondb.net/pokedex/national'
html_page = requests.get(url).content

soup = BeautifulSoup(html_page, 'html.parser')


def get_pokemons_names():
    all_infocards = soup.find_all('a', class_='ent-name')
    # all_pokemon_name = all_infocards.find_all('a', class_='ent-name')

    pokemons_names = tuple(pokemon_name.get_text() for pokemon_name in all_infocards)
    pokemons = {'pokemons': pokemons_names}

    with open('pokemons.txt', 'w') as json_file:
        json.dump(pokemons, json_file)

    return pokemons_names


def get_pokemons_sprites():
    sprites = soup.find_all('span', class_='img-sprite')
    for i in sprites:
        file_name = i['data-src'].rsplit('/')[-1]
        file = requests.get(i['data-src'])
        with open(f'media\\{file_name}', 'wb') as image:
            image.write(file.content)

# get_pokemons_sprites()
