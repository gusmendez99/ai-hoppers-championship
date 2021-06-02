import socket
import sys
import random
import numpy as np
import time
import utils
from settings import *
# Game
from hoppers.game.board import Board
from hoppers.game.referee import Referee

WINNER = False
TIME_EXP = False

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
        print("Waiting for new move from Player 1...")
        first_player_req, addr = sock.recvfrom(BUFF_SIZE)
        if addr not in board.players:
            sock.sendto(f"{SERVER_FULL}".encode(), addr)
            continue

        # Parse bytes response to string
        first_player_req = first_player_req.decode()
        action, payload = first_player_req[0], first_player_req[1:]
        
        # Validate player 1 & action
        if addr == board.players[0] and action == NEW_MOVE:
            dict_move = utils.from_xml(payload)

            initial_row, initial_col = int(dict_move['from']['@row']), int(dict_move['from']['@col'])
            final_row, final_col = int(dict_move['to']['@row']), int(dict_move['to']['@col'])

            # Finally, we need to move the piece placed at initial position
            new_move = [
                (initial_row, initial_col), 
                (final_row, final_col)
            ]

            print(f"Move received: {initial_row},{initial_col} to {final_row},{final_col}")
            legal_moves = referee.generate_legal_moves(new_move[0][0], new_move[0][1], board.get_board())
            print("Legal moves:", legal_moves)
            referee.clear_prev_spots()
            # TODO: modify move_piece() and return a bool if movement was performed successfully

            if new_move[1] in legal_moves:
                board.move_piece(new_move[0], new_move[1])
                # Send move to the opponent
                sock.sendto(f"{NEW_MOVE}{payload}".encode(), board.players[1])
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

        
        print("Waiting for new move from Player 2...")
        second_player_req, addr = sock.recvfrom(BUFF_SIZE)
        if addr not in board.players:
            sock.sendto(f"{SERVER_FULL}".encode(), addr)
            continue
        
        # Parse bytes response to string
        second_player_req = second_player_req.decode()
        action, payload = second_player_req[0], second_player_req[1:]
        
        # Validate player 2 & action
        if addr == board.players[1] and action == NEW_MOVE:
            dict_move = utils.from_xml(payload)

            initial_row, initial_col = int(dict_move['from']['@row']), int(dict_move['from']['@col'])
            final_row, final_col = int(dict_move['to']['@row']), int(dict_move['to']['@col'])

            # Finally, we need to move the piece placed at initial position
            new_move = [
                (initial_row, initial_col), 
                (final_row, final_col)
            ]


            print(f"Move received: {initial_row},{initial_col} to {final_row},{final_col}")
            legal_moves = referee.generate_legal_moves(new_move[0][0], new_move[0][1], board.get_board())
            print("Legal moves:", legal_moves)
            referee.clear_prev_spots()
            # TODO: modify move_piece() and return a bool if movement was performed successfully
            if new_move[1] in legal_moves:
                board.move_piece(new_move[0], new_move[1])
                # Send move to the opponent
                sock.sendto(f"{NEW_MOVE}{payload}".encode(), board.players[0])
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


