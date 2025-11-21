import socket
import threading

class Server:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.clients = []
        self.lock = threading.Lock()
    
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.socket.accept()
            print(f"New connection: {addr}")
            
            with self.lock:
                self.clients.append(client_socket)
            
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.daemon = True
            thread.start()
    
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"Received: {data}")
                
                # Просто пересылаем сообщение всем клиентам
                self.broadcast(data, client_socket)
        
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            with self.lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            client_socket.close()
            print("Client disconnected")
    
    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.clients.remove(client)

if __name__ == "__main__":
    server = Server()
    server.start()