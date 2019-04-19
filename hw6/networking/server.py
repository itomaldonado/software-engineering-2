import click
import logging
import os
import socket

from networking import config
from networking.utils import Commands
from networking.utils import extract_command
from networking.utils import extract_parameters
from networking.utils import send_message
from networking.utils import send_file
from networking.utils import receive_message
from networking.utils import receive_size
from networking.utils import setup_logging
from networking.utils import validate_ip

logger = logging.getLogger(__name__)

# server configuration:
SERVER_RUNNING = True


def handle_invalid(command, connection):
    """ Handle schenarios when the command sent was invalit"""
    msg = f'Invalid Command: {command}'
    logger.debug(msg)
    send_message(msg, connection)


def handle_exit(data, address, connection):
    """ Handle the EXIT command"""

    # get parameters and decide what code to use
    params = extract_parameters(data)
    code = params[0] if params else config.SERVER_DEFAULT_EXIT

    # log code, send goodbye message, and close connection
    logger.info(f'Closing connection to client, address: {address}, exit code: {code}')
    msg = f'Goodbye: {code}'
    send_message(msg, connection)
    connection.close()
    pass


def handle_get(data, connection):
    """ Handle the GET command"""
    # get parameters and decide what code to use
    params = extract_parameters(data)

    # handle when GET without file was sent
    if not params:
        msg = 'ERROR: no file provided'
        logger.debug(msg)
        send_message(msg, connection)
        return

    # hanlde when the file provided does not exist or is not a file
    filename = params[0]
    filepath = os.path.abspath(f'{config.SERVER_STATIC_DIR}/{filename}')
    logger.debug(f'Processed file name: {filename}')
    logger.debug(f'Processed file path: {filepath}')
    if not os.path.exists(filepath):
        msg = 'ERROR: no such file'
        logger.debug(msg)
        send_message(msg, connection)
        return
    elif not os.path.isfile(filepath):
        msg = 'ERROR: not a file'
        logger.debug(msg)
        send_message(msg, connection)
        return

    # send file using socket.sendfile
    # reference: https://docs.python.org/3/library/socket.html#socket.socket.sendfile
    logger.debug(f'Sending file: {filepath}')
    send_file(filepath, connection)


def handle_bounce(data, connection):
    """ Handle the BOUNCE command"""
    params = extract_parameters(data)
    msg = ' '.join(params)
    logger.debug(f'Sending data: {msg}')
    send_message(msg, connection)


@click.command()
@click.option('--debug', is_flag=True, help="Show debug data")
@click.option('--host', '-h', default='127.0.0.1', help='IP to bind.', type=str, show_default=True)
@click.option('--port', '-p', default=3000, help='Port to bind.', type=int, show_default=True)
def run(debug, host, port):

    # validate IP address
    if not validate_ip(host):
        logger.error('Invalid IP address')
        exit(1)

    # global server running
    global SERVER_RUNNING

    # setup logging
    setup_logging(debug)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            s.listen()
            logger.info(f'Server started, listening at: {host}:{port}')

            # infinite loop to wait for connections, until KeyboardInterrupt is received
            # KeyboardInterrupt = 'CTRL+C'
            while SERVER_RUNNING:
                # the accept() method blocks intil a connection is established
                connection, addr = s.accept()
                try:
                    with connection:
                        addr_str = f'{addr[0]}:{addr[1]}'
                        logger.info(f'Received connection from client, address: {addr_str}')

                        # wait for data until client sends 'EXIT'
                        while True:

                            # get the size of the next data interaction
                            size = receive_size(connection)
                            logger.debug(f'Next data size: {size}')

                            # client sent size 0 and ready to shutdown
                            if size == 0:
                                logger.info(f'Closing connection to client, address: {addr_str}')
                                break

                            # if there is data, decode it, remove any
                            # newline/carriage returns
                            data = receive_message(connection, size)
                            if not data:
                                logger.error('Client sent no data, closing connection.')
                                break

                            logger.debug(f'Message received: {data}')

                            # get the command sent
                            command = extract_command(data)

                            # EXIT command
                            if command in (Commands.EXIT,):
                                logger.debug('EXIT command received.')
                                handle_exit(data, addr_str, connection)
                                break

                            # GET command
                            elif command in (Commands.GET,):
                                logger.debug('GET command received.')
                                handle_get(data, connection)

                            # BOUNCE command
                            elif command in (Commands.BOUNCE,):
                                logger.debug('BOUNCE command received.')
                                handle_bounce(data, connection)

                            # All other commands are invalid
                            else:
                                logger.debug('Unknown command received.')
                                handle_invalid(command, connection)
                except ConnectionError as ce:
                    logger.error(f'There was a connection error: {ce}')
        except (KeyboardInterrupt, SystemExit):
            logger.info('\nServer stopped by KeyboardInterrupt or SystemExit.')
            SERVER_RUNNING = False
            s.close()
            exit(0)
        except Exception as e:
            SERVER_RUNNING = False
            logger.error(f'Something bad happened: {e}')
            raise
