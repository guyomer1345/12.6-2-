from typing import Callable, Dict, Tuple
from exceptions.exceptions import BadRequst, ValidationError
from typz import Message, Request
from typz import Commands
from server import Server
from dispatcher.processors import kick_processor, mute_processor,\
                                promote_processor, private_message_processor,\
                                send_all_processor, view_managers_processor, \
                                quit_processor, request_validator
import logging


def dispatch(server: Server, request: Request) -> Tuple[Callable, Dict[str, str]]:
    action, args = None, {}
    logging.debug(f'Request: {request}')
    client = server.clients.get_client_by_sock(request.sock)
    logging.info(f'Client: {client.name}, Permissions: {client.permissions}')

    try:
        request_validator(server, request)

        action, args = dispatcher_dict[request.cmd](server, request)

    except (ValidationError, BadRequst) as e:
        client = server.clients.get_client_by_sock(request.sock)
        message = Message(client.sock, sender=server.name, data=str(e))
        logging.info(f'{client.name}, {e}')
        
        args = {'clients': [client], 'message': message}
        action = server.add_messages_to_clients

    finally:
        return action, args

dispatcher_dict = {
    Commands.EXIT: quit_processor,
    Commands.KICK: kick_processor,
    Commands.MUTE: mute_processor,
    Commands.PRIVATE_MESSAGE: private_message_processor,
    Commands.PROMOTE: promote_processor,
    Commands.SEND_ALL: send_all_processor,
    Commands.VIEW_MANAGERS: view_managers_processor
    }