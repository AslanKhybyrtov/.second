import configparser
from config import *

config = configparser.ConfigParser()
config.read('config/setting.ini')

def config_update():
    with open(r'settings/settings.ini', 'w') as f:
        config.write(f)
    config.read(r'settings/settings.ini')