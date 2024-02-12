import pygame

from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, SIDEBAR_WIDTH, DARK_BLUE, RED
from checkers.game import Game
from minimax.algorithm import minimax


# ___________________________________________ PYGAME SETTINGS _________________________________________
pygame.init()
WIN = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
FPS = 60

# ___________________ Function to get the mouse position in the checker system__________________________________
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# ___________________________________________ PYGAME MAIN FUNCTION ___________________________________
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)


    while run:
        clock.tick(FPS)

        if game.turn == DARK_BLUE:
            value, new_board = minimax(game.get_board(), 3, DARK_BLUE, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_r:
                    game.reset()



        game.update()
    pygame.quit()


if __name__ == "__main__":
    main()
