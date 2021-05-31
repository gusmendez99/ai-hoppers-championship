import socket
import sys
import threading
import time
import utils
from settings import *
from ast import literal_eval as make_tuple

# TODO: import your minimax & board code, or you can overwrite the TODOs in @RobertoFigueroa lib module...
from hoppers.game.board import Board
from hoppers.game.minimax import Minimax
from hoppers.game.node import Node

EXIT_CODES = {
    SERVER_FULL: "Server is full! Try again later",
    GAME_END : "Thank you for playing!"
}

ERROR_CODES = {
    ILLEGAL_MOVE: "Opponent sent an illegal move, change turn!",
}
GAME_OVER = False

if len(sys.argv) != 3:
    print("usage: client.py <server-ip> <port>")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
if sys.argv[1] == "default":
    server_ip = SERVER_DEFAULT_IP

server_address = (server_ip, server_port)

# TODO: declare your board & your minimax bot
""" board = Board()
ai_bot = Minimax(TIME_LIMIT, True)
my_turn = None """

def display_game():
    # TODO: show your board
    # board.pp_board()

    a = 1 # TODO: comment this line when you have done the above task...

def game_thread():
    # this function handles display
    global GAME_OVER
    global my_turn
    global board
    while not GAME_OVER:
        response, _ = sock.recvfrom(BUFF_SIZE)

        # Parse bytes response to string
        response = response.decode()
        action, payload = response[0], response[1:]
        
        if action == REGISTER:
            # Payload: Player position, assigned by the server
            player_position = None
            if P1_POSITION == make_tuple(payload):
                player_position = P1_POSITION
            elif P2_POSITION == make_tuple(payload):
                player_position = P2_POSITION

            x, y = player_position
            print(f"Player assigned to: {x},{y}")

            # TODO: initialize your board, knowing which player (x,y) you were assigned by the server
            # my_turn = P1 if player_position == P1_POSITION else P2

            # TODO: start local game
            # board.init_pieces()

        elif action == NEW_MOVE:
            dict_move = utils.from_xml(payload)

            initial_row, initial_col = int(dict_move['from']['@row']), int(dict_move['from']['@col'])
            final_row, final_col = int(dict_move['to']['@row']), int(dict_move['to']['@col'])

            # Finally, we need to move the piece placed at initial position
            # You can use a namedtuple as Position = (x, y) if you manage your pieces in this way
            new_move = [
                (initial_row, initial_col), 
                (final_row, final_col)
            ]
            
            print(f"Move received: {initial_row},{initial_col} to {final_row},{final_col}")
            # TODO: process new move in your board & change turn
            """ board.move_piece(new_move[0], new_move[1])
            board.pp_board()
            board.change_turn() """


        elif action in EXIT_CODES:
            print(EXIT_CODES[response])
            GAME_OVER = True

        elif action in ERROR_CODES:
            print(ERROR_CODES[response])
            # TODO: change/omit opponent turn, and continue game
            """ board.change_turn() """

        else:
            print(action, payload)

def bot_thread():
    """
    This function handles bot response (moves)
    """
    # Server handshake
    handshake_message = HANDSHAKE
    sock.sendto(handshake_message.encode(), server_address)

    global GAME_OVER
    global my_turn
    global board
    while not GAME_OVER:
        if board.turn == my_turn:
            # Listen for Minimax or RL & MCTS Bot

            # TODO: Your own AI Implementation
            """ copy_board = Board()
            copy_board.set_board(board.get_board())
            root_node = Node(board.turn, copy_board, 3)
            print("AI thinking") """

            # TODO: await for Bot response to process its move
            """ return_node, best_move = ai_bot.alpha_beta_minimax(root_node)
            print("AI move  from {} to {}".format(best_move[0], best_move[1])) """
            
            move_dict = {
                'from': best_move[0],
                'to': best_move[1]
            }
            move = utils.to_xml(move_dict)
            sock.sendto(f"{NEW_MOVE}{move}".encode(), server_address)

            # TODO: move pieces and change turn
            """ print("Now I have sent a new move to server...")
            board.move_piece(best_move[0], best_move[1])
            board.change_turn() """
        

def start_game():
    # this function launches the game
    bot = threading.Thread(target=bot_thread)
    game = threading.Thread(target=game_thread)
    bot.daemon = True
    game.daemon = True
    bot.start()
    game.start()
    while not GAME_OVER:
        time.sleep(1)

def initialize():
    print(f"Connecting to Hoppers server on {server_ip}...")
    sock.connect(server_address)

initialize()
start_game()