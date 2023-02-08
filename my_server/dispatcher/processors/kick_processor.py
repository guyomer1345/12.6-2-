from typing import Callable, Dict, Tuple
from server import Server
from typz import Request

def kick_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    # check  that client isn't self
    client_to_kick = request.passive_username
    client_to_kick = server.clients.get_client_by_name(client_to_kick)
    
    kick_message = f'{request.passive_username} was kicked from the chat!'
    return server.disconnect, {'message': kick_message, 'sock': client_to_kick.sock}

