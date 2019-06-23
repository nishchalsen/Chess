
# Basic class
class Piece:
    def __init__(self, name, icon, colour, xpos, ypos):
        self.icon = icon
        self.name = name
        self.colour = colour
        self.xpos = xpos
        self.ypos = ypos

    def __repr__(self):
        return self.colour


class King(Piece):
    def __init__(self, colour):
        if colour == "white":
            super().__init__(name="king", icon=chr(9818), colour=colour, xpos=5, ypos=1)
        else:
            super().__init__(name="king", icon=chr(9812), colour=colour, xpos=5, ypos=8)

    def is_move_valid(self, before, after, board):
        if abs(after[1] - before[1]) + abs(after[0] - before[0]) == 1:
            return True
        elif abs(after[1] - before[1]) == abs(after[0] - before[0]) and abs(after[1] - before[1]) == 1 and abs(
                after[0] - before[0]) == 1:
            return True
        else:
            return False


class Queen(Piece):
    def __init__(self, colour, xpos, ypos):
        if colour == "white":
            super().__init__(name="queen", icon=chr(9819), colour=colour, xpos=xpos, ypos=ypos)
        else:
            super().__init__(name="queen", icon=chr(9813), colour=colour, xpos=xpos, ypos=ypos)

    def is_move_valid(self, before, after, board):
        # Rook and Bishop
        if abs(after[1] - before[1]) > 0 and abs(after[0] - before[0]) == 0 or abs(after[1] - before[1]) == 0 and abs(
                after[0] - before[0]) > 0:
            return is_collision(before, after, board, "rook")
        if abs(after[1] - before[1]) == abs(after[0] - before[0]):
            return is_collision(before, after, board, "bishop")
        else:
            return False


class Rook(Piece):
    def __init__(self, colour, xpos, ypos):
        if colour == "white":
            super().__init__(name="rook", icon=chr(9820), colour=colour, xpos=xpos, ypos=ypos)
        else:
            super().__init__(name="rook", icon=chr(9814), colour=colour, xpos=xpos, ypos=ypos)

    def is_move_valid(self, before, after, board):

        if abs(after[1] - before[1]) > 0 and abs(after[0] - before[0]) == 0 or abs(after[1] - before[1]) == 0 and abs(
                after[0] - before[0]) > 0:
            return is_collision(before, after, board, "rook")

        else:
            return False


class Bishop(Piece):
    def __init__(self, colour, xpos, ypos):
        if colour == "white":
            super().__init__(name="bishop", icon=chr(9821), colour=colour, xpos=xpos, ypos=ypos)
        else:
            super().__init__(name="bishop", icon=chr(9815), colour=colour, xpos=xpos, ypos=ypos)

    def is_move_valid(self, before, after, board):
        if abs(after[1] - before[1]) == abs(after[0] - before[0]):
            return is_collision(before, after, board, "bishop")
        else:
            return False


class Knight(Piece):
    def __init__(self, colour, xpos, ypos):
        if colour == "white":
            super().__init__(name="knight", icon=chr(9822), colour=colour, xpos=xpos, ypos=ypos)
        else:
            super().__init__(name="knight", icon=chr(9816), colour=colour, xpos=xpos, ypos=ypos)


    def is_move_valid(self, before, after, board):
        # Have to check that abs(x)  or abs(y) can not exceed 3
        if abs(after[1] - before[1]) == 2 and abs(after[0] - before[0]) == 1 or abs(after[1] - before[1]) == 1 and abs(after[0] - before[0]) == 2:
            return True
        else:
            return False


class Pawn(Piece):
    def __init__(self, colour, xpos, ypos):
        if colour == "white":
            super().__init__(name="pawn", icon=chr(9823), colour=colour, xpos=xpos, ypos=ypos)
        else:
            super().__init__(name="pawn", icon=chr(9817), colour=colour, xpos=xpos, ypos=ypos)
        self.start_x = xpos
        self.start_y = ypos

    def is_move_valid(self, before, after, board):
        if self.colour == "white":
            y = 1
        else:
            y = -1

        condition1 = abs(after[1] - before[1]) == abs(after[0] - before[0])  # check diagonal
        condition2 = abs(after[0] - before[0]) == 1  # check if the abs of x is 1
        condition3 = abs(after[1] - before[1])  # check y is negative or not

        if (after[0] - before[0] == y and after[1] - before[1] == 0) or (
                after[1] - before[1] == y and after[0] - before[0] == 0) and (board[after[1]][after[0]] == ""):
            return True
        elif condition1 and condition2 and condition3 == 1 and board[after[1]][after[0]] != "":
            return True

        elif before[0] == self.start_x and before[1] == self.start_y and abs(after[1] - before[1]) == 2 and abs(after[0] - before[0]) == 0:
            return is_collision(before, after, board, "pawn")

        else:
            return False


def is_collision(before, after, board, name):

    if name == "rook":

        if after[1] == before[1]:
            constant, dynamic = 1, 0
        else:
            constant, dynamic = 0, 1

        if after[dynamic] - before[dynamic] > 0:
            increment = 1
            before[dynamic] += increment
            check_boolean = before[dynamic] < after[dynamic]

        else:
            increment = -1
            before[dynamic] += increment
            check_boolean = before[dynamic] > after[dynamic]

        while check_boolean:
            if constant == 1:
                if not board[before[constant]][before[dynamic]] == "":
                    return False
            else:
                if not board[before[dynamic]][before[constant]] == "":
                    return False
            before[dynamic] += increment

            if increment == 1:
                check_boolean = before[dynamic] < after[dynamic]
            else:
                check_boolean = before[dynamic] > after[dynamic]
        else:
            return True

    elif name == "bishop":
        if after[0] - before[0] > 0:
            x_increment = 1
            before[0] += x_increment
            check_boolean_x = before[0] < after[0]
        else:
            x_increment = -1
            before[0] += x_increment
            check_boolean_x = before[0] > after[0]

        if after[1] - before[1] > 0:
            y_increment = 1
            before[1] += y_increment
            check_boolean_y = before[1] < after[1]
        else:
            y_increment = -1
            before[1] += y_increment
            check_boolean_y = before[1] > after[1]

        while check_boolean_x and check_boolean_y:
            if not board[before[1]][before[0]] == "":
                return False
            before[0] += x_increment
            before[1] += y_increment

            if x_increment == 1:
                check_boolean_x = before[0] < after[0]
            else:
                check_boolean_x = before[0] > after[0]

            if y_increment == 1:
                check_boolean_y = before[1] < after[1]
            else:
                check_boolean_y = before[1] > after[1]
        else:
            return True
    else:
        condition = abs(after[0] - before[0]) == 0
        condition = abs(after[0] - before[0]) == 1 and abs(after[1] - before[1]) == 1
        if after[1] - before[1] > 0:
            # if abs(after[0] - before[0]) == 1:
            #     # condition =
            y_increment = 1
        else:
            y_increment = -1

        before[1] += y_increment
        if not board[before[1]][before[0]] == "":
            return False
        else:
            return True


def create_pieces():
    chess_pieces = []

    w_king = King(colour="white")
    w_queen = Queen(colour="white", xpos=4, ypos=1)
    w_rook_l, w_rook_r = Rook(colour="white", xpos=1, ypos=1), Rook(colour="white", xpos=8, ypos=1)
    w_bishop_l, w_bishop_r = Bishop(colour="white", xpos=3, ypos=1), Bishop(colour="white", xpos=6, ypos=1)
    w_knight_l, w_knight_r = Knight(colour="white", xpos=2, ypos=1), Knight(colour="white", xpos=7, ypos=1)
    b_king = King(colour="black")
    b_queen = Queen(colour="black", xpos=4, ypos=8)
    b_rook_l, b_rook_r = Rook(colour="black", xpos=1, ypos=8), Rook(colour="black", xpos=8, ypos=8)
    b_bishop_l, b_bishop_r = Bishop(colour="black", xpos=3, ypos=8), Bishop(colour="black", xpos=6, ypos=8)
    b_knight_l, b_knight_r = Knight(colour="black", xpos=2, ypos=8), Knight(colour="black", xpos=7, ypos=8)

    chess_pieces.append(w_king)  # white king position 0
    chess_pieces.append(b_king)  # black king position 0

    chess_pieces += [w_queen, w_rook_l, w_rook_r, w_bishop_l, w_bishop_r, w_knight_l, w_knight_r,
                     b_queen, b_rook_l, b_rook_r, b_bishop_l, b_bishop_r, b_knight_l, b_knight_r]
    for i in range(1, 9):
        chess_pieces.append(Pawn(colour="white", xpos=i, ypos=2))
        chess_pieces.append(Pawn(colour="black", xpos=i, ypos=7))

    return chess_pieces
