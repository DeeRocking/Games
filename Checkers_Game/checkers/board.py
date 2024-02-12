"""
Inside this module, the class controlling everything related to the board is defined.
"""

import pygame

from .constants import BLACK, ROWS,COLS,  RED, SQUARE_SIZE, WHITE, DARK_BLUE, DARK_RED, WIDTH, HEIGHT, WINNER_MEDAL
from .pieces import Piece



class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.blue_left = 12
        self.red_king = self.blue_king = 0

        self.create_board()

    def draw_squares(self, win):
        """ This method draws the squares of the chess board """
        win.fill(DARK_BLUE)
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == 0 and row % 2 == 0:
                    pygame.draw.rect(win, DARK_RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif  col % 2 == 0 and row % 2 == 1:
                    pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                elif col % 2 == 1 and row % 2 == 0:
                    pygame.draw.rect(win, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, DARK_RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def move(self, piece, row, col):
        self.board[piece.row][piece.column], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.column]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == DARK_BLUE:
                self.blue_king += 1
            else:
                self.red_king += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        """ This method  creates the chess board representation with all the pieces """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, DARK_BLUE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)

                else:
                    self.board[row].append(0)


    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.blue_left -= 1

    def evaluate(self):
        """ This method allows us to evaluate the board state in order to
        feed the AI. It's the main figure of merit.
        """
        return self.blue_left - self.red_left + (self.blue_king * 0.5 - self.red_king * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces


    def winner(self):
        if self.red_left <= 0:
            return 'BLUE'
        elif self.blue_left <= 0:
            return 'RED'
        else:
            return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column -1
        right = piece.column + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(
                row-1, max(row-3, -1), -1, piece.color, left
            ))
            moves.update(self._traverse_right(
                row-1, max(row-3, -1), -1, piece.color, right
            ))
        if piece.color == DARK_BLUE or piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row + 3, ROWS), +1, piece.color, left
            ))
            moves.update(self._traverse_right(
                row + 1, min(row + 3, ROWS), +1, piece.color, right
            ))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped:list = []):

        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = skipped + last
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(r+step, row, step, color, left-1, skipped=last)
                    )
                    moves.update(
                        self._traverse_right(r+step, row, step, color, left+1, skipped=last)
                    )
                break

            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1


        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped:list = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = skipped + last
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(r + step, row, step, color, right - 1, skipped=last)
                    )
                    moves.update(
                        self._traverse_right(r + step, row, step, color, right + 1, skipped=last)
                    )
                break

            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves


    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

