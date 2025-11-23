from connector import Client
import json
import settings as st
from config_handler import *

def pre_connect():
    print(f"{st.title} v{st.version}\n")
    data = get_config()
    
    if ("lastserver" in data and 
            input(f"{st.connect_server_question}({data['lastserver'][0]}:{data['lastserver'][1]}) ").lower() != 'n'):
        return data, *data['lastserver']
    else:
        return [data, input(st.ip_question), int(input(st.port_question))]
    
def post_connect(data, ip, port):
    if "lastserver" in data and data['lastserver'] != [ip, port]:
        if input(st.save_server_question).lower() == 'y':
            data['lastserver'] = [ip, port]
    else:
        data['lastserver'] = [ip, port]

    set_config(data)

    

if __name__ == "__main__":
    data, ip, port = pre_connect()
    client = Client(data, ip, port)
    client.start()
    post_connect(data, ip, port)
    input()