import logging
from dispatcher.dispatcher import dispatch
from server import Server
import argparse

logging.basicConfig(level=logging.INFO)

def main(): 
    parser = argparse.ArgumentParser(description='Enter ip, port for the server to run on')
    parser.add_argument('ip', metavar='ip', type=str,
                    help='The ip the server will run on')
    parser.add_argument('port', metavar='port', type=int,
                    help='The port the server will run on')    
    args = parser.parse_args()
    ip, port = args.ip, args.port

    server = Server(ip=ip, port=port)
    server.run_server()
    while server.is_running:          
        r_list, w_list, x_list = server.get_lists()
        server.process_x_list(x_list=x_list)
        server.process_w_list(w_list=w_list)
        server.process_r_list(dispatcher=dispatch, r_list=r_list)
    
if __name__ == '__main__':
    main()