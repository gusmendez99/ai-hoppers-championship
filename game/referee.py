from board import Board

class Referee:

    def __init__(self):

        self.prevSpots = []
        self.move_list = []


    def hop_search(self, row, col, board):
        row_offsets = [-1, 0, 1]
        col_offsets = [-1, 0, 1]
        jumps = []

        gameboard = Board()

        for row_offset in row_offsets:
            for col_offset in col_offsets:
                if (row + row_offset) >= len(board) or (col + col_offset) >= len(board):
                    continue
                if (row + row_offset) < 0 or (col + col_offset) < 0:
                    continue

                if (row + row_offset) == row and (col + col_offset) == col:
                    continue
                
                if ( board[row + row_offset][col + col_offset] != 0):
                    row_jump_offset = row + 2*row_offset
                    col_jump_offset = col + 2*col_offset

                    if (row_jump_offset) >= len(board) or (col_jump_offset) >= len(board):
                        continue
                    if (row_jump_offset) < 0 or (col_jump_offset) < 0:
                        continue
                
                    if(board[row + 2*row_offset][col+2*col_offset] == 0 and (row + 2*row_offset, col+2*col_offset) not in self.prevSpots):
                        
                        if(board[row][col] == 1 and (row,col) not in gameboard.redCorner):
                            if((row_jump_offset, col_jump_offset) in gameboard.redCorner):
                                continue
                    
                        if(board[row][col] == 2 and (row, col) not in gameboard.blueCorner):
                            if((row_jump_offset, col_jump_offset) in gameboard.blueCorner):
                                continue
                    
                        self.prevSpots.append((row, col))
                        jumps.append((row + 2*row_offset, col + 2*col_offset))
                        
                        future_hops = self.hop_search(row_jump_offset, col_jump_offset, board)

                        jumps.extend(future_hops)

                        self.move_list.extend(future_hops)

        return jumps

    
    def generate_legal_moves(self, row, col, board):
        gameboard = Board()

        if row >= len(board) or col >= len(board):
            print("That position is out of bounds")
            return

        if row < 0 or col < 0:
            print("That position is out of bounds")
            return
        
        if board[row][col] == 0:
            print("There isn't a piece there to move.")
            return
        
        row_offsets = [-1, 0, 1]
        col_offsets = [-1, 0, 1]

        legal_moves = []
        blocked_spaces = []

        for row_offset in row_offsets:
            for col_offset in col_offsets:

                if (row + row_offset) >= len(board) or (col + col_offset) >= len(board[0]):
                    continue
                
                if (row + row_offset) == row and (col + col_offset) == col:
                    continue
                
                if (row + row_offset) < 0 or (col + col_offset) < 0:
                    continue
                
                if (board[row + row_offset][col + col_offset] == 0): #means its empty
                    if (board[row][col] == 1 and (row, col) not in gameboard.redCorner):
                        if ((row + row_offset, col + col_offset) in gameboard.redCorner):
                            continue
                
                    if (board[row][col] == 2 and (row, col) not in gameboard.blueCorner):
                        if ((row + row_offset, col + col_offset) in gameboard.blueCorner):
                            continue

                    legal_moves.append((row + row_offset, col + col_offset))
                else:
                    blocked_spaces.append((row + row_offset, col + col_offset))
        
        legal_moves.extend(self.hop_search(row, col, board))

        self.move_list.extend(legal_moves)

        return legal_moves

    def clear_prev_spots(self):
        self.prevSpots = []