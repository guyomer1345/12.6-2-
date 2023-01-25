import socket
import logging
from enum import Enum
from exceptions.exceptions import ProtocolError

class Protocol(Enum):
    MESSAGE_PADDING = 10
    CMD_PADDING = 1
    NAME_PADDING = 2


def recv(sock: socket.socket, amount: int) -> bytes:
    try:
        left_to_read = int(sock.recv(amount))
    except ValueError:
        logging.warning(f"Message didn't follow protcol")
        raise ProtocolError()
    
    data = b''
    while len(data) != left_to_read:
        data += sock.recv(left_to_read-len(data))
    
    return data


def recv_name(sock: socket.socket, amount: int = Protocol.NAME_PADDING) -> str:
    name = recv(sock, amount).decode()
    
    return name


def recv_cmd(sock: socket.socket) -> int:
    cmd = int(sock.recv(Protocol.CMD_PADDING))
    
    return cmd


def recv_message(sock: socket.socket, amount: int = Protocol.MESSAGE_PADDING) -> str:
    messsage = recv(sock, amount).decode()
    
    return messsage


def send_message(sock: socket.socket, message):
    pass