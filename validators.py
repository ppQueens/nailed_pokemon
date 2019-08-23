from geopy import Point

import pokemons


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
