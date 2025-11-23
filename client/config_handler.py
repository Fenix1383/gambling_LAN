import settings as st
import uuid
import json

def recreate_config(conf):
    if 'lastserver' not in conf:
        data = {
            "username": conf['username'],
            "userid": conf['userid'],
            "version": st.version
        }
    else:
        data = {
            "username": conf['username'],
            "userid": conf['userid'],
            "version": st.version,
            "lastserver": conf['lastserver'],
        }
    return data

def create_config():
    data = {
        "username": input(st.username_question),
        "userid": str(uuid.uuid4()),
        "version": st.version,
    }
    return data

def vtoint(version: str):
    v = [int(i) for i in version.split('.')]
    return v[0]*256 + v[1]*16 + v[2]

def config_is_correct(conf: dict):
    correct = ("version" in conf and "username" in conf and "userid" in conf)
    if correct:
        if conf["version"] == st.version: return 2
        elif vtoint(conf["version"]) < vtoint(st.version): return 1
        else: return 3
    return 0 

def get_config():
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        correct = config_is_correct(data)
        if not correct: raise Exception
        elif correct == 1: data = recreate_config(data)
        elif correct == 3:
            if input(st.recreate_config_question).lower() == 'y':
                data = recreate_config(data)
            else: exit()
    except:
        data = create_config()

    return data

def set_config(data):
    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)
