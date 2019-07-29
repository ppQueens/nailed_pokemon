from configparser import ConfigParser

__config = ConfigParser()
__config.read('config.ini')

if not __config.sections():
    raise FileNotFoundError('Check existence of your config file')


def get_telegram_secret_key():
    return __config['telegram']['key']


def get_telegram_api_id():
    return __config['telegram']['api_id']


def get_telegram_api_hash():
    return __config['telegram']['api_hash']


def get_pokemons_file_path():
    return __config['pokemons-file']['path']


def get_db_config():
    return dict(__config['db'])
