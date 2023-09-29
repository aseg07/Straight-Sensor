JSON_FILE = "config.json"
vars = {}

def save_data():
    with open(JSON_FILE, 'w') as outfile:
        json.dump(vars, outfile)
    print('save data')
    print(vars)

def load_data():
    global vars
    print('load data')
    try:
        with open(JSON_FILE) as json_file:
            vars = json.load(json_file)
            print(data)
    except:
        print('error to load json data')
