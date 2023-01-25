from dataclasses import dataclass
from enum import Enum


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
class Message:
    user: str
    cmd: Commands
    passive_user: str
    message: str