import click
import logging
import os
import socket

logger = logging.getLogger(__name__)

# server configuration:
DATA_ENCODING = 'utf-8'
MAX_BUFFER_SIZE = 1024
DEFAULT_EXIT = 200
SERVER_STATIC_DIR = os.path.abspath(f'{os.path.dirname(os.path.realpath(__file__))}/static')
SERVER_RUNNING = True


# commands names:
class Commands:
    EXIT = 'EXIT',
    BOUNCE = 'BOUNCE',
    GET = 'GET'


def handle_invalid(command, connection):
    """ Handle schenarios when the command sent was invalit"""
    msg = f'Invalid Command: {command}'
    logger.debug(msg)
    _send_message(msg, connection)


def handle_exit(data, address, connection):
    """ Handle the EXIT command"""

    # get parameters and decide what code to use
    params = _extract_parameters(data)
    code = params[0] if params else DEFAULT_EXIT

    # log code, send goodbye message, and close connection
    logger.info(f'Closing connection to client, address: {address}, exit code: {code}')
    msg = f'Goodbye: {code}'
    _send_message(msg, connection)
    connection.close()
    pass


def handle_get(data, connection):
    """ Handle the GET command"""
    # get parameters and decide what code to use
    params = _extract_parameters(data)

    # handle when GET without file was sent
    if not params:
        msg = 'ERROR: no file provided'
        logger.debug(msg)
        _send_message(msg, connection)
        return

    # hanlde when the file provided does not exist or is not a file
    filename = params[0]
    filepath = os.path.abspath(f'{SERVER_STATIC_DIR}/{filename}')
    logger.debug(f'Processed file name: {filename}')
    logger.debug(f'Processed file path: {filepath}')
    if not os.path.exists(filepath):
        msg = 'ERROR: no such file'
        logger.debug(msg)
        _send_message(msg, connection)
        return
    elif not os.path.isfile(filepath):
        msg = 'ERROR: not a file'
        logger.debug(msg)
        _send_message(msg, connection)
        return

    # send file using socket.sendfile
    # reference: https://docs.python.org/3/library/socket.html#socket.socket.sendfile
    logger.debug(f'Sending file: {filepath}')
    with open(filepath, 'rb') as f:
        connection.sendfile(f, 0)

    # send a final 'new line'
    _send_message('', connection)


def handle_bounce(data, connection):
    """ Handle the BOUNCE command"""
    params = _extract_parameters(data)
    msg = ' '.join(params)
    _send_message(msg, connection)


def _extract_parameters(data):
    """ Extracts command parameters from the data object"""

    # tokenize the data object by splitting it by spaces
    params = data.split(' ')

    if len(params) == 1:
        # return empty list since we assume that the command was sent
        # without any parameters
        params = []
    else:
        # slice the parameters to remove the first entry
        # since we assume that this is the command
        params = params[1:]

    return params


def _extract_command(data):
    """ Extracts and normalizes the command from the data object"""
    return data.split(' ')[0].upper()


def _send_message(msg, connection):
    """ Encodes and sends message through the connection"""
    connection.sendall(f'{msg}\n'.encode(DATA_ENCODING))


def _setup_logging(debug):
    """ Setup server logging"""
    fmt = '%(message)s'
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format=fmt, level=loglevel)


@click.command()
@click.option('--debug', is_flag=True, help="Show debug data")
@click.option('--host', '-h', default='127.0.0.1', help='IP to bind.', type=str, show_default=True)
@click.option('--port', '-p', default=3000, help='Port to bind.', type=int, show_default=True)
def run(debug, host, port):

    # global server running
    global SERVER_RUNNING

    # setup logging
    _setup_logging(debug)

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
                with connection:
                    addr_str = f'{addr[0]}:{addr[1]}'
                    logger.info(f'Received connection from client, address: {addr_str}')

                    # wait for data until client sends 'EXIT'
                    while True:
                        data = connection.recv(MAX_BUFFER_SIZE)
                        logger.debug(f'Raw data received: {data}')

                        # if there is data, decode it, remove any
                        # newline/carriage returns
                        try:
                            data = data.decode(DATA_ENCODING)
                        except UnicodeDecodeError:
                            logger.error('Could not decode data sent, closing connection.')
                            break

                        data = data.rstrip('\r\n')
                        logger.debug(f'Processed data: {data}')

                        # no data, continue listening
                        if not data:
                            continue

                        # get the command sent
                        command = _extract_command(data)

                        # EXIT command
                        if command.startswith(Commands.EXIT):
                            logger.debug('EXIT command received.')
                            handle_exit(data, addr_str, connection)
                            break

                        # GET command
                        elif command.startswith(Commands.GET):
                            logger.debug('GET command received.')
                            handle_get(data, connection)

                        # BOUNCE command
                        elif command.startswith(Commands.BOUNCE):
                            logger.debug('BOUNCE command received.')
                            handle_bounce(data, connection)

                        # All other commands are invalid
                        else:
                            logger.debug('Unknown command received.')
                            handle_invalid(command, connection)
        except (KeyboardInterrupt, SystemExit):
            logger.info('\nServer stopped by KeyboardInterrupt or SystemExit.')
            SERVER_RUNNING = False
            s.close()
        except Exception as e:
            logger.error(f'Something bad happened: {e}')
            raise


if __name__ == '__main__':
    run()
