import json

def read(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def write(data, file='Save'):
    with open(file, 'w') as json_file:
        json.dump(data, json_file)
    return file

player_data={'name':'Vandi', 'level_count':1}

print(read(write(player_data))['name'])