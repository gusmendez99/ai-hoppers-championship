import socket
import sys
import threading
import time
import game.constants

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
    print("usage: client <PORT>")
    sys.exit()

def display_game():
    # this function handles displaying the game
    # TODO: add board local representation
    # board.print_status()

def display_thread():
    # this function handles display
    global GAME_OVER
    while not GAME_OVER:
        response, _ = sock.recvfrom(game.constants.BUFF_SIZE)
        # TODO: check if server response is a new move response
        if response[0] == game.constants.NEW_MOVE:
            # process new move
            # new_move = response[something]
            # board.process_move(new_move)
            display_game()

        elif response in EXIT_CODES:
            print(EXIT_CODES[response])
            GAME_OVER = True

        else:
            print(response)

def bot_thread():
    # this function handles bot input
    while not GAME_OVER:
        # listen for Minimax or RL & MCTS Bot
        # TODO: await for Bot response
        # new_move = await 
        # sock.sendto(new_move, server_address)

def start_game():
    # this function launches the game
    bot = threading.Thread(target=bot_thread)
    display = threading.Thread(target=display_thread)
    bot.daemon = True
    display.daemon = True
    bot.start()
    display.start()
    while not GAME_OVER:
        time.sleep(1)

def initialize():
    print("Connecting to Hoppers server on {}...".format(SERVER_ADDRESS))
    sock.sendto(game.constants.REGISTER, server_address)

initialize()
start_game()