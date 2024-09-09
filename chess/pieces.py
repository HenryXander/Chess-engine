class Piece:
    def __init__(self, color, pos):
        self.color = color
        self.position = pos

    def __str__(self):
        return self.symbol()

    def symbol(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update_position(self, new_pos):
        self.position = new_pos


class Pawn(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.first_move = True
        self.legal_moves = []

    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def first_move_done(self):
        self.first_move = False

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

class Rook(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.legal_moves = []


    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

class Knight(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.legal_moves = []

    def symbol(self):
        return 'N' if self.color == 'white' else 'n'



    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

class Bishop(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.legal_moves = []

    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

class Queen(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.legal_moves = []

    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves

class King(Piece):
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self.legal_moves = []

    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def get_legal_moves(self):
        return self.legal_moves

    def set_legal_moves(self, legal_moves):
        self.legal_moves = legal_moves