from dataclasses import dataclass
from enum import Enum
import socket

MESSAGE_PADDING = 10
ADMIN_PREFIX = '@'

class Commands(Enum):
    SEND_ALL = 1
    PROMOTE = 2 
    KICK = 3
    MUTE = 4
    PRIVATE_MESSAGE = 5
    VIEW_MANAGERS = 6 
    EXIT = 7 


class Permissions(Enum):
    SEND = 0
    READ = 1
    ADMIN = 2


@dataclass
class Request:
    sock: socket.socket
    username: str
    cmd: Commands
    passive_username: str
    message: str


@dataclass
class Message:
    client: socket.socket
    sender: str
    data: bytes


