import socket
import threading
import json

class Client:
    def __init__(self, data, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.data = data
        self.username = data['username']
        self.userid = data['userid']
        self.socket = None
        self.running = False
    
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        
        # Поток для приема сообщений
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Основной поток для ввода
        self.send_messages()
    
    def send_data(self, message):
        try:
            self.socket.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")

    def recv_data(self, bufsize=1024):
        message = self.socket.recv(1024).decode('utf-8')
        return json.loads(message)

    def receive_messages(self):
        while self.running:
            try:
                message = self.recv_data(1024)
                if not message:
                    break
                print(f"\n{message['username']}: {message['text']}\n> ", end='')
            except:
                break
        
        self.running = False
        print("\nDisconnected from server")
    
    def send_messages(self):
        print("Connected to server. Type messages (type 'quit' to exit):")
        
        while self.running:
            try:
                message = input("> ")
                if message.lower() == 'quit':
                    break
                
                self.send_data({
                    "text": message,
                    "username": self.username,
                    "userid": self.userid,
                    })
            except EOFError:
                break
            except Exception as e:
                print(f"Send error: {e}")
                break
        
        self.running = False
        self.socket.close()
