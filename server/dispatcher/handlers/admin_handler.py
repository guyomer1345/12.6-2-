from client.chat_client import ChatClient
from typz import Permissions


class AdminHandler:
    def __init__(self):
        pass

    def has_admin_permissions(self, client: ChatClient) -> bool:
        return client.permissions is Permissions.ADMIN
    
    