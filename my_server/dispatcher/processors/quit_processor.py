from typing import Callable, Dict, Tuple
from server import Server
from typz import Request


def quit_processor(server: Server, request: Request) -> Tuple[Callable, Dict[str, any]]:
    return server.disconnect, {'sock': request.sock}


