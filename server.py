import socket
import sys
import random

from numpy import True_

from board import Board
from referee import Referee

TURN_ERROR = "It isn't your turn right now."
INPUT_ERROR = "Invalid input: %s. Try again."
WAIT_MSG = "Awaiting players... (%s/%s).\n"
MAX_PLAYERS = 2

if len(sys.argv) <= 1:
    print("<PORT NUMBER> not defined")
    sys.exit()

board = Board()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)}

server_address = ('localhost', int(sys.argv[1]))

sock.bind(server_address)

sock.listen(5)

while len(board.players) < MAX_PLAYERS:
    print("Waiting for players ... ")
    conexion, addr = sock.accept()
    print("One player entered!")
    board.players.append(conexion) #ponerle algo mas bonito como add player

print("Game ready!")

for player in board.players:
    #send XML with init Game message



