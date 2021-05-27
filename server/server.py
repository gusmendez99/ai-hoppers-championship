import socket
import sys
import random
import numpy as np
import time

from board import Board
from referee import Referee
from utils import getCoords

TURN_ERROR = "It isn't your turn right now."
INPUT_ERROR = "Invalid input: %s. Try again."
WAIT_MSG = "Awaiting players... (%s/%s).\n"
MAX_PLAYERS = 2
BUFF_SIZE = 4096
WINNER = False
TIME_LIMIT = 900 #for 15 mins
TIME_EXP = False

if len(sys.argv) <= 1:
    print("<PORT NUMBER> not defined")
    sys.exit()

board = Board()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    server_address = ('localhost', int(sys.argv[1]))

    sock.bind(server_address)

    sock.listen(3)

    while len(board.players) < MAX_PLAYERS:
        print("Waiting for players ... ")
        conn, addr = sock.accept()
        print("One player entered!")
        board.players.append(addr) #ponerle algo mas bonito como add player

    print("Game ready!")
    board = Board()
    referee = Referee()
    board.pp_board()

    #turno will be choose as follow:
    #   the first one to be connected will go first and goes in the buttom corner
    #   te second one to be connected will go second and goes in the up corner

    #send XML with init Game message an started positions
    sock.sendto("StartPos:(0,0)", board.players[0])
    sock.sendto("StartPos:(10,10)", board.players[1])

    start = time.time()

    while not WINNER or not TIME_EXP:
        #start to recieve moves
        print("Recieving coords from first player")
        first_player_req = sock.recv(BUFF_SIZE) #this method could be recvfrom for check the address of the player
        coords = getCoords(first_player_req)
        legal_moves = referee.generate_legal_moves(coords[0][0], coords[0][1], board)
        if coords[1] in legal_moves:
            board.move_piece(coords[0], coords[1]) #also here we need to check either there is a for the user in that start position
        else:
            print("Illegal move") # TODO: handle illegal moves : may be just pass the turn

        board.pp_board()

        winner = board.detectWin()
        if winner[0]:
            print("First player wins")
            WINNER = True

        if winner[1]:
            print ("Second player wins")
            WINNER = True

        
        print("Recieving coords from second player")
        second_player_req = sock.recv(BUFF_SIZE) #this method could be recvfrom for check the address of the player
        coords = getCoords(second_player_req)
        legal_moves = referee.generate_legal_moves(coords[0][0], coords[0][1], board)
        if coords[1] in legal_moves:
            board.move_piece(coords[0], coords[1]) #also here we need to check either there is a for the user in that start position
        else:
            print("Illegal move") # TODO: handle illegal moves : may be just pass the turn

        board.pp_board()


        winner = board.detectWin()
        if winner[0]:
            print("First player wins")
            WINNER = True

        if winner[1]:
            print ("Second player wins")
            WINNER = True

        #check time
        end = time.time()
        elapsed = end - start
        if elapsed >= TIME_LIMIT:
            TIME_EXP = True
            print("Time has expired")
            sock.close()

    sock.close()

