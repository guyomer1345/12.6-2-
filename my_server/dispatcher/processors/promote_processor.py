from typing import Callable, Dict, Tuple
from server import Server
from typz import Message, Permissions, Request

def promote_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    client_to_promote = server.clients.get_client_by_name(request.passive_username)
    data = 'You are now an admin'
    permissions = Permissions.ADMIN
    if client_to_promote.permissions == permissions: # If client is already admin, demote
        permissions = permissions.READ 
        data = 'You are no longer an admin'
    
    message = Message(client=request.sock, sender=server.name,
                    data=data)

    args = {'client': client_to_promote, 'permssions': permissions, 'message': message}
    return server.change_client_permissions, args