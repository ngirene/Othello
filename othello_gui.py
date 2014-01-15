# Lab 3 Project 5 Irene Ng 95413809

import tkinter
import othello

DEFAULT_FONT = ('Helvetica', 18)

class OthelloApplication:
    '''Represents an Othello graphical board'''

    def __init__(self, state:othello.Othello):
        '''Initializes an Othello application'''

        self.state = state

        self.board = state.start()

        self.root_window = tkinter.Tk()
        self.root_window.title("Othello")

        self.canvas = tkinter.Canvas(
            master = self.root_window, width=500, height=500, background = "#808080")

        self.canvas.grid(
            row = 1, column = 0, columnspan=2, padx=10, pady=10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self.canvas.bind("<Configure>", self.on_canvas_resized)
        self.canvas.bind("<Button-1>", self.on_canvas_clicked)

        self.root_window.rowconfigure(0, weight=1)
        self.root_window.rowconfigure(1, weight=2)
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.columnconfigure(1, weight=2)

    def start(self)->None:
        '''Starts a Othello game in a GUI.'''
        self.root_window.mainloop()

    def on_canvas_clicked(self, event:tkinter.Event)->None:
        '''Makes a move on the canvas when mouse is clicked'''

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
    
        vertical = width/self.state.col
        horizontal = height/self.state.row

        col, row = (int(event.x//vertical), int(event.y//horizontal))

        if not self.state.full_board(self.board) and self.state.valid_board(self.board):
            
            if self.state.moves_exist(self.board, self.state.player):
                
                if self.state.make_move(self.board, col, row, self.state.player):
                    
                    self.redraw_board()
                else:
                    self.player.set("Invalid Move! TURN: {}! Please click!".format(self.state.player.upper()))
                    
      
    def on_canvas_resized(self, event:tkinter.Event)->None:
        '''Resizes the canvas.'''

        self.redraw_board()

    def redraw_board(self)->None:
        '''Redraws the canvas'''

        self.canvas.delete(tkinter.ALL)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        black_score, white_score = self.state.score_board(self.board)

        for row in range(self.state.row):
            for col in range(self.state.col):
                
                vertical = canvas_width/self.state.col
                horizontal = canvas_height/self.state.row
                start = col*vertical
                end = row*horizontal
                    
                if self.board[col][row] == "[ ]":
                    self.canvas.create_rectangle(
                        start,end, start+vertical, end+horizontal)

                elif self.board[col][row] == "[●]":
                    self.canvas.create_rectangle(
                        start,end, start+vertical, end+horizontal)
                    self.canvas.create_oval(
                        start, end, start+vertical, end+horizontal, fill="#000000")
                       
                elif self.board[col][row] == "[○]":
                    self.canvas.create_rectangle(
                        start,end, start+vertical, end+horizontal)
                    self.canvas.create_oval(
                        start, end, start+vertical, end+horizontal, fill="#ffffff")

        self.player = tkinter.StringVar()

        player_label = tkinter.Label(
            self.root_window, textvariable = self.player,
            font = DEFAULT_FONT, relief='ridge', width=50)

        player_label.grid(
            row=0, column=0,
            sticky=tkinter.W+tkinter.E)
        
        self.player.set("TURN: {}! Please click!".format(self.state.player.upper()))

        self.white_score = tkinter.StringVar()

        white_score_label = tkinter.Label(
            self.root_window, textvariable = self.white_score,
            font = DEFAULT_FONT, width=10)

        white_score_label.grid(
            row=2, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.white_score.set("WHITE: {}".format(white_score))

        self.black_score = tkinter.StringVar()

        black_score_label = tkinter.Label(
            self.root_window, textvariable = self.black_score,
            font=DEFAULT_FONT, width=10)

        black_score_label.grid(
            row=2, column=1, padx=10, pady=10,
            sticky=tkinter.E)

        self.black_score.set("BLACK: {}".format(black_score))

        if not self.state.moves_exist(self.board, self.state.player):
            if self.state.player.upper() == "BLACK":
                self.player.set("WHITE passes! TURN: {}! Please click!".format(self.state.player.upper()))
            elif self.state.player.upper() == "WHITE":
                self.player.set("BLACK passes! TURN: {}! Pleas click!".format(self.state.player.upper()))

        if self.state.full_board(self.board):
            self.player.set("Game Over! Winner: {}!".format(self.state.winning_player(self.board)))
        elif not self.state.valid_board(self.board):
            self.player.set("Game Over! Winner: {}!".format(self.state.winning_player(self.board)))
        elif not self.state.moves_exist(self.board, 'BLACK') and not self.state.moves_exist(self.board, "WHITE"):
            self.player.set("Game Over! Winner: {}!".format(self.state.winning_player(self.board)))
  
class OthelloSetup:
    '''Represents the initial game setup of an Othello game'''
    
    def __init__(self):
        '''Initializes the set up for the Othello game'''
        
        self.dialog_window = tkinter.Tk()
        self.dialog_window.title("Set up your Othello game!")

        welcome_label = tkinter.Label(
            self.dialog_window,
            text = "Welcome players! Let's set up a game of Othello!",
            font = DEFAULT_FONT)

        welcome_label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        row_label = tkinter.Label(
            self.dialog_window,
            text="How many rows (even integer between 4 and 16 inclusive)?",
            font = DEFAULT_FONT)

        row_label.grid(
            row=1, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.row_label_entry = tkinter.Entry(
            self.dialog_window, width=3, font = DEFAULT_FONT)

        self.row_label_entry.grid(
            row=1, column=1, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        column_label = tkinter.Label(
            self.dialog_window,
            text="How many columns (even integer between 4 and 16 inclusive)?",
            font = DEFAULT_FONT)

        column_label.grid(
            row=2, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.column_label_entry = tkinter.Entry(
            self.dialog_window, width=3, font = DEFAULT_FONT)

        self.column_label_entry.grid(
            row=2, column=1, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        first_player_label = tkinter.Label(
            self.dialog_window,
            text="Will [BLACK] or [WHITE] go first?",
            font=DEFAULT_FONT)

        first_player_label.grid(
            row=3, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.first_player_label_entry = tkinter.Entry(
            self.dialog_window, width=6, font = DEFAULT_FONT)

        self.first_player_label_entry.grid(
            row=3, column=1, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        center_disc_label = tkinter.Label(
            self.dialog_window,
            text = "[BLACK] or [WHITE] in the top-left center cell?",
            font=DEFAULT_FONT)

        center_disc_label.grid(
            row=4, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.center_disc_label_entry = tkinter.Entry(
            self.dialog_window, width=6, font=DEFAULT_FONT)

        self.center_disc_label_entry.grid(
            row=4, column=1, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        winner_label = tkinter.Label(
            self.dialog_window,
            text = "Will [MOST] amount of discs or [LEAST] amount of discs win?",
            font=DEFAULT_FONT)

        winner_label.grid(
            row=5, column=0, padx=10, pady=10,
            sticky=tkinter.W)

        self.winner_label_entry = tkinter.Entry(
            self.dialog_window, width=6, font=DEFAULT_FONT)

        self.winner_label_entry.grid(
            row=5, column=1, padx=10, pady=10,
            sticky=tkinter.W+tkinter.E)

        self.button_frame = tkinter.Frame(self.dialog_window)

        self.button_frame.grid(
            row=6, column=0, columnspan=2, padx=10, pady=10,
            sticky=tkinter.E+tkinter.S)

        ok_button = tkinter.Button(
            self.button_frame, text = "OK", font=DEFAULT_FONT,
            command = self.on_ok)
        
        ok_button.grid(row = 0, column = 1, padx = 10)

        self.dialog_window.rowconfigure(3, weight = 1)

        self.dialog_window.columnconfigure(1, weight = 1)

        self.ok_clicked = False

        self.row = 0
        self.col = 0
        self.player = ''
        self.disc = ''
        self.win = ''

    def was_ok_clicked(self)->bool:
        '''Returns True if the OK button is clicked'''
        return self.ok_clicked

    def on_ok(self)->None:
        '''Determines what happens when the OK button is clicked'''

        self.ok_clicked = True
        self.row = int(self.row_label_entry.get())
        self.col = int(self.column_label_entry.get())
        self.player = self.first_player_label_entry.get()
        self.disc = self.center_disc_label_entry.get()
        self.win = self.winner_label_entry.get()

        invalid_row = not 4<=self.row<=16 or self.row%2!=0
        invalid_col = not 4<=self.col<=16 or self.col%2!=0
        invalid_player = not self.player.upper()=="BLACK" and not self.player.upper()=="WHITE"
        invalid_disc = not self.disc.upper() == "BLACK" and not self.disc.upper() == "WHITE"
        invalid_win = not self.win.upper() == "MOST" and not self.win.upper() == "LEAST"

        input_validity = [invalid_row, invalid_col, invalid_player, invalid_disc, invalid_win]
        
        if True in input_validity:
            invalid = tkinter.Toplevel()
            invalid.title("Error")

            msg = tkinter.Message(invalid, text="Invalid input! Try again.", font=DEFAULT_FONT)
            msg.pack()
            
            button = tkinter.Button(invalid, text="Close", command=invalid.destroy)
            button.pack()
        else:
            self.dialog_window.destroy()

            game = othello.Othello(self.row, self.col, self.player, self.disc, self.win)
            app = OthelloApplication(game)
            app.start()
                            
if __name__ == "__main__":
    setup = OthelloSetup()

    
    

    
    
    
    
        
        
        
