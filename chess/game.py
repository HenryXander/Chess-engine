from chess.board import Board
import pygame
import sys

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'

    def play(self):
        pygame.init()
        running = True
        self.board.display()
        pygame.display.flip()
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not self.is_game_over():
                self.handle_turn()
            self.board.display()
            pygame.display.flip()
        pygame.quit()
        sys.exit()



    def choose_piece(self):
        piece = None
        while piece is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        board_coords = (mouse_pos[1] // 80, mouse_pos[0] // 80)
                        temp_piece = self.board.get_piece(board_coords)
                        if temp_piece is not None:
                            if temp_piece.color == self.current_turn:
                                print(temp_piece.get_legal_moves())
                                if temp_piece.get_legal_moves() == []:
                                    print('choose other piece')
                                else:
                                    piece = temp_piece
                            else:
                                print('not your piece')
        print(f"chosen piece: {piece}")
        return piece

    def choose_move_spot(self, piece):
        piece_moves = piece.get_legal_moves()
        print('legal_moves: {}'.format(piece_moves))

        for legal_move in piece_moves:
            (row, col) = legal_move
            legal_spot_image = pygame.image.load(f'chess\images\legal_move_spot.png')
            legal_spot_image = pygame.transform.scale(legal_spot_image, (self.board.square_size, self.board.square_size))
            self.board.window.blit(legal_spot_image, (col * self.board.square_size, row * self.board.square_size))
        pygame.display.flip()

        move = None
        while move is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        board_coords = (mouse_pos[1] // 80, mouse_pos[0] // 80)
                        if board_coords in piece_moves:
                            move = board_coords
                        else:
                            print('not a legal move')
        return move

    def handle_turn(self):
        piece = self.choose_piece()
        move_spot = self.choose_move_spot(piece)

        move = {"piece" : piece,
                "to_spot" : move_spot
                }

        self.make_move(move)
        self.switch_turn()

    def make_move(self, move):
        # Placeholder for making a move
        self.board.process_move(self.current_turn, move)

    def switch_turn(self):
        self.current_turn = 'white' if self.current_turn == 'black' else 'black'

    def is_game_over(self):
        # Placeholder for game over logic
        return False



