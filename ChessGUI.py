from tkinter import *
from tkinter import messagebox
from Chess_mechanic import Chess
from functools import partial


class Menu:
    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
        else:
            self.window = window
        self.window.title("Chess Game")
        self.window.geometry = "500*500"

        self.heading = Label(self.window, text="Welcome to my Chess Game", font=("Arial", 15))
        self.heading.grid(row=0, column=0, columnspan=5, pady=(5, 20))
        self.new_game = Button(self.window, text="Start a new game.", font=("Arial", 10), command=self.new_game)
        self.new_game.grid(row=1, column=2, pady=(1, 10))
        self.help = Button(self.window, text="Guide on how to play chess", font=("Arial", 10), command=self.help_function)
        self.help.grid(row=2, column=2, pady=(5, 20))
        self.exit = Button(self.window, text="Exit", font=("Arial", 10), command=self.window.destroy)
        self.exit.grid(row=3, column=2, pady=(1, 5))

        self.window.mainloop()

    def help_function(self):
        self.heading.destroy()
        self.new_game.destroy()
        self.help.destroy()
        self.exit.destroy()
        HelpWindow(self.window)

    def new_game(self):
        self.window.destroy()
        ChessGUI()



class HelpWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Help")
        self.heading = Label(self.window, text="Help", font=("Arial", 20))
        self.heading.grid(row=0, column=0, columnspan=100, pady=(5, 10))
        self.info = Label(self.window, font=("Arial", 10))
        self.info.grid()

        def get_text():
            file = open("help.txt", "r")
            help_text = ""
            for line in file.readlines():
                help_text += line + "\n"
            file.close()
            return help_text

        self.info.configure(text=get_text())

        self.exit_btn = Button(self.window, text="Go Back", font=("Arial", 15), command=self.menu_function)
        self.exit_btn.grid(row=3, column=0, pady=(1, 5))

        self.window.mainloop()

    def menu_function(self):
        self.heading.destroy()
        self.info.destroy()
        self.exit_btn.destroy()
        Menu(window=self.window)


class ChessGUI:

    def __init__(self):
        self.chess = Chess()
        self.window = Tk()
        self.window.title("My Chess game")
        self.window.geometry("750x800")
        self.chessboard_gui = [[]]
        self.temp_choice = []
        self.move = False
        self.alph_to_num = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}
        self.colour_choice = {"king": {"black": chr(9818), "white": chr(9812)},
                              "queen": {"black": chr(9819), "white": chr(9813)},
                              "rook": {"black": chr(9820), "white": chr(9814)},
                              "bishop": {"black": chr(9821), "white": chr(9815)},
                              "knight": {"black": chr(9822), "white": chr(9816)},
                              "pawn": {"black": chr(9823), "white": chr(9817)}}

        # Title text
        Label(self.window, text="Welcome to my chess game", font=("Arial", 10)).grid(column=1, columnspan=10, pady=5)

        # Creates Squares
        for i in list(range(1, 9))[::-1]:
            board = []
            num_list = Label(self.window, text=f"{9 - i}", borderwidth=10, bg="#E5DCDA", fg="#727070",
                             font=("Arial", 25))
            num_list.grid(row=i, column=0, padx=(30, 20))
            board.append(num_list)

            alph_column = Label(self.window, text=f" {self.alph_to_num[i]} ", bg="#E5DCDA", fg="#727070",
                                font=("Arial", 25))
            alph_column.grid(row=9, column=i, pady=5)
            if i % 2 == 1:
                colour = "White"
            else:
                colour = "#AC5E4D"

            for j in range(1, 9):
                btn = Button(self.window, text="    ", borderwidth=0, bg=colour, font=("Arial", 30), width=3, height=1,
                             command=partial(self.choose_or_move, [j, 9 - i]))
                btn.grid(row=i, column=j)
                board.append(btn)

                if colour == "White":
                    colour = "#AC5E4D"
                else:
                    colour = "White"

            self.chessboard_gui.append(board)

        # Adds all the chess pieces to the board
        for piece in self.chess.chess_pieces:
            self.chessboard_gui[9 - piece.ypos][piece.xpos].configure(text=piece.icon)

        # Display player
        self.display_player = Label(self.window, text="Player 1\n(White)", bg="#7EBCF4", fg="white", relief="raised",
                                    font=("Arial", 18))
        self.display_player.grid(column=0, row=10, rowspan=2, pady=(3, 5), padx=(10, 5))

        # Display Reset and Close button
        self.reset_btn = Button(self.window, text="Reset Game", font=("Arial", 9), command=self.restart_game)
        self.reset_btn.grid(column=8, row=10, pady=5)
        self.close_window = Button(self.window, text="Close Game", font=("Arial", 9), command=self.window.destroy)
        self.close_window.grid(column=8, row=11)

        self.window.mainloop()

    # Restart and Close the game
    def restart_game(self):
        self.window.destroy()
        ChessGUI()

    # I can only choose or only move
    def choose_or_move(self, pos):
        if not self.temp_choice == pos:
            if not self.chess.game_over:
                if not self.move:
                    self.valid_piece(pos)
                else:
                    self.valid_move(pos)
            else:
                if messagebox.askyesno("Game Over", "Game is already over.\nDo you want to play again?"):
                    self.restart_game()
        else:
            self.chessboard_gui[self.temp_choice[1]][self.temp_choice[0]].configure(fg="black")
            self.move = False
            self.temp_choice = []

    # Checks if you move this piece or not
    def valid_piece(self, pos):
        if self.chess.which_piece(pos):
            self.temp_choice = [pos[0], pos[1]]
            self.chessboard_gui[self.temp_choice[1]][self.temp_choice[0]].configure(fg="#FF4949")
            self.move = True
        else:
            if self.chess.which_player == 1:
                messagebox.showerror("Invalid Choice", "Invalid Choice, Please Choose a White Piece")
            else:
                messagebox.showerror("Invalid Choice", "Invalid Choice, Please Choose a Black Piece")

        # Is the move valid or not

    def valid_move(self, pos):
        self.chess.update_board()

        # Info: returns [boolean, player.name, player.colour] if True else [boolean]
        condition = self.chess.which_move(player_location=self.temp_choice, new_location=pos)
        if condition[0]:
            self.move = False

            self.chess.update_board()  # update inside the mechanics

            # Changes the UI
            self.chessboard_gui[self.temp_choice[1]][self.temp_choice[0]].configure(text=" ")
            self.chessboard_gui[pos[1]][pos[0]].configure(text=self.colour_choice[condition[1]][condition[2]])
            self.chessboard_gui[self.temp_choice[1]][self.temp_choice[0]].configure(fg="Black")

            # Checks if it is game over
            if self.chess.game_over:
                # Message to say that you have won
                if self.chess.player_1 == 1:
                    play_again = messagebox.askyesno("Congratulation",
                                                     "!!! Player 1 Wins !!!\nDo you want to play again?")
                else:
                    play_again = messagebox.askyesno("Congratulation",
                                                     "!!! Player 1 Wins !!!\nDo you want to play again?")
                if play_again:
                    pass
                    self.restart_game()

                return  # Stops instruction execution

            # Checks if it is check
            if self.chess.is_check():
                if self.chess.which_player == 1:
                    messagebox.showwarning("CHECK!", "Warning Black King is in danger!\nYou have been warned.")
                else:
                    messagebox.showwarning("CHECK!", "Warning White King is in danger!\nYou have been warned.")

            if self.chess.which_player == 1:
                self.display_player.configure(text="Player 2\n(Black)", fg="#616060")
                self.chess.which_player = 2
            else:
                self.chess.which_player = 1
                self.display_player.configure(text="Player 1\n(White)", fg="white")

        else:
            messagebox.showerror("Invalid Move", "This chess piece can't move there.")
