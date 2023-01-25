from protocol.protocol import recv_cmd, recv_message, recv_name
from typz import Message, Permissions
from abc import ABC
import socket



class Client(ABC):
    def __init__(self, sock: socket.socket):
        self.sock = sock
        