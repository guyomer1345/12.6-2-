from dataclasses import dataclass, field
import socket
from typing import Any, List
from client.b_client import Client
from client.chat_client import ChatClient


@dataclass 
class Clients:
    clients: List[ChatClient] = field(default_factory=list)

    def get_client_by_sock(self, sock: socket.socket) -> ChatClient:
        for client in self.clients:
            if sock == client.sock:
                return client

        return None