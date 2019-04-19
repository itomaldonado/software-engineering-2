"""
General configuration

These can be made configurable via environmental variables
"""
import os

# general config
PACKING = '<L'
LENGTH_BYTES = 4
DATA_ENCODING = 'utf-8'
TRANSFER_TIMEOUT = 5.0
MAX_BUFFER_SIZE = 4 * 1024
RETURN_KEY = '\xED\x1E\x94\x7C'


# server-specific config
SERVER_DEFAULT_EXIT = 200
SERVER_STATIC_DIR = os.path.abspath(f'{os.path.dirname(os.path.realpath(__file__))}/static')

# client-specific config
CLIENT_PROMPT_CHAR = '> '
