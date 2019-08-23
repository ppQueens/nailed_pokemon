import psycopg2
import os

from datetime import datetime
import pokemons

from validators import SpawnDataValidation


def db(query, data):
    try:
        connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cursor = connection.cursor()
    except psycopg2.DatabaseError as de:
        connection = None
        # log
    try:
        # print(cursor.mogrify(add_spawn, data_spawn))
        cursor.execute(query, data)
        connection.commit()

        return True
    except AttributeError as ae:
        print(ae)
    except psycopg2.DatabaseError as de:
        connection.rollback()
        cursor.close()
        connection.close()
        #log
    return False


def save_pokemon_spawn_db(pokemon, coordinates, dt, address):
    """
    :param pokemon: pokemon_name
    :type pokemon: str

    :param coordinates: (lat, lon)
    :type coordinates: tuple
    """

    validation = SpawnDataValidation(pokemon, coordinates)

    if validation.validate():

        add_spawn = ("INSERT INTO  spawns_map_pokemonspawn"
                     "(pokemon_id, lat, lon, created, time_zone, modified, country, state, city, confirming_spawn, confirmed, on_map) "
                     "VALUES ((SELECT id FROM spawns_map_pokemon WHERE pokemon_name=%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_spawn = (pokemon.capitalize(), *coordinates, dt, dt.tzinfo.zone, dt,
                      address['country'], address['state'], address['city'], False, 0, False)
        return db(add_spawn, data_spawn)
    return False


def _populate_pokemons_table(pokemons):
    # cnx = mysql.connector.connect(**get_db_config())

    add_spawn = ("INSERT INTO  spawns_map_pokemon"
                 "(pokemon_name, created, modified, pokemon_image_path) "
                 "VALUES (%s, %s, %s, %s)")
    pokemons_data = [(pokemon_name, datetime.now(), datetime.now(), '') for pokemon_name in pokemons]

    return db(add_spawn, pokemons_data)


# data = ('bulbasaur', (30., 51.))
#
# save_pokemon_spawn_db(*data)

def populate():
    _populate_pokemons_table(pokemons.pokemons_list)
