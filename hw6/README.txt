Python Networking/Socket Example:


Requirements:
- Python 3.7+ (https://www.python.org/downloads/)
- pip (https://pip.pypa.io/en/stable/installing/)


Installation:
- Clone repository
- To install dependencies run: pip install -r requirements.txt


Server Usage: python server.py [OPTIONS]

Options:
  --debug             Show debug data
  -h, --host TEXT     IP to bind.  [default: 127.0.0.1]
  -p, --port INTEGER  Port to bind.  [default: 3000]
  --help              Show this message and exit.


Client Usage: python client.py [OPTIONS]

Options:
  --debug             Show debug data
  -h, --host TEXT     IP to bind.  [default: 127.0.0.1]
  -p, --port INTEGER  Port to bind.  [default: 3000]
  --help              Show this message and exit.


Example uses:

- Show server Help Menu: python ./server.py --help

- Show client Help Menu: python ./server.py --help

- Run server with defaults:
$ python server.py 
Server started, listening at: 127.0.0.1:3000

- Run client with defaults:
$ python client.py 
Connected to server: 127.0.0.1:3000
Please enter commands or type "HELP" for list of available commands
> 

- Client Help Menu:
- Run client with defaults:
$ python client.py 
Connected to server: 127.0.0.1:3000
Please enter commands or type "HELP" for list of available commands
> Help
Commands you can enter are the following:
HELP			Shows this menu.
GET <file>		Gets specified file from the server.
BOUNCE <msg>		The server echos the message back to the client.
EXIT [<code>]		Close connection and exit with provided code.
> 
