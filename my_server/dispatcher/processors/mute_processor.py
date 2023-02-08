from typing import Callable, Dict, Tuple
from server import Server
from typz import Message, Permissions, Request

def mute_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    client_to_mute = server.clients.get_client_by_name(request.passive_username)
    data = 'You are now muted'
    permissions = Permissions.SEND
    if client_to_mute.permissions == permissions: # If client is already muted, unmute
        permissions = permissions.READ 
        data = 'You are no longer muted'
    
    message = Message(client=request.sock, sender=server.name,
                    data=data)

    args = {'client': client_to_mute, 'permssions': permissions, 'message': message}
    return server.change_client_permissions, args

