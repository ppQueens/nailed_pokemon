# import mysql.connector
import mysql
import os
from geopy import Point
from datetime import datetime

import _pokemon_parse
import pokemons
from config_provider import get_db_config


class SpawnDataValidation:
    """
    coordinates = (lat,lon)
    """

    def __init__(self, pokemon: str, coordinates: tuple):
        self.pokemon = pokemon.capitalize()
        self.coordinates = coordinates

    def validate(self):
        return self._coordinate_validation() and self._pokemon_name_validation()

    def _coordinate_validation(self):
        try:
            Point(*self.coordinates)
        except ValueError:
            return False
        return True

    def _pokemon_name_validation(self):
        return self.pokemon in pokemons.pokemons_list


def save_pokemon_spawn_db(pokemon, coordinates, dt, address):
    """
    :param pokemon: pokemon_name
    :type pokemon: str

    :param coordinates: (lat, lon)
    :type coordinates: tuple
    """

    validation = SpawnDataValidation(pokemon, coordinates)
    if validation.validate():
        try:
            cnx = mysql.connector.connect(**get_db_config())
            cursor = cnx.cursor()
            add_spawn = ("INSERT INTO  spawns_map_pokemonspawn"
                         "(pokemon_id, lat, lon, created, time_zone, modified, country, state, city, confirming_spawn, confirmed, on_map) "
                         "VALUES ((SELECT id FROM spawns_map_pokemon WHERE pokemon_name=%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_spawn = (pokemon.capitalize(), *coordinates, dt, dt.tzinfo.zone, dt,
                          address['country'], address['state'], address['city'], False, 0, False)

            cursor.execute(add_spawn, data_spawn)
            cnx.commit()

            cursor.close()
            cnx.close()
            return True
        except mysql.connector.Error as err:
            print(err)
    return False


def _populate_pokemons_table(pokemons):
    connection = mysql.connector.connect(**get_db_config())

    # connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    cursor = connection.cursor()
    add_spawn = ("INSERT INTO  spawns_map_pokemon"
                 "(pokemon_name, created, modified, pokemon_image_path) "
                 "VALUES (%s, %s, %s, %s)")
    pokemons_data = [(pokemon_name, datetime.now(), datetime.now(), '') for pokemon_name in pokemons]

    cursor.executemany(add_spawn, pokemons_data)
    connection.commit()

    cursor.close()
    connection.close()
    return True

# data = ('bulbasaur', (30., 51.))
#
# save_pokemon_spawn_db(*data)
# import _pokemon_parse

def populate():
    _populate_pokemons_table(_pokemon_parse.get_pokemons_names())
