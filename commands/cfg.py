import json


def update():
    file = open("config.json", "r")
    config = json.load(file)
    file.close()
    return config