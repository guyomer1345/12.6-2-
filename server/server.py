import select
import socket
from client.clients import Clients

#ip, port = arg_pat

class Server:
    def __init__(self, ip: str = '0.0.0.0', port: int = 8000, clients: Clients = None):
        self.ip = ip
        self.port = port
        self.sock = socket.socket((ip, port))
        self.clients = clients or Clients()
        self.is_running = True
    
    def send(self):
        return NotImplemented

    def disconnect(self):
        return NotImplemented

    def accept(self):
        return NotImplemented

    
def main():
    server = Server()
    while server.is_running:
            
        clients = server.clients.clients
        r_list, w_list, x_list = select.select(r_list= clients+[server.sock], w_list=clients, x_list=clients)
        for socket in r_list:
            client = server.clients.get_client_by_sock(sock=socket)
            message = client.get_message()
        #   data = get_data()
        #   dispatch(data)
        # 
        # for socket in w_list:
        #   data = message_queue[socket]
        #   for message in data:
        #       send(message)   
        # 
        # for socket in x_list:
        #   disconnect(socket)     
        pass


'''
Client
generic client 
attributes - name, socket, addr

user_client(Client)
implementation of client for user 
attributes - __super__... , message queue: queue[bytes], 

Clients
attributes clients: List[client]

SERVER
attributes - port, ip, clients: Dict[socket, Client]
functions - set_server, recv_message(from protocol), accept_client

COMMANDS (ENUM)
SEND_ALL = 1
...
'''
