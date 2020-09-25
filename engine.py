import pygame as pg
from settings import *
import sys


def terminate():
    pg.quit()
    sys.exit()


def wait_for_player_to_press_key():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    terminate()
                return
            if event.type == pg.MOUSEBUTTONUP:
                return


class Board:

    def __init__(self, board=None):
        if board is not None:
            self.board_cells = board.board_cells.copy()
        else:
            self.board_cells = []
        self.cell_image = pg.image.load('images/cell.png')
        self.cell_O_image = pg.image.load('images/cellO.png')
        self.cell_X_image = pg.image.load('images/cellX.png')
        self.cell_P_image = pg.image.load('images/cellP.png')
        self.board_cells_copy = self.board_cells.copy()

    def fill_cell(self, x, y, image, tile):
        return {
            'rect': pg.Rect((25 + y * (WINDOW_WIDTH - 50) // 8), (25 + x * (WINDOW_HEIGHT - 50) // 8),
                            ((WINDOW_WIDTH - 50) // 8), ((WINDOW_HEIGHT - 50) // 8)),
            'surface': image,
            'cX': x,
            'cY': y,
            'tile': tile,
        }

    def get_new_board(self):
        for y in range(WIDTH):
            for x in range(HEIGHT):
                if y == 3:
                    if x == 3:
                        self.board_cells.append(self.fill_cell(x, y, self.cell_X_image, 'X'))
                        continue
                    elif x == 4:
                        self.board_cells.append(self.fill_cell(x, y, self.cell_O_image, 'O'))
                        continue
                if y == 4:
                    if x == 3:
                        self.board_cells.append(self.fill_cell(x, y, self.cell_O_image, 'O'))
                        continue
                    elif x == 4:
                        self.board_cells.append(self.fill_cell(x, y, self.cell_X_image, 'X'))
                        continue
                self.board_cells.append(self.fill_cell(x, y, self.cell_image, ' '))

    def get_board_copy(self):
        self.board_cells_copy = self.board_cells.copy()

    def is_on_board(self, x, y):
        return 0 <= x <= WIDTH - 1 and 0 <= y <= HEIGHT - 1

    def get_valid_moves(self, tile):
        valid_moves = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.is_valid_move(tile, x, y):
                    valid_moves.append([x, y])
        return valid_moves

    def is_valid_move(self, tile, x_start, y_start):
        for cell_start in self.board_cells:
            if cell_start['cX'] == x_start and cell_start['cY'] == y_start:
                if cell_start['tile'] != ' ' or not self.is_on_board(x_start, y_start):
                    return False

                if tile == 'X':
                    other_tile = 'O'
                else:
                    other_tile = 'X'

                tiles_to_flip = []
                for x_direction, y_direction in DIRECTIONS:
                    x, y = x_start, y_start
                    x += x_direction
                    y += y_direction
                    k = 0
                    while self.is_on_board(x, y) and k == 0:
                        for cell in self.board_cells[:]:
                            if cell['cX'] == x and cell['cY'] == y:
                                if cell['tile'] == other_tile:
                                    x += x_direction
                                    y += y_direction
                                elif cell['tile'] == tile:
                                    while True:
                                        x -= x_direction
                                        y -= y_direction
                                        if x == x_start and y == y_start:
                                            break
                                        tiles_to_flip.append([x, y])
                                else:
                                    k = 1

                if len(tiles_to_flip) == 0:
                    return False
                return tiles_to_flip

    def get_board_with_valid_moves(self, tile):
        self.get_board_copy()
        for x, y in self.get_valid_moves(tile):
            for cell in self.board_cells_copy[:]:
                if cell['cX'] == x and cell['cY'] == y:
                    self.board_cells_copy.remove(cell)
                    self.board_cells_copy.append(self.fill_cell(x, y, self.cell_P_image, '.'))
                    break
        self.board_cells = self.board_cells_copy.copy()
