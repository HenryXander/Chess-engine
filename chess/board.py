from chess.pieces import Pawn, Rook, Knight, Bishop, Queen, King
import pygame
import os.path

class Board:
    def __init__(self):
        self.board = self.__create_board()

        self.square_size = 80  # Size of each square on the chessboard
        self.window_size = self.square_size * 8

        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Chess Board")

        self.colors = [pygame.Color(255, 206, 158), pygame.Color(209, 139, 71)]  # Light and dark squares
        self.pieces_blocking_map = self.__initialize_blocking_map()
        self.pieces_move_map = self.__initialize_move_map()
        self.update_legal_moves()

    def __create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        self.__setup_pieces(board)
        return board
    def __setup_pieces(self, board):
        # Initialize pawns
        for i in range(8):
            board[1][i] = Pawn('white', (1, i))
            board[6][i] = Pawn('black', (6, i))

        # Initialize other pieces
        placement = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(placement):
            board[0][i] = piece('white', (0, i))
            board[7][i] = piece('black', (7, i))

    def __initialize_blocking_map(self):
        map = {}
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    blocked_pieces = self.close_out(piece)
                    map[piece] = set(blocked_pieces)
        return map
    def __initialize_move_map(self):
        map = {}
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    result = self.get_free_spots_and_blocking(piece)
                    free_spots = result[0]
                    map[piece] = free_spots
        return map

    def __draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(self.window, color,
                                 pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                             self.square_size))
                piece = self.board[row][col]
                if piece:
                    self.__draw_piece(piece, col, row)
    def __draw_piece(self, piece, col, row):
        # You need to add images for each piece (e.g., "white_pawn.png", "black_queen.png", etc.)
        piece_image = pygame.image.load(f'chess\images\{piece.color}_{piece.__class__.__name__.lower()}.png')
        piece_image = pygame.transform.scale(piece_image, (self.square_size, self.square_size))
        self.window.blit(piece_image, (col * self.square_size, row * self.square_size))
    def display(self):
        self.__draw_board()

    def close_out(self, piece):
        (free_spots, blocking_pieces) = self.__get_free_spots_and_blocking_DIAGONAL(piece)
        result = self.__get_free_spots_and_blocking_STRAIGHT(piece)
        blocking_pieces += result[1]
        result = self.__get_free_spots_and_blocking_L(piece)
        blocking_pieces += result[1]
        return blocking_pieces

    def get_free_spots_and_blocking(self, piece):
        if isinstance(piece, Bishop) or isinstance(piece, Queen):
            (free_spots, blocking_pieces) = self.__get_free_spots_and_blocking_DIAGONAL(piece)
            if isinstance(piece, Queen):
                result = self.__get_free_spots_and_blocking_STRAIGHT(piece)
                free_spots += result[0]
                blocking_pieces += result[1]
            return (free_spots, blocking_pieces)
        elif isinstance(piece, Rook) or isinstance(piece, Queen):
            (free_spots, blocking_pieces) = self.__get_free_spots_and_blocking_STRAIGHT(piece)
            if isinstance(piece, Queen):
                result = self.__get_free_spots_and_blocking_DIAGONAL(piece)
                free_spots += result[0]
                blocking_pieces += result[1]
            return (free_spots, blocking_pieces)
        elif isinstance(piece, Knight):
            return self.__get_free_spots_and_blocking_L(piece)
        elif isinstance(piece, Pawn):
            return self.__get_free_spots_and_blocking_Pawn(piece)
        elif isinstance(piece, King):
            return self.__get_free_spots_and_blocking_King(piece)
        else:
            print("No valid piece")
            return None

    def __get_free_spots_and_blocking_DIAGONAL(self, piece):
        free_spots = []
        blocking_pieces = []
        i, j = piece.position
        #diagonal UP /
        for k in range(1, min(7 - i, j) + 1):
            spot = self.board[i + k][j - k]
            if spot is None:
                free_spots.append((i + k, j - k))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        for k in range(1, min(i, 7 - j)):
            spot = self.board[i - k][j + k]
            if spot is None:
                free_spots.append((i - k, j + k))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        #diagonal DOWN \
        for k in range(1, min(i, j) + 1):
            spot = self.board[i - k][j - k]
            if spot is None:
                free_spots.append((i - k, j - k))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        for k in range(1, min(8 - i, 8 - j)):
            spot = self.board[i + k][j + k]
            if spot is None:
                free_spots.append((i + k, j + k))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        return (free_spots, blocking_pieces)

    def __get_free_spots_and_blocking_STRAIGHT(self, piece):
        free_spots = []
        blocking_pieces = []
        i, j = piece.position
        #straight horizontal
        for k in range(1, j + 1):
            spot = self.board[i][j - k]
            if spot is None:
                free_spots.append((i, j - k))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        for k in range(1, 8 - j):
            spot = self.board[i][j + k]
            if spot is None:
                free_spots.append((i, j + k))
            if spot is not None:
                blocking_pieces.append(spot)
                break

        #straight vertical
        for k in range(1, i + 1):
            spot = self.board[i - k][j]
            if spot is None:
                free_spots.append((i - k, j))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        for k in range(1, 8 - i):
            spot = self.board[i + k][j]
            if spot is None:
                free_spots.append((i + k, j))
            if spot is not None:
                blocking_pieces.append(spot)
                break
        return (free_spots, blocking_pieces)

    def __get_free_spots_and_blocking_L(self, piece):
        free_spots = []
        blocking_pieces = []
        i, j = piece.position
        if (i - 2) >= 0:
            if (j - 1) >= 0:
                spot = self.board[i - 2][j - 1]
                if spot is None:
                    free_spots.append((i - 2, j - 1))
                if spot is not None:
                    blocking_pieces.append(spot)
            if (j + 1 < 8):
                spot = self.board[i - 2][j + 1]
                if spot is None:
                    free_spots.append((i - 2, j + 1))
                if spot is not None:
                    blocking_pieces.append(spot)
        if (i - 1) >= 0:
            if (j - 2) >= 0:
                spot = self.board[i - 1][j - 2]
                if spot is None:
                    free_spots.append((i - 1, j - 2))
                if spot is not None:
                    blocking_pieces.append(spot)
            if (j + 2 < 8):
                spot = self.board[i - 1][j + 2]
                if spot is None:
                    free_spots.append((i - 1, j + 2))
                if spot is not None:
                    blocking_pieces.append(spot)
        if (i + 1) < 8:
            if (j - 2) >= 0:
                spot = self.board[i + 1][j - 2]
                if spot is None:
                    free_spots.append((i + 1, j + 2))
                if spot is not None:
                    blocking_pieces.append(spot)
            if (j + 2 < 8):
                spot = self.board[i + 1][j + 2]
                if spot is None:
                    free_spots.append((i + 1, j + 2))
                if spot is not None:
                    blocking_pieces.append(spot)
        if (i + 2) < 8:
            if (j - 1) >= 0:
                spot = self.board[i + 2][j - 1]
                if spot is None:
                    free_spots.append((i + 2, j - 1))
                if spot is not None:
                    blocking_pieces.append(spot)
            if (j + 1 < 8):
                spot = self.board[i + 2][j + 1]
                if spot is None:
                    free_spots.append((i + 2, j + 1))
                if spot is not None:
                    blocking_pieces.append(spot)
        return (free_spots, blocking_pieces)

    def __get_free_spots_and_blocking_Pawn(self, piece):
        free_spots = []
        blocking_pieces = []
        i, j = piece.position
        if piece.color == 'white':
            spot = self.board[i + 1][j]
            if spot is None:
                free_spots.append((i + 1, j))
                if piece.first_move:
                    spot = self.board[i + 2][j]
                    if spot is None:
                        free_spots.append((i + 2, j))
                    if spot is not None:
                        blocking_pieces.append(spot)
            if spot is not None:
                blocking_pieces.append(spot)
        else:
            spot = self.board[i - 1][j]
            if spot is None:
                free_spots.append((i - 1, j))
                if piece.first_move:
                    spot = self.board[i - 2][j]
                    if spot is None:
                        free_spots.append((i - 2, j))
                    if spot is not None:
                        blocking_pieces.append(spot)
            if spot is not None:
                blocking_pieces.append(spot)
        return (free_spots, blocking_pieces)

    def __get_free_spots_and_blocking_King(self, piece):
        free_spots = []
        blocking_pieces = []
        i, j = piece.position
        if i - 1 >= 0:
            if j - 1 >= 0:
                spot = self.board[i - 1][j - 1]
                if spot is None:
                    free_spots.append((i - 1, j - 1))
                if spot is not None:
                    blocking_pieces.append(spot)

                spot = self.board[i][j - 1]
                if spot is None:
                    free_spots.append((i, j - 1))
                if spot is not None:
                    blocking_pieces.append(spot)
            spot = self.board[i - 1][j]
            if spot is None:
                free_spots.append((i - 1, j))
            if spot is not None:
                blocking_pieces.append(spot)
            if j + 1 < 8:
                spot = self.board[i - 1][j + 1]
                if spot is None:
                    free_spots.append((i - 1, j + 1))
                if spot is not None:
                    blocking_pieces.append(spot)
                spot = self.board[i][j + 1]
                if spot is None:
                    free_spots.append((i, j + 1))
                if spot is not None:
                    blocking_pieces.append(spot)
        if i + 1 < 8:
            if j - 1 >= 0:
                spot = self.board[i + 1][j - 1]
                if spot is None:
                    free_spots.append((i + 1, j - 1))
                if spot is not None:
                    blocking_pieces.append(spot)
            spot = self.board[i + 1][j]
            if spot is None:
                free_spots.append((i + 1, j))
            if spot is not None:
                blocking_pieces.append(spot)
            if j + 1 < 8:
                spot = self.board[i + 1][j + 1]
                if spot is None:
                    free_spots.append((i + 1, j + 1))
                if spot is not None:
                    blocking_pieces.append(spot)
        return (free_spots, blocking_pieces)




    def process_move(self, player, move):
        piece = move["piece"]
        new_spot = move["to_spot"]
        i, j = piece.position

        old_pieces_blocked_by_piece = self.pieces_blocking_map[piece]

        self.board[i][j] = None
        self.board[new_spot[0]][new_spot[1]] = piece
        piece.update_position(new_spot)

        new_pieces_blocked_by_piece = self.close_out(piece)
        all_impacted_pieces = old_pieces_blocked_by_piece.union(set(new_pieces_blocked_by_piece))
        self.pieces_blocking_map[piece] = set(new_pieces_blocked_by_piece)
        for impacted_piece in all_impacted_pieces:
            (free_spots, blocking_pieces) = self.get_free_spots_and_blocking(piece)
            for blocking_piece in blocking_pieces:
                self.pieces_blocking_map[blocking_piece].add(piece)
            self.pieces_move_map[impacted_piece] = free_spots
            impacted_piece.set_legal_moves(free_spots)

    def get_piece(self, coords):
        return self.board[coords[0]][coords[1]]

    def update_legal_moves(self):
        for piece in self.pieces_move_map.keys():
            legal_moves = self.pieces_move_map[piece]
            piece.set_legal_moves(legal_moves)