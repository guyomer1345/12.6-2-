import logging
from client.chat_client import ChatClient
from exceptions.exceptions import BadRequst, NoPermissions, ValidationError
from typz import Commands, Permissions, Request, ADMIN_PREFIX
from server import Server


def request_validator(server: Server, request: Request):
    client = server.clients.get_client_by_name(request.username)
    if not client: # If client is None, its his first message
        validiate_new_client(server=server, request=request)
    
    if client:
        validate_request(server=server, request=request)

    

def validiate_new_client(server: Server, request: Request):
    client = server.clients.get_client_by_sock(sock=request.sock)    
    if ADMIN_PREFIX in request.username:
        raise ValidationError('Bad UserName')
    
    #Add more checks   

    permissions = Permissions.READ
    if server.clients.count_valid_clients() == 0:
        permissions = Permissions.ADMIN

    client.set_name(name=request.username)
    client.permissions = permissions
    server.broadcast_message(f'{client.get_name()} has joined the chat, say hey!')
    logging.info(f'Validated new client {client.name}')


def validate_request(server: Server, request: Request):
    client_by_sock = server.clients.get_client_by_sock(request.sock)
    client_by_name = server.clients.get_client_by_name(request.username)

    if client_by_sock != client_by_name:
        raise BadRequst("This isn't your username") 
    passive_user= request.passive_username
    pasive_client = server.clients.get_client_by_name(passive_user)

    if request.username == passive_user:
        raise BadRequst("Can't do things on yourself") 

    if passive_user and not pasive_client:
        raise BadRequst("User doesn't exist")

    client = client_by_sock
    cmd = request.cmd
    if cmd in [Commands.PROMOTE, Commands.MUTE, Commands.KICK]:
        if client.permissions != Permissions.ADMIN:
            raise NoPermissions('You need admin for that')
    
    if cmd in [Commands.SEND_ALL, Commands.PRIVATE_MESSAGE]:
        if client.permissions == Permissions.SEND:
            raise NoPermissions('You are muted')