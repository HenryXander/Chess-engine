from chess.pieces import Pawn, Rook, Knight, Bishop, Queen, King
import pygame
import pickle
import os.path

class Board:
    def __init__(self):
        if os.path.isfile('initial_board_pickle'):
            with open('initial_board_pickle', 'rb') as file:
                self.board = pickle.load(file)
        else:
            self.board = self.__create_board()
            with open('initial_board_pickle', 'wb') as file:
                pickle.dump(self.board, file)

        self.square_size = 80  # Size of each square on the chessboard
        self.window_size = self.square_size * 8

        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Chess Board")

        self.colors = [pygame.Color(255, 206, 158), pygame.Color(209, 139, 71)]  # Light and dark squares

        if os.path.isfile('initial_blocking_map_pickle'):
            with open('initial_blocking_map_pickle', 'rb') as file:
                self.pieces_blocking_map = pickle.load(file)
        else:
            self.pieces_blocking_map = self.__initialize_blocking_map()
            with open('initial_blocking_map_pickle', 'wb') as file:
                pickle.dump(self.pieces_blocking_map, file)

        if os.path.isfile('initial_move_map_pickle'):
            with open('initial_move_map_pickle', 'rb') as file:
                self.pieces_move_map = pickle.load(file)
        else:
            self.pieces_move_map = self.__initialize_move_map()
            with open('initial_move_map_pickle', 'wb') as file:
                pickle.dump(self.pieces_move_map, file)
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
                    free_spots = self.open_up(piece)
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
        blocked_pieces = self.close_out_diag(piece)
        blocked_pieces += self.__close_out_hor(piece)
        blocked_pieces += self.__close_out_vert(piece)
        blocked_pieces += self.close_out_L(piece)
        return blocked_pieces

    def close_out_diag(self, piece):
        blocked_pieces = []
        blocked_pieces += self.__close_out_diagonal_down(piece)
        blocked_pieces += self.__close_out_diagonal_up(piece)
        return blocked_pieces
    def __close_out_diagonal_up(self, piece):
        blocked_pieces = []
        i, j = piece.position
        for k in range(1, min(7 - i, j) + 1):
            spot = self.board[i + k][j - k]
            if spot is not None:
                if isinstance(spot, Bishop) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        for k in range(1, min(i, 7 - j)):
            spot = self.board[i - k][j + k]
            if spot is not None:
                if isinstance(spot, Bishop) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        return blocked_pieces
    def __close_out_diagonal_down(self, piece):
        blocked_pieces = []
        i, j = piece.position
        for k in range(1, min(i, j) + 1):
            spot = self.board[i - k][j - k]
            if spot is not None:
                if isinstance(spot, Bishop) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        for k in range(1, min(8 - i, 8 - j)):
            spot = self.board[i + k][j + k]
            if spot is not None:
                if isinstance(spot, Bishop) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        return blocked_pieces

    def close_out_straight(self, piece):
        blocked_pieces = []
        blocked_pieces += self.__close_out_hor(piece)
        blocked_pieces += self.__close_out_vert(piece)
        return blocked_pieces
    def __close_out_hor(self, piece):
        blocked_pieces = []
        i, j = piece.position
        for k in range(1, j + 1):
            spot = self.board[i][j - k]
            if spot is not None:
                if isinstance(spot, Rook) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        for k in range(1, 8 - j):
            spot = self.board[i][j + k]
            if spot is not None:
                if isinstance(spot, Rook) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        return blocked_pieces
    def __close_out_vert(self, piece):
        blocked_pieces = []
        i, j = piece.position
        if piece.color == 'white':
            if i - 1 >= 0:
                spot = self.board[i - 1][j]
                if isinstance(spot, Pawn):
                    blocked_pieces.append(spot)
            if i - 2 >= 0:
                spot = self.board[i - 2][j]
                if isinstance(spot, Pawn):
                    if spot.first_move:
                        blocked_pieces.append(spot)
        else:
            if i + 1 < 8:
                spot = self.board[i + 1][j]
                if isinstance(spot, Pawn):
                    blocked_pieces.append(spot)
            if i + 2 < 8:
                spot = self.board[i + 2][j]
                if isinstance(spot, Pawn):
                    if spot.first_move:
                        blocked_pieces.append(spot)

        for k in range(1, i + 1):
            spot = self.board[i - k][j]
            if spot is not None:
                if isinstance(spot, Rook) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        for k in range(1, 8 - i):
            spot = self.board[i + k][j]
            if spot is not None:
                if isinstance(spot, Rook) or isinstance(spot, Queen):
                    blocked_pieces.append(spot)
                if k == 1 and isinstance(spot, King):
                    blocked_pieces.append(spot)
                break
        return blocked_pieces

    def close_out_L(self, piece):
        blocked_pieces = []
        i, j = piece.position
        spots = []

        if i >= 2 and j >= 2:
            spots += [
                self.board[i - 2][j - 1],
                self.board[i - 1][j - 2]
            ]
            if i + 1 < 8 and j + 1 < 8:
                spots += [
                    self.board[i - 2][j + 1],
                    self.board[i + 1][j - 2]
                ]
        else:
            if i >= 2:
                if j - 1 >= 0:
                    spots += [
                        self.board[i - 2][j - 1]
                    ]
                if j + 1 < 8:
                    spots += [
                        self.board[i - 2][j + 1]
                    ]
            if j >= 2:
                if i - 1 >= 0:
                    spots += [
                        self.board[i - 1][j - 2]
                    ]
                if i + 1 < 8:
                    spots += [
                        self.board[i + 1][j - 2]
                    ]

        if i + 2 < 8 and j + 2 < 8:
            spots += [
                self.board[i + 2][j + 1],
                self.board[i + 1][j + 2]
            ]
            if i - 1 >= 0 and j - 1 >= 0:
                spots += [
                    self.board[i + 2][j - 1],
                    self.board[i - 1][j + 2]
                ]
        else:
            if i + 2 < 8:
                if j + 1 < 8:
                    spots += [
                        self.board[i + 2][j + 1]
                    ]
                if j - 1 >= 0:
                    spots += [
                        self.board[i + 2][j - 1]
                ]
            if j + 2 < 8:
                if i + 1 < 8:
                    spots += [
                        self.board[i + 1][j + 2]
                    ]
                if i - 1 >= 0:
                    spots += [
                        self.board[i - 1][j + 2]
                    ]

        for spot in spots:
            if isinstance(spot, Knight):
                blocked_pieces.append(spot)
        return blocked_pieces


    def open_up(self, piece):
        free_spots = []
        if isinstance(piece, Bishop) or isinstance(piece, Queen):
            free_spots = self.open_up_diagonal(piece)
            if isinstance(piece, Queen):
                free_spots += self.open_up_straight(piece)
            return free_spots
        elif isinstance(piece, Rook) or isinstance(piece, Queen):
            free_spots = self.open_up_straight(piece)
            if isinstance(piece, Queen):
                free_spots += self.open_up_diagonal(piece)
            return free_spots
        elif isinstance(piece, Knight):
            free_spots = self.open_up_L(piece)
            return free_spots
        elif isinstance(piece, Pawn):
            free_spots = self.open_up_pawn(piece)
            return free_spots
        elif isinstance(piece, King):
            free_spots = self.open_up_king(piece)
            return free_spots
        return free_spots

    def open_up_diagonal(self, piece):
        free_spots = []
        free_spots += self.__open_up_diagonal_up(piece)
        free_spots += self.__open_up_diagonal_down(piece)
        return free_spots
    def __open_up_diagonal_up(self, piece):
        free_spots = []
        i, j = piece.position
        for k in range(1, min(7 - i, j) + 1):
            spot = self.board[i + k][j - k]
            if spot is None:
                free_spots.append((i + k, j - k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        for k in range(1, min(i, 7 - j)):
            spot = self.board[i - k][j + k]
            if spot is None:
                free_spots.append((i - k, j + k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        return free_spots
    def __open_up_diagonal_down(self, piece):
        free_spots = []
        i, j = piece.position
        for k in range(1, min(i, j) + 1):
            spot = self.board[i - k][j - k]
            if spot is None:
                free_spots.append((i - k, j - k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        for k in range(1, min(8 - i, 8 - j)):
            spot = self.board[i + k][j + k]
            if spot is None:
                free_spots.append((i + k, j + k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        return free_spots

    def open_up_straight(self, piece):
        free_spots = []
        free_spots += self.__open_up_hor(piece)
        free_spots += self.__open_up_vert(piece)
        return free_spots
    def __open_up_hor(self, piece):
        free_spots = []
        i, j = piece.position
        for k in range(1, j + 1):
            spot = self.board[i][j - k]
            if spot is None:
                free_spots.append((i, j - k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        for k in range(1, 8 - j):
            spot = self.board[i][j + k]
            if spot is None:
                free_spots.append((i, j + k))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        return free_spots
    def __open_up_vert(self, piece):
        free_spots = []
        i, j = piece.position
        for k in range(1, i + 1):
            spot = self.board[i - k][j]
            if spot is None:
                free_spots.append((i - k, j))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        for k in range(1, 8 - i):
            spot = self.board[i + k][j]
            if spot is None:
                free_spots.append((i + k, j))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
                break
        return free_spots

    def open_up_L(self, piece):
        free_spots = []
        i, j = piece.position
        if (i - 2) >= 0:
            if (j - 1) >= 0:
                spot = self.board[i - 2][j - 1]
                if spot is None:
                    free_spots.append((i - 2, j - 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            if (j + 1 < 8):
                spot = self.board[i - 2][j + 1]
                if spot is None:
                    free_spots.append((i - 2, j + 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        if (i - 1) >= 0:
            if (j - 2) >= 0:
                spot = self.board[i - 1][j - 2]
                if spot is None:
                    free_spots.append((i - 1, j - 2))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            if (j + 2 < 8):
                spot = self.board[i - 1][j + 2]
                if spot is None:
                    free_spots.append((i - 1, j + 2))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        if (i + 1) < 8:
            if (j - 2) >= 0:
                spot = self.board[i + 1][j - 2]
                if spot is None:
                    free_spots.append((i + 1, j + 2))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            if (j + 2 < 8):
                spot = self.board[i + 1][j + 2]
                if spot is None:
                    free_spots.append((i + 1, j + 2))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        if (i + 2) < 8:
            if (j - 1) >= 0:
                spot = self.board[i + 2][j - 1]
                if spot is None:
                    free_spots.append((i + 2, j - 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            if (j + 1 < 8):
                spot = self.board[i + 2][j + 1]
                if spot is None:
                    free_spots.append((i + 2, j + 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        return free_spots

    def open_up_pawn(self, piece):
        free_spots = []
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
                        self.pieces_blocking_map[spot].add(piece)
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
        else:
            spot = self.board[i - 1][j]
            if spot is None:
                free_spots.append((i - 1, j))
                if piece.first_move:
                    spot = self.board[i - 2][j]
                    if spot is None:
                        free_spots.append((i - 2, j))
                    if spot is not None:
                        self.pieces_blocking_map[spot].add(piece)
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
        return free_spots

    def open_up_king(self, piece):
        free_spots = []
        i, j = piece.position
        if i - 1 >= 0:
            if j - 1 >= 0:
                spot = self.board[i - 1][j - 1]
                if spot is None:
                    free_spots.append((i - 1, j - 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)

                spot = self.board[i][j - 1]
                if spot is None:
                    free_spots.append((i, j - 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            spot = self.board[i - 1][j]
            if spot is None:
                free_spots.append((i - 1, j))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
            if j + 1 < 8:
                spot = self.board[i - 1][j + 1]
                if spot is None:
                    free_spots.append((i - 1, j + 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
                spot = self.board[i][j + 1]
                if spot is None:
                    free_spots.append((i, j + 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        if i + 1 < 8:
            if j - 1 >= 0:
                spot = self.board[i + 1][j - 1]
                if spot is None:
                    free_spots.append((i + 1, j - 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
            spot = self.board[i + 1][j]
            if spot is None:
                free_spots.append((i + 1, j))
            if spot is not None:
                self.pieces_blocking_map[spot].add(piece)
            if j + 1 < 8:
                spot = self.board[i + 1][j + 1]
                if spot is None:
                    free_spots.append((i + 1, j + 1))
                if spot is not None:
                    self.pieces_blocking_map[spot].add(piece)
        return free_spots

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
            free_moves = self.open_up(impacted_piece)
            self.pieces_move_map[impacted_piece] = free_moves
            impacted_piece.set_legal_moves(free_moves)


    def get_piece(self, coords):
        return self.board[coords[0]][coords[1]]

    def update_legal_moves(self):
        for piece in self.pieces_move_map.keys():
            legal_moves = self.pieces_move_map[piece]
            piece.set_legal_moves(legal_moves)