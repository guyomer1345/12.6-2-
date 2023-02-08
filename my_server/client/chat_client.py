import socket
from exceptions.exceptions import ProtocolError
from protocol.protocol import receive_cmd, receive_message, receive_name
from typz import Commands, Request, Permissions, Message, ADMIN_PREFIX
from queue import Queue




class ChatClient:
    def __init__(self, sock: socket.socket, name: str = None,
                 message_queue: Queue[Message] = None, permissions: Permissions = Permissions.SEND):
        
        self.name = name
        self.sock = sock
        self.permissions = permissions
        self.message_queue = message_queue or Queue()
    
    def set_name(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        name = self.name
        if self.permissions == Permissions.ADMIN:
            name = ADMIN_PREFIX + name
        
        return name

    def get_request(self) -> Request:
        try:
            username = receive_name(sock=self.sock)
            cmd = Commands(receive_cmd(sock=self.sock))
            passive_user = receive_name(sock=self.sock)
            message = receive_message(sock=self.sock)

            return Request(username=username, cmd=cmd, passive_username=passive_user, 
                            message=message, sock=self.sock)

        except ValueError:
            raise ProtocolError("The request didn't follow protocol")