import logging
import os
import socket
import struct

from networking import config


# commands names
class Commands:
    EXIT = 'EXIT'
    BOUNCE = 'BOUNCE'
    GET = 'GET'


def setup_logging(debug):
    """ Setup server logging"""
    fmt = '%(message)s'
    loglevel = logging.INFO
    if debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format=fmt, level=loglevel)


def extract_command(data):
    """ Extracts and normalizes the command name from the data object"""
    return data.split(' ')[0].upper()


def extract_parameters(data):
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


def send_message(msg, connection):
    """ Encodes and sends message through the connection using our wire protocol
        length is sent first packed as an unsigned int, little-indian
        then the message
    """
    to_send = f'{msg}\r\n'.encode(config.DATA_ENCODING)
    connection.sendall(struct.pack(config.PACKING, len(to_send)))
    connection.sendall(to_send)


def send_file(filepath, connection):
    """ Sends a file through the connection using our wire protocol
        length is sent first packed as an unsigned int, little-indian
        then the message
    """

    # first send file size
    size = os.path.getsize(filepath)
    connection.sendall(struct.pack(config.PACKING, size))
    with open(filepath, 'rb') as f:
        connection.sendfile(f, 0)


def receive_size(connection):
    """ Receives the size of the message"""
    try:
        received = 0
        chunks = []

        # receive the first chunk and check if it is empty, if so, return size to 0
        chunk = connection.recv(config.LENGTH_BYTES)
        if chunk == b'':
            # received empty chunk return size = 0
            return 0

        received += len(chunk)
        chunks.append(chunk)

        while received < config.LENGTH_BYTES:
            chunk = connection.recv(config.LENGTH_BYTES - received)
            received += len(chunk)
            chunks.append(chunk)

        return struct.unpack(config.PACKING, b''.join(chunks))[0]
    except Exception as e:
        print(f'Could not receive size: {e}')
        return 0


def receive_message(connection, size):
    """ Receives and decodes data from server,
    if there are any decoding errors, ignore the data...
    """
    try:
        received = 0
        chunks = []
        chunk = connection.recv(min(size, config.MAX_BUFFER_SIZE))
        received += len(chunk)
        chunks.append(chunk)
        while received < size:
            chunk = connection.recv(min((size - config.MAX_BUFFER_SIZE), config.MAX_BUFFER_SIZE))
            received += len(chunk)
            chunks.append(chunk)

        try:
            msg = b''.join(chunks)
            msg = msg.decode(config.DATA_ENCODING)
            msg = msg.strip().rstrip('\r\n')
        except UnicodeDecodeError as e:
            print(e)
            msg = None
    except Exception as e:
        print(f'Could not receive message: {e}')
        msg = None

    return msg


def validate_ip(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False
