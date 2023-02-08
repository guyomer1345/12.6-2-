from typing import Callable, Dict, Tuple
from server import Server
from typz import Request, Message


def private_message_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:    
    sender_client = server.clients.get_client_by_name(request.username)
    client_to_send = server.clients.get_client_by_name(request.passive_username)

    message = Message(client=sender_client.sock, sender=sender_client.get_name(),
                    data=request.message)
    
    return server.add_messages_to_clients, {'clients': [client_to_send], 'message': message}