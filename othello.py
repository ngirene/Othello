# ICS 32 Spring 2013
# Lab 3 Project 5 Irene Ng 

black_piece = '['+u"\u25CF"+']'
white_piece = '['+u"\u25CB"+']'


class Othello:
    '''Represents a game of Othello.'''

    def __init__(self, row:int, col:int, player:str, disc:str, win:str)->None:
        '''Intialize an Othello game with a specified number of rows and number of columns.'''
        self.row = row
        self.col = col
        self.player = player
        self.disc = disc
        self.win = win

    def new_board(self)->[list]:
        '''Generates an empty board.'''
        board = []
        for i in range(self.col):
            board.append(["[ ]"]*self.row)
        return board
 
    def copy_board(self, board: [list]) -> [list]:
        '''Copies the board.'''
        board_copy = []

        for col in range(self.col):
            board_copy.append([])
            for row in range(self.row):
                board_copy[-1].append(board[col][row])

        return board_copy

    def opposite_player(self)->None:
        '''Alternates the players' turns.'''

        if self.player.upper() == "WHITE":
            self.player = "BLACK"
            
        elif self.player.upper() == "BLACK":
            self.player = "WHITE"
            

    def start(self)->[list]:
        '''Starts an Othello game.'''

        empty_board = self.new_board()
        board = self.copy_board(empty_board)
        center_col = int(self.col/2)-1
        center_row = int(self.row/2)-1

        if self.disc.upper() == "BLACK":
            board[center_col][center_row] = black_piece
            board[center_col+1][center_row] = white_piece
            board[center_col+1][center_row+1] = white_piece
            board[center_col][center_row+1] = black_piece
            
        if self.disc.upper() == "WHITE":
            board[center_col][center_row] = white_piece
            board[center_col+1][center_row] = black_piece
            board[center_col+1][center_row+1] = white_piece
            board[center_col][center_row+1] = black_piece

        return board
    
    def score_board(self, board:[list])->tuple:
        '''Displays the current scores.'''

        black_score = 0
        white_score = 0

        for row in range(self.row):
            for col in range(self.col):
                
                if board[col][row] == white_piece:
                    white_score+=1
                if board[col][row] == black_piece:
                    black_score+=1

        return (black_score, white_score)

    def is_valid_column_number(self, col: int) -> bool:
        '''Returns True if the given column number is valid.'''
        return 0 <= col < self.col

    def is_valid_row_number(self, row: int) -> bool:
        '''Returns True if the given row number is valid.'''
        return 0 <= row < self.row

    def require_valid_cell(self, col: int, row:int) -> bool:
        '''Raises a ValueError if its parameter is not a valid column number'''
        return self.is_valid_column_number(col) and self.is_valid_row_number(row)

    def neighbor(self, board:[list], col:int, row:int, direction:tuple)->bool:
        '''Returns the neighbor of the current cell; else, return False'''
        cell = board[col][row]
        x, y = direction
        neighbor = board[col+x][row+y]
        if self.require_valid_cell(col+x, row+y):
            return neighbor
        else:
            return False

        
    def valid_move(self, board:[list], col_to_check:int, row_to_check:int, player:str)->list:
        '''Checks for valid moves and returns a list of discs to be flipped if the move is valid
    else returns an empty list.'''
        
        flipping_discs = []
        eight_directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

        player, opponent = self.determine_opponent()

        if self.require_valid_cell(col_to_check,row_to_check):
            if board[col_to_check][row_to_check] == "[ ]":                
                for (x,y) in eight_directions:
                    col, row = col_to_check, row_to_check
                    col+=x
                    row+=y
                    if self.require_valid_cell(col, row) and board[col][row]==opponent:
                        col+=x
                        row+=y 
                        if not self.require_valid_cell(col, row):                            
                            continue                    
                        else:                            
                            while board[col][row]==opponent:
                                col+=x
                                row+=y
                                if not self.require_valid_cell(col,row):                                    
                                    break
                            if not self.require_valid_cell(col,row):                                
                                continue                        
                            if board[col][row] == player:
                                col-=x
                                row-=y                                
                                while board[col][row] == opponent:                                    
                                    flipping_discs.append((col,row))
                                    col-=x
                                    row-=y                              
                                    if col==col_to_check and row==row_to_check:
                                        break
        return flipping_discs

    def determine_opponent(self)->str:
        '''Return the player's piece and the corresponding opponent's piece'''
       
        if self.player.upper() == "BLACK":
            player = black_piece
            opponent = white_piece
            return (player, opponent)
        elif self.player.upper() == "WHITE":
            player = white_piece
            opponent = black_piece
            return (player, opponent)
    
    def make_move(self, board:[list], col:int, row:int, player:str)->bool:
        '''Returns true if a move is made; else, returns False and no move is made.'''
        flipping_discs = self.valid_move(board, col, row, player)
        if len(flipping_discs)!=0:
            if self.player.upper() == "WHITE":
                board[col][row] = white_piece
                for disc in flipping_discs:
                    (flip_col, flip_row) = disc
                    board[flip_col][flip_row] = white_piece

            elif self.player.upper() == "BLACK":
                board[col][row] = black_piece
                for disc in flipping_discs:
                    (flip_col, flip_row) = disc
                    board[flip_col][flip_row] = black_piece
            self.opposite_player()

            return True
        else:
            return False

    def moves_exist(self,board:[list], player:str)->bool:
        '''Returns True if the current player has any valid moves to make; else, return False.'''
        num_of_moves = 0
        for col in range(self.col):
            for row in range(self.row):
                if self.valid_move(board, col, row, self.player):
                    num_of_moves+=1
        if num_of_moves == 0:
            self.opposite_player()
        return num_of_moves != 0

    def winning_player(self, board:[list])->str:
        '''Determines how to win a game'''
        (black_score, white_score) = self.score_board(board)
        if black_score == white_score:
            tie = "TIE"
            return tie
        else:
            if self.win.upper() == "MOST":
                winner = max((black_score, white_score))
            
                if winner == black_score:
                    player = "BLACK"
                    return player
                elif winner == white_score:
                    player = "WHITE"
                    return player
            elif self.win.upper() == "LEAST":
                winner = min((black_score, white_score))
                if winner == black_score:
                    player = "BLACK"
                    return player
                elif winner == white_score:
                    player = "WHITE"
                    return player
    def full_board(self, board:[list])->bool:
        '''Returns True if the board is full'''
        free_cells = 0

        for row in range(self.row):
            for col in range(self.col):
                if board[col][row] == "[ ]":
                    free_cells+=1
        return free_cells == 0

    def valid_board(self, board:[list])->bool:
        '''Returns True if the board is still playable'''
        opponent_cells = 0
        player, opponent = self.determine_opponent()
        for row in range(self.row):
            for col in range(self.col):
                if board[col][row] == opponent:
                    opponent_cells += 1
        return opponent_cells != 0


                    

    
    
    
    
    
    



    
    
    
