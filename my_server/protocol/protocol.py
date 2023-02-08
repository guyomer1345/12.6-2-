import socket
import logging
from enum import Enum
import time
from exceptions.exceptions import ProtocolError

class Protocol(Enum):
    MESSAGE_PADDING = 10
    CMD_PADDING = 1
    NAME_PADDING = 2


def sock_receive(sock: socket.socket, amount: int) -> bytes:
    try:
        left_to_read = int(sock.recv(amount))
        
        data = b''
        while len(data) != left_to_read:
            data += sock.recv(left_to_read-len(data))
        
        return data

    except Exception as e:
        raise ProtocolError(str(e))

def receive_name(sock: socket.socket, amount: int = Protocol.NAME_PADDING.value) -> str:
    name = sock_receive(sock, amount).decode()
    
    return name


def receive_cmd(sock: socket.socket) -> int:
    cmd = int(sock.recv(Protocol.CMD_PADDING.value))
    
    return cmd


def receive_message(sock: socket.socket, amount: int = Protocol.MESSAGE_PADDING.value) -> str:
    messsage = sock_receive(sock, amount).decode()
    
    return messsage


def send_message(sock: socket.socket, data: bytes, sender: str) -> None:
    current_time = time.strftime("%H:%S")
    message = f"{current_time} {sender}: {data}".encode()
    message = str(len(message)).zfill(Protocol.MESSAGE_PADDING.value).encode() + message
    sock.send(message)