import json


def read_config():
    with open('config.json') as cfg_file:
        return json.load(cfg_file)


def read_bot_config():
    return read_config()['Bot']


def read_mal_config():
    return read_config()['MAL']
