
import numpy as np

class Board:

    BLUE = 2
    RED = 1
    EMPTY = 0

    def __init__(self, size=10):
        self.players = []
        self.max_players = 2
        self.size = size
        self.turn = 1
        self.board = np.full((self.size,self.size), self.EMPTY)
        self.blueCorner = []
        self.redCorner = []
        
        self.initPieces()
        self.getRedCorner(int(size/2))
        self.getBlueCorner(int(size/2))
        self.chosenMove = 0

    def changeTurn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def setTurn(self, turn):
        self.turn = turn

    def detectWin(self):
        blueWins = False
        redWins = False

        #check if all the tiles in blue corner are filled with red
        for coord in self.blueCorner:
            if self.get_piece_at(coord[0], coord[1]) == False or self.get_piece_at(coord[0],coord[1]) == 2:
                redWins = False
                break
            elif self.get_piece_at(coord[0], coord[1]) == 1:
                redWins = True
        for coord in self.redCorner:
            if self.get_piece_at(coord[0], coord[1]) == False or self.get_piece_at(coord[0], coord[1]) == 1:
                blueWins = False
                break
            elif self.get_piece_at(coord[0], coord[1]) == 2:
                blueWins = True

        return (redWins, blueWins)
    
    def get_piece_at(self, row, col):
        return self.board[row][col]


    def get_board(self):
        return self.board

    def initPieces(self):
        for i in range(5):
            self.board[i,:5-i] = self.RED
        for j in range(5,10):
            self.board[j,(5+9-j):10] = self.BLUE

    def getRedCorner(self, size):
        # points = np.where(self.board == self.RED)
        # for i in zip(points[0],points[1]):
        #     self.redCorner.append(i)
        for i in range(0, size):
            for j in range(0, size-i):
                self.redCorner.append((i,j))        

    
    def getBlueCorner(self, size):
        for i in range(0, size):
            cur_row = (size * 2) - (size -i)
            start_col = size * 2 - 1 - i
            end_col = size * 2
            for col in range(start_col, end_col):
                self.blueCorner.append((cur_row, col))


    def get_height(self):
        return self.size
    
    def get_width(self):
        return self.size
    
    def move_piece(self, start_pos, end_pos):
        player = self.remove_piece_at(start_pos[0], start_pos[1])
        self.place_piece(player, end_pos[0], end_pos[1])
    
    def remove_piece_at(self, row, col):
        player = self.board[row][col]
        self.board[row][col] = self.EMPTY
        return player

    def place_piece(self, player, row, col):
        self.board[row][col] = player

    def print_board(self):
        print(self.board)
    
    def get_red_positions(self):
        red_pos_list = []
        points = np.where(self.board == self.RED)
        for i in zip(points[0], points[1]):
            red_pos_list.append(i)
        return red_pos_list

    def get_blue_positions(self):
        blue_pos_list = []
        points = np.where(self.board == self.BLUE)
        for i in zip(points[0],points[1]):
            blue_pos_list.append(i)
        return blue_pos_list

    def set_board(self, new_board):
        self.board = np.copy(new_board)
    
    def pp_board(self, targets=[]):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 and (i,j) not in targets:
                    print('_', end='  ')
                if self.board[i][j] == 1 and (i,j) not in targets:
                    print('O', end='  ')
                if self.board[i][j] == 2 and (i,j) not in targets:
                    print('X', end='  ')
                if (i,j) in targets:
                    print('+', end='  ')
            
            print()
