from queue import Empty
import select
import socket
from typing import List, Tuple
from client.clients import Clients
from client.chat_client import ChatClient
from exceptions.exceptions import ProtocolError
from protocol.protocol import send_message
from typz import Message, Permissions
import logging


class Server:
    def __init__(self, ip: str = '0.0.0.0', port: int = 8000, clients: Clients = None, name: str = 'SERVER', max_listen: int = 5):
        self.ip = ip
        self.name = name
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = clients or Clients()
        self.max_listen = max_listen
        self.is_running = True
    
    def run_server(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.max_listen)
        logging.info('Server is up and running!')

    def accept_new_connection(self):
        client, addr = self.sock.accept()
        self.clients.add_new_client(client)

        logging.info(f'New client joined {addr}')
    
    def broadcast_message(self, data: str):
        message = Message(client = self.sock, sender=self.name, data=data)
        clients = self.clients.clients
        args = {'message': message, 'clients': clients}

        self.add_messages_to_clients(**args)

    def process_r_list(self, r_list: List[socket.socket], dispatcher: callable):
        try:
            for socket in r_list:
                client = self.clients.get_client_by_sock(sock=socket)
                if not client: # New connection
                    self.accept_new_connection()
                
                if client:
                    request = client.get_request()
                    action, args = dispatcher(server=self, request=request)
                    if action: action(**args)

        except ProtocolError:
            self._disconnect(socket=socket)

    def process_w_list(self, w_list: List[socket.socket]):
        for socket in w_list:
            client = self.clients.get_client_by_sock(sock=socket)
            try:
                message = client.message_queue.get(block=False)
                sender, data, sock = message.sender, message.data, client.sock
                send_message(sender=sender, sock=sock, data=data)

            except Empty:
                pass
    
    def process_x_list(self, x_list: List[socket.socket]):
        for sock in x_list:
            self.disconnect({'sock': sock})

    def get_lists(self) -> Tuple[List[socket.socket], List[socket.socket], List[socket.socket]]: #TODO change name
        clients = self.clients.get_all_socks()
        return select.select(clients+[self.sock], clients, clients)

    def _disconnect(self, socket: socket.socket, custom_message: str = ""):
        client = self.clients.get_client_by_sock(sock=socket)
        client.sock.close()
        self.clients.delete_client(client=client)

        name = client.get_name()
        message = custom_message or f'{name} has left the chat'
        
        self.broadcast_message(data=message)

    def disconnect(self, **kwargs):
        sock: socket.socket = kwargs['sock']
        exit_message = kwargs.get('message', '')

        self._disconnect(socket=sock, custom_message=exit_message)

    def add_messages_to_clients(self, **kwargs):
        message: Message = kwargs['message'] 
        clients: List[ChatClient] = kwargs['clients']

        for client in clients:
            client.message_queue.put_nowait(message)
    
    def change_client_permissions(self, **kwargs):
        client: ChatClient = kwargs['client'] 
        permissions: Permissions = kwargs['permssions']
        message: Message = kwargs['message']

        client.permissions = permissions
        
        args = {'message': message, 'clients': [client]}
        self.add_messages_to_clients(**args)

