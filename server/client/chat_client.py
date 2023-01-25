import socket
from client.b_client import Client
from protocol.protocol import recv_cmd, recv_message, recv_name
from typz import Message, Permissions


class ChatClient(Client):
    def __init__(self, sock: socket.socket, permissions: Permissions = Permissions.SEND):
        super(self, sock)
        self.permissions = permissions
    
    def get_message(self) -> Message:
        user = recv_name(sock=self.sock)
        cmd = recv_cmd(sock=self.sock)
        passive_user = recv_name(sock=self.sock)
        message = recv_message(sock=self.sock)

        return Message(user, cmd, passive_user, message)