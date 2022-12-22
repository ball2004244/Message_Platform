import threading
import socketserver

class ChatHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.clients = []
        super().__init__(request, client_address, server)

    def handle(self):
        # Add the client to the list of clients
        self.clients.append(self.request)

        # Continuously receive messages from the client and broadcast them to all clients
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            
            # here to process private message
            # 
            for client in self.clients:
                client.sendall(data)
                text = data.decode('utf-8') 
                print(text)

        # Remove the client from the list of clients
        self.clients.remove(self.request)

    def private_message(self, user1, user2):
        pass 
    
class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    # Start the server
    server = ChatServer((HOST, PORT), ChatHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f'Server running on {HOST}:{PORT}')

    # Run the server until interrupted
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
