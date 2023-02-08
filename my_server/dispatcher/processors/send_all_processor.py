import logging
from typing import Dict, Tuple, Callable
from server import Server
from typz import Message
from typz import Request

def send_all_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    sender_client = server.clients.get_client_by_name(request.username)
    clients_to_send = server.clients.get_valid_recipients()
    message = Message(client=sender_client.sock, sender=sender_client.get_name(),
                    data=request.message)
    
    args = {'clients': clients_to_send, 'message': message}

    logging.info(f'Adding message from {sender_client.get_name()}')
    return server.add_messages_to_clients, args