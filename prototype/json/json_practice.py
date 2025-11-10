import json

class Test():
    def __init__(self,val,var):
        self.val=val
        self.var=var

def read(file):
    file=file+".json"
    with open(file) as json_file:
        data = json.load(json_file)
    return data

def write(data, file='Save'):
    file=file+'.json'
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(", ", " : "), sort_keys=True)
    return file

player_data={'name':'Vandi',
             'level_count':1}
player_data1={'name':'Denys',
              'level_count':5}

# write(player_data, player_data['name'])
# write(player_data1, player_data1['name'])

a=Test(5,3)
write([a.val,a.var], 'Test')

print(read('Denys')['name'])