from connector import Client
import json
import settings as st
import uuid

def create_config():
    data = {
        "username": input(st.username_question),
        "userid": str(uuid.uuid4()),
        "version": st.version,
    }
    return data

def config_is_correct(conf: dict):
    return ("version" in conf and "username" in conf and "userid" in conf)

def pre_connect():
    print(f"{st.title} {st.version}\n")
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        if not config_is_correct(data): raise Exception
    except:
        data = create_config()
        # json.dump(data, file, indent=4)
    
    if ("lastserver" in data and 
            input(f"{st.connect_server_question}({data['lastserver'][0]}:{data['lastserver'][1]}) ").lower() == 'y'):
        return data, *data['lastserver']
    else:
        return [data, input(st.ip_question), int(input(st.port_question))]
    
def post_connect(data, ip, port):
    if "lastserver" in data and data['lastserver'] != [ip, port]:
        if input(st.save_server_question).lower() == 'y':
            data['lastserver'] = [ip, port]
    else:
        data['lastserver'] = [ip, port]

    with open('config.json', 'w') as file:
        json.dump(data, file, indent=4)

    

if __name__ == "__main__":
    data, ip, port = pre_connect()
    client = Client(data, ip, port)
    client.start()
    post_connect(data, ip, port)