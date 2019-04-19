import click
import logging
import socket

from networking import config
from networking.utils import Commands
from networking.utils import extract_command
from networking.utils import receive_message
from networking.utils import receive_size
from networking.utils import send_message
from networking.utils import setup_logging
from networking.utils import validate_ip

logger = logging.getLogger(__name__)

# server configuration:
CLIENT_RUNNING = True


def handle_help():
    """ Display the help menu"""
    logger.info('Commands you can enter are the following:')
    logger.info('HELP\t\t\tShows this menu.')
    logger.info(f'{Commands.GET} <file>\t\tGets specified file from the server.')
    logger.info(f'{Commands.BOUNCE} <msg>\t\tThe server echos the message back to the client.')
    logger.info(f'{Commands.EXIT} [<code>]\t\tClose connection and exit with provided code.')


def handle_bounce(data, connection):
    """ Handle the bounce command"""

    # first send
    logger.debug('Sending BOUNCE message to server.')
    send_message(data, connection)

    # now wait for resonse
    logger.debug('Awaiting response from server.')
    size = receive_size(connection)
    if size != 0:
        response = receive_message(connection, size)
        logger.info(response)
    else:
        logger.info('No data sent by server...')


def handle_get(data, connection):
    """ Handle the get command"""

    # first send
    logger.debug('Sending GET message to server.')
    send_message(data, connection)

    # now wait for resonse
    logger.debug('Awaiting response from server.')
    size = receive_size(connection)
    if size != 0:
        response = receive_message(connection, size)
        logger.info(response)
    else:
        logger.info('No data sent by server...')


def handle_exit(data, connection):
    """ Handle the exit command"""

    # first send
    logger.debug('Sending EXIT message to server.')
    send_message(data, connection)

    # now wait for resonse
    logger.debug('Awaiting response from server.')
    size = receive_size(connection)
    if size != 0:
        response = receive_message(connection, size)
        logger.info(response)
    else:
        logger.info('No data sent by server...')


@click.command()
@click.option('--debug', is_flag=True, help="Show debug data")
@click.option('--host', '-h', default='127.0.0.1', help='IP to bind.', type=str, show_default=True)
@click.option('--port', '-p', default=3000, help='Port to bind.', type=int, show_default=True)
def run(debug, host, port):

    # validate IP address
    if not validate_ip(host):
        logger.error('Invalid IP address')
        exit(1)

    # global running variable
    global CLIENT_RUNNING

    # setup logging
    setup_logging(debug)

    logger.debug(f'Command input. debug: {debug} - host: {host} - port: {port}')

    logger.debug(f'Connecting to server, address: {host}:{port}')

    # Create a socket object
    s = None
    try:
        s = socket.socket()
        s.connect((host, port))
        addr_str = f'{host}:{port}'
        logger.info(f'Connected to server: {addr_str}')
        logger.info('Please enter commands or type "HELP" for list of available commands')

        while CLIENT_RUNNING:
            input_raw = input(config.CLIENT_PROMPT_CHAR)

            # clean the command by stripping preceeding/trailing spaces
            # and removing any trailing newline/carriage returns
            logger.debug(f'Raw input: {input_raw}')
            input_processed = input_raw.strip().rstrip('\r\n')
            logger.debug(f'Processed input: {input_processed}')

            # if no command entered, continue
            if not input_processed:
                continue

            # get the command sent
            command = extract_command(input_processed)

            # HELP command:
            if command in ('HELP',):
                handle_help()
            elif command in (Commands.EXIT,):
                handle_exit(input_processed, s)
                s.close()
                CLIENT_RUNNING = False
            elif command in (Commands.GET,):
                handle_get(input_processed, s)
            elif command in (Commands.BOUNCE,):
                handle_bounce(input_processed, s)
            else:
                continue
    except (KeyboardInterrupt, SystemExit):
        logger.info('\nClient stopped by KeyboardInterrupt or SystemExit.')
        CLIENT_RUNNING = False
        if s:
            s.close()
    except Exception as e:
        logger.error(f'Something happened, closing: {e}')
        CLIENT_RUNNING = False
        if s:
            s.close()
        exit(1)
