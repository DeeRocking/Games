import pygame

from .board import Board
from .constants import RED, WHITE, DARK_BLUE, SQUARE_SIZE, SIDEBAR_WIDTH, BLACK, WIDTH, HEIGHT, WINNER_MEDAL


class Game:

    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_side_bar()
        self.draw_valid_moves(self.valid_moves)
        self.end_game_check()
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.turn = RED
        self.valid_moves = {}
        self.board = Board()

    def reset(self):
        self._init()

    def winner(self):
        return self.board.winner()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}

        if self.turn == RED:
            self.turn = DARK_BLUE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.rect(self.win, (127, 215, 127),
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_side_bar(self):
        padding = 10
        outline = 2
        y_shift = 30
        pygame.draw.rect(self.win, BLACK,
                         (WIDTH + padding, padding, SIDEBAR_WIDTH - 2 * padding, 3 * SQUARE_SIZE - padding))

        x = WIDTH + padding + (SIDEBAR_WIDTH - 2 * padding)//2
        y = (3 * SQUARE_SIZE - padding)//2 + y_shift
        radius = (SIDEBAR_WIDTH - 2 * padding)//4
        pygame.draw.circle(self.win, WHITE, (x, y), radius + outline)
        pygame.draw.circle(self.win, RED, (x, y), radius)

        font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 42)
        self.win.blit(font1.render("CAPTURED", True, "White"), (x-100, y - 150))
        font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 90)
        self.win.blit(font1.render(str(12 - self.board.red_left) ,True, "White"), (x-50, y- 65))


        pygame.draw.rect(self.win, BLACK,
                         (WIDTH + padding, HEIGHT - 3 * SQUARE_SIZE, SIDEBAR_WIDTH - 2 * padding, 3 * SQUARE_SIZE - padding))

        x = WIDTH + padding + (SIDEBAR_WIDTH - 2 * padding)//2
        y = HEIGHT - (3 * SQUARE_SIZE - padding)//2 + y_shift
        radius = (SIDEBAR_WIDTH - 2 * padding)//4
        pygame.draw.circle(self.win, WHITE, (x, y), radius + outline)
        pygame.draw.circle(self.win, DARK_BLUE, (x, y), radius)

        font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 42)
        self.win.blit(font1.render("CAPTURED", True, "White"), (x-100, y - 150))
        font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 90)
        self.win.blit(font1.render(str(12 - self.board.blue_left), True, "White"), (x - 50, y - 65))

    def draw_winner_window(self, winning_player):
        font1 = pygame.font.Font('SourceSansPro-Bold.ttf', 42)

        pygame.draw.rect(self.win, (31, 149, 31),(0, 0, WIDTH,HEIGHT))

        self.win.blit(WINNER_MEDAL,(WIDTH//2 - 150,HEIGHT//2 - 200))

        self.win.blit(font1.render(winning_player + ' PLAYER WON!', True,
                                   "White"), (WIDTH // 2 - 150, HEIGHT//2 + 100))

        self.win.blit(font1.render('r: Reset the Game', True,
                                   "White"), (0 + 30, HEIGHT - 50))
        self.win.blit(font1.render('q: Quit the Game', True,
                                   "White"), (WIDTH - 150, HEIGHT - 50))

    def end_game_check(self):
        winning_player = self.winner()
        if winning_player is not None:
            self.draw_winner_window(winning_player)

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()