from Pieces import create_pieces, Piece, Queen, Knight, Rook, Bishop
from tkinter import *
from functools import partial


# Fix pawn movement

class Chess:
    def __init__(self):
        self.which_player = 1
        self.player_1 = "black"
        self.player_2 = "white"
        self.state = False
        self.game_over = False
        self.killed_pieces = []
        self.chess_pieces = create_pieces()
        self.wait = True
        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.chessboard = [[],
                           [1, "", "", "", "", "", "", "", ""],
                           [2, "", "", "", "", "", "", "", ""],
                           [3, "", "", "", "", "", "", "", ""],
                           [4, "", "", "", "", "", "", "", ""],
                           [5, "", "", "", "", "", "", "", ""],
                           [6, "", "", "", "", "", "", "", ""],
                           [7, "", "", "", "", "", "", "", ""],
                           [8, "", "", "", "", "", "", "", ""],
                           ]
        # puts the object in the ar
        for piece in self.chess_pieces:
            self.chessboard[piece.ypos][piece.xpos] = piece

    def update_board(self):
        self.chessboard = [[],
                           [1, "", "", "", "", "", "", "", ""],
                           [2, "", "", "", "", "", "", "", ""],
                           [3, "", "", "", "", "", "", "", ""],
                           [4, "", "", "", "", "", "", "", ""],
                           [5, "", "", "", "", "", "", "", ""],
                           [6, "", "", "", "", "", "", "", ""],
                           [7, "", "", "", "", "", "", "", ""],
                           [8, "", "", "", "", "", "", "", ""],
                           ]
        for piece in self.chess_pieces:
            self.chessboard[piece.ypos][piece.xpos] = piece

    def which_piece(self, choice):  # fix
        if self.which_player == 1:
            player_colour = self.player_2
        else:
            player_colour = self.player_1

        piece = self.chessboard[choice[1]][choice[0]]

        if isinstance(piece, Piece) and player_colour == piece.colour:
            self.update_board()
            return True
        else:
            return False

    def which_move(self, player_location, new_location):

        player = self.chessboard[player_location[1]][player_location[0]]
        temp_pos = [player.xpos, player.ypos]

        obj_or_not = self.chessboard[new_location[1]][new_location[0]]
        if isinstance(obj_or_not, Piece) and obj_or_not.colour == player.colour:  # This is wrong
            return [False]

        if player.is_move_valid(before=temp_pos, after=new_location, board=self.chessboard):

            if isinstance(obj_or_not, Piece):
                # If it is king that is killed, Game over
                if obj_or_not.name == "king":
                    self.game_over = [True, player.name, player.colour]

                self.killed_pieces.append(obj_or_not.icon)
                self.chess_pieces.remove(obj_or_not)

            if player.name == "pawn":
                if player.colour == "white":
                    if new_location[1] == 8:

                        self.chess_pieces.append(Queen(colour="white", xpos=new_location[0], ypos=new_location[1]))
                        self.chess_pieces.remove(player)
                        self.update_board()
                        return [True, "queen", "white"]
                else:
                    if new_location[1] == 1:
                        self.chess_pieces.append(Queen(colour="black", xpos=new_location[0], ypos=new_location[1]))
                        self.chess_pieces.remove(player)
                        self.update_board()
                        return [True, "queen", "black"]

            player.xpos, player.ypos = new_location[0], new_location[1]  # update board
            self.update_board()
            return [True, player.name, player.colour]



        else:
            return [False]


    def is_check(self):
        if self.which_player == 1:
            king = self.chess_pieces[1]  # White King
            colour = "white"
        else:
            king = self.chess_pieces[0]  # Black King
            colour = "black"

        pieces_to_check = []
        for piece in self.chess_pieces:
            if piece.colour == colour:
                pieces_to_check.append(piece)

        for piece in pieces_to_check:
            after = [king.xpos, king.ypos]
            temp_pos = [piece.xpos, piece.ypos]

            if piece.is_move_valid(before=temp_pos, after=[int(after[0]), int(after[1])], board=self.chessboard):
                return True
            else:
                continue
