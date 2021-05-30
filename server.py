import socket
import sys
import random
import numpy as np
import time
from settings import *
# Game
from game.board import Board
from game.referee import Referee
from game.utils import get_coords

WINNER = False
TIME_EXP = False
SERVER_DEFAULT_IP = "127.0.0.1"

if len(sys.argv) <= 1:
    print("usage: server.py <port>")
    sys.exit()

board = Board()
board.init_pieces()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

    server_port = int(sys.argv[1])
    server_address = (SERVER_DEFAULT_IP, server_port)

    sock.bind(server_address)

    while len(board.players) < MAX_PLAYERS:
        print("Waiting for players ... ")
        conn, addr = sock.recvfrom(BUFF_SIZE)
        print("One player entered!")
        board.players.append(addr)

    print("Game ready!")
    referee = Referee()
    board.pp_board()

    # Turn will be choose as follow:
    #   The first one to be connected will have TURN 1 and placed at (0,0) [Red]
    #   The second one to be connected will have TURN 2, and placed at (9,9) [Blue]

    sock.sendto(f"{REGISTER}(0,0)".encode(), board.players[0])
    sock.sendto(f"{REGISTER}(9,9)".encode(), board.players[1])

    start = time.time()

    while not WINNER or not TIME_EXP:
        # TODO: make refactor, the two players do the same...
        # Start to receive moves
        first_player_req, addr = sock.recvfrom(BUFF_SIZE)
        if addr not in board.players:
            sock.sendto(f"{SERVER_FULL}".encode(), addr)
            continue

        # Parse bytes response to string
        first_player_req = first_player_req.decode()
        action, data = first_player_req[0], first_player_req[1:]
        
        # Validate player 1 & action
        if addr == board.players[0] and action == NEW_MOVE:
            print("Receiving coords from first player")
            coords = get_coords(first_player_req)
            legal_moves = referee.generate_legal_moves(coords[0][0], coords[0][1], board)
            # TODO: modify move_piece() and return a bool if movement was performed successfully
            if coords[1] in legal_moves:
                board.move_piece(coords[0], coords[1])
                # Send move to the opponent
                sock.sendto(f"{NEW_MOVE}{data}".encode(), board.players[1])
            else:
                print("Illegal move")
                # Send error to the opponent
                sock.sendto(f"{ILLEGAL_MOVE}".encode(), board.players[1])

            board.pp_board()
            winner = board.detect_win()
            if winner[0]:
                print("Player 1 wins")
                WINNER = True

            if winner[1]:
                print ("Player 2 wins")
                WINNER = True
            
            board.change_turn()

        
        second_player_req, addr = sock.recvfrom(BUFF_SIZE)
        if addr not in board.players:
            sock.sendto(f"{SERVER_FULL}".encode(), addr)
            continue

        # Parse bytes response to string
        second_player_req = second_player_req.decode()
        action, data = second_player_req[0], second_player_req[1:]
        
        # Validate player 2 & action
        if addr == board.players[1] and action == NEW_MOVE:
            print("Receiving coords from second player")
            coords = get_coords(second_player_req)
            legal_moves = referee.generate_legal_moves(coords[0][0], coords[0][1], board)
            # TODO: modify move_piece() and return a bool if movement was performed successfully
            if coords[1] in legal_moves:
                board.move_piece(coords[0], coords[1])
                # Send move to the opponent
                sock.sendto(f"{NEW_MOVE}{data}".encode(), board.players[0])
            else:
                print("Illegal move")
                # Send error to the opponent
                sock.sendto(f"{ILLEGAL_MOVE}".encode(), board.players[0])

            board.pp_board()
            winner = board.detect_win()
            if winner[0]:
                print("Player 1 wins")
                WINNER = True

            if winner[1]:
                print ("Player 2 wins")
                WINNER = True

            board.change_turn()

        #check time
        end = time.time()
        elapsed = end - start
        if elapsed >= TIME_LIMIT:
            TIME_EXP = True
            print("Time has expired")
    
    # Close connection
    sock.close()

    # Send game status to both players
    sock.sendto(f"{GAME_END}".encode(), board.players[0])
    sock.sendto(f"{GAME_END}".encode(), board.players[1])

    # If time has expired, we need to decide a winner based on best board
    print("[END] Time has expired, we need to choose a winner...")
    board.pp_board()


