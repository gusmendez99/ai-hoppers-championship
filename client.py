import socket
import sys
import threading
import time
import game.constants
from ast import literal_eval as make_tuple

EXIT_CODES = {
    game.constants.SERVER_FULL: "Server is full! Try again later",
    game.constants.GAME_END : "Thank you for playing!"
}

# TODO: set our AWS instance ip address as default
SERVER_ADDRESS = 'localhost' 
GAME_OVER = False

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_ADDRESS, int(sys.argv[1]))

if len(sys.argv) <= 1:
    print("usage: client.py <PORT>")
    sys.exit()

def display_game(board):
    # this function handles displaying the game
    # TODO: add board local representation
    print(board)

def game_thread():
    # this function handles display
    global GAME_OVER
    while not GAME_OVER:
        response, _ = sock.recvfrom(game.constants.BUFF_SIZE)

        # Parse response bytes to string
        response = response.decode()
        
        if response[0] == game.constants.MY_PLAYER_POSITION:
            # Payload: Player position, assigned by the server
            player_position = None
            if game.constants.P1_POSITION == make_tuple(response[1:]):
                player_position = game.constants.P1_POSITION
            elif game.constants.P2_POSITION == make_tuple(response[1:]):
                player_position = game.constants.P2_POSITION

            x, y = player_position
            print("Player assigned to: {},{}".format(x, y))

            # TODO: initialize your board, knowing which player (x,y) you were assigned by the server


            # TODO: start local game
            

        elif response[0] in EXIT_CODES:
            print(EXIT_CODES[response])
            GAME_OVER = True

        else:
            print(response)

def bot_thread():
    new_move = "GG"
    sock.sendto(new_move.encode(), server_address)
    # this function handles bot input
    while not GAME_OVER:
        # listen for Minimax or RL & MCTS Bot
        # TODO: await for Bot response
        # new_move = await
        a = 1 
        

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
    print("Connecting to Hoppers server on {}...".format(SERVER_ADDRESS))
    sock.connect(server_address)

initialize()
start_game()