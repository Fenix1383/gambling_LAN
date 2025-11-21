import socket
import threading

class Client:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
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
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\nReceived: {message}\n> ", end='')
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
                
                self.socket.send(message.encode('utf-8'))
            except EOFError:
                break
            except Exception as e:
                print(f"Send error: {e}")
                break
        
        self.running = False
        self.socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()