from copy import deepcopy
import pygame

# ________________________________________________________ -GLOBAL CONSTANTS
RED = (255, 0, 0)
DARK_BLUE = (15, 5, 255)

# _______________________________________________________ - Main Algorithm function
def minimax(position, depth, max_player, game):
    """

    :param position: Current position of the player
    :param depth: Depth of the decision tree
    :param max_player: Boolean indicating if we want to maximize or minimize
    :param game: Instance of the game
    :return:
    """
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, DARK_BLUE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = float('+inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def get_all_moves(board, color, game):
    moves = []      # ___________ moves is as moves = [[board, piece], [new_board, piece]]
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():

            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.column)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    row, col = piece.row, piece.column
    pygame.draw.circle(game.win, (240, 0, 255),
                     (piece.x, piece.y), radius=50, width=5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()

    # pygame.time.delay(100)
