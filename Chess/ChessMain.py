
import pygame as py
from Chess.ChessOffline import ChessEngine

FPS = 15
W = H = 512
DIMENTION = 8
SQ_SIZE = H//DIMENTION
IMAGES = {}

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


py.init()
screen = py.display.set_mode((W, H))
py.display.set_caption("Chess")
clock = py.time.Clock()
board_state = ChessEngine.GameState()


def load_images():
    images = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for image in images:
        IMAGES[image] = py.transform.scale(py.image.load('images/' + image + '.png'), (SQ_SIZE, SQ_SIZE))


def draw_board():
    colors = [py.Color('white'), py.Color('gray')]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = (r + c) % 2
            py.draw.rect(screen, colors[color], (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_peaces(peace_location):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            image = peace_location[r][c]
            if image != '--':
                screen.blit(IMAGES[image], py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    # py.image.save(screen, "save.png")             # Сохранить изображение экрана


load_images()
draw_board()
draw_peaces(board_state.board)
py.display.update()

list_moves = []
generate_moves = True
start_move = ()
selected_moves = []

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            location = py.mouse.get_pos()
            col = location[0] // SQ_SIZE
            row = location[1] // SQ_SIZE
            if start_move == (row, col):
                start_move = ()
                selected_moves = []
            else:
                start_move = (row, col)
                selected_moves.append(start_move)
            if len(selected_moves) == 2:
                move = ChessEngine.Move(selected_moves[0], selected_moves[1], board_state.board)
                print(move.get_chess_notation())
                if move in list_moves:
                    board_state.make_move(move)
                    generate_moves = True
                    start_move = ()
                    selected_moves = []
                else:
                    selected_moves = [start_move]
        elif event.type == py.KEYDOWN:
            if event.key == py.K_z:
                board_state.undo_move()
                generate_moves = True

    if generate_moves:
        list_moves = board_state.get_valid_moves()
        generate_moves = False

    draw_board()
    draw_peaces(board_state.board)
    py.display.update()
    clock.tick(FPS)

