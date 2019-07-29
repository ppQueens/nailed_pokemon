from configparser import ConfigParser

__config = ConfigParser()
__config.read('config.ini')

if not __config.sections():
    raise FileNotFoundError('Check existence of your config file')