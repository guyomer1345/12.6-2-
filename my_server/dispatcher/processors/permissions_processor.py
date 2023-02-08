'''
from client.chat_client import ChatClient
from typz import Permissions, Request
from server import Server



class PermissionsProcessor:
    def __init__(self, server: Server = None):
        self.server = server
    
    def set_server(self, server: Server):
        self.server = server
    
    def basic_admin_command_checks(self, client: ChatClient, request: Request) -> bool:
        passive_client = self.server.clients.get_client_by_name(request.passive_user)

        has_permissions = client.permissions == Permissions.ADMIN
        user_exists = passive_client in self.server.clients.clients
        isnt_self = client != passive_client

        return has_permissions and user_exists and isnt_self
    
    def basic_command_checks(self, client: ChatClient):
        pass
'''