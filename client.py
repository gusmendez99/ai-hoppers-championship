import socket
import sys
import threading
import time
from settings import *
from ast import literal_eval as make_tuple

EXIT_CODES = {
    SERVER_FULL: "Server is full! Try again later",
    GAME_END : "Thank you for playing!"
}

ERROR_CODES = {
    ILLEGAL_MOVE: "Opponent sent an illegal move, change turn!",
}

SERVER_DEFAULT_IP = "127.0.0.1" 
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

# TODO: declare your board
# board = Board()

def display_game():
    # TODO: add board local representation
    # board.print()

    a = 1 # TODO: remove when you have done the above task...

def game_thread():
    # this function handles display
    global GAME_OVER
    while not GAME_OVER:
        response, _ = sock.recvfrom(BUFF_SIZE)

        # Parse bytes response to string
        response = response.decode()
        action, data = response[0], response[1:]
        
        if action == REGISTER:
            # Payload: Player position, assigned by the server
            player_position = None
            if P1_POSITION == make_tuple(data):
                player_position = P1_POSITION
            elif P2_POSITION == make_tuple(data):
                player_position = P2_POSITION

            x, y = player_position
            print("Player assigned to: {},{}".format(x, y))

            # TODO: initialize your board, knowing which player (x,y) you were assigned by the server
            """
            board.initialize()
            my_player = P1(Red) if player_position==P1_POSITION else P2(Blue)
            board.set_my_player(my_player)
            """

            # TODO: start local game
            # board.init_pieces()
            

        elif action in EXIT_CODES:
            print(EXIT_CODES[response])
            GAME_OVER = True

        elif action in ERROR_CODES:
            print(ERROR_CODES[response])
            # TODO: change/omit opponent turn, and continue game
            # board.change_turn()

        else:
            print(action, data)

def bot_thread():
    """
    This function handles bot response (moves)
    """
    handshake_message = "GG"
    sock.sendto(handshake_message.encode(), server_address)
    while not GAME_OVER:
        # Listen for Minimax or RL & MCTS Bot
        # TODO: await for Bot response
        """
        move = ai_agent.get_best_move(board)
        sock.sendto(f"{NEW_MOVE}{move}", server_address)
        """

        a = 1 # TODO: remove when you have done the above task...
        

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
    print("Connecting to Hoppers server on {}...".format(server_ip))
    sock.connect(server_address)

initialize()
start_game()