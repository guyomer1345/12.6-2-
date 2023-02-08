from typing import Callable, Dict, Tuple
from server import Server
from typz import Request, Message

def view_managers_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    admins = server.clients.get_admins()
    admins = ', '.join([admin.get_name() for admin in admins])
    
    sender = server.name
    data = f'Managers are: {admins}'
    clients = [server.clients.get_client_by_sock(request.sock)]
    message = Message(client=request.sock, sender=sender, data=data)

    return server.add_messages_to_clients, {'clients': clients, 'message': message}