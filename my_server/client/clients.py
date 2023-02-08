import socket
from typing import List
from client.chat_client import ChatClient
from typz import Message, Permissions, Request


class Clients:
    def __init__(self, clients: List[ChatClient] = None):
        self.clients = clients or []
    
    def get_admins(self) -> List[ChatClient]:
        admins: List[ChatClient] = [] 
        for client in self.clients:
            if client.permissions == Permissions.ADMIN:
                admins.append(client)
        
        return admins
        
    def delete_client(self, client: ChatClient):
        self.clients.remove(client)

    def add_new_client(self, sock: socket.socket):
        new_client = ChatClient(sock=sock)
        self.clients.append(new_client)

    def get_valid_recipients(self) -> list[ChatClient]:
        valid_clients = []
        for client in self.clients:
            if client.permissions in [Permissions.READ, Permissions.ADMIN] and client.get_name():
                valid_clients.append(client)
        
        return valid_clients

    def count_valid_clients(self) -> int:
        count = 0
        for client in self.clients:
            if client.name:
                count += 1
        
        return count

    def add_to_queue(self, clients_to_add: list[ChatClient], message: Message):
        for client in clients_to_add:
            client.message_queue.put_nowait(message)

    def get_client_by_name(self, name: str) -> ChatClient:
        for client in self.clients:
            if name == client.name and name != None:
                return client
        
        return None

    def get_client_by_sock(self, sock: socket.socket) -> ChatClient:
        for client in self.clients:
            if sock == client.sock:
                return client

        return None
    
    def get_all_socks(self) -> List[socket.socket]:
        sockets = []
        for client in self.clients:
            sockets.append(client.sock)
        
        return sockets