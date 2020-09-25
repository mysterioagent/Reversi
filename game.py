# Реверси клон Отелло

import random as r
import pygame as pg
from settings import *
import engine


def draw_text(text, text_font, surface, x, y):
    text_obj = text_font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (int(x), int(y))
    surface.blit(text_obj, text_rect)


def enter_player_tile():
    # O - black, X - white
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                engine.terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    return 'O', 'X'
                if event.key == pg.K_w:
                    return 'X', 'O'


def get_score_of_board(board):
    x_score = 0
    o_score = 0
    for cell in board.board_cells:
        if cell['tile'] == 'X':
            x_score += 1
        if cell['tile'] == 'O':
            o_score += 1
    return {'X': x_score, 'O': o_score}


def who_goes_first():
    if r.randint(0, 1) == 0:
        return 'Компьютер'
    else:
        return 'Человек'


def tile_image(board, tile):
    new_image = pg.image
    if tile == ' ':
        new_image = board.cell_image
    elif tile == '.':
        new_image = board.cell_P_image
    elif tile == 'X':
        new_image = board.cell_X_image
    elif tile == 'O':
        new_image = board.cell_O_image
    return new_image


def make_move(board, tile, x_start, y_start):
    tiles_to_flip = board.is_valid_move(tile, x_start, y_start)
    if not tiles_to_flip:
        return False
    for cell in board.board_cells[:]:
        if cell['cX'] == x_start and cell['cY'] == y_start:
            board.board_cells.remove(cell)
            board.board_cells.append(board.fill_cell(x_start, y_start, image=tile_image(board, tile),
                                                     tile=tile))
            # boardCellsCopy.append(new_cell)
            break

    for x, y in tiles_to_flip:
        for cell in board.board_cells[:]:
            if cell['cX'] == x and cell['cY'] == y:
                board.board_cells.remove(cell)
                board.board_cells.append(board.fill_cell(x, y, image=tile_image(board, tile), tile=tile))
                break

    return True


def is_on_corner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


def get_player_move(board, player_tile):
    k = 0
    x = y = 0
    while k == 0:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                engine.terminate()
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    engine.terminate()
            if event.type == pg.MOUSEBUTTONUP:
                x = int((-25 + event.pos[1]) / 50)
                y = int((-25 + event.pos[0]) / 50)
                print(x, y)
                if not board.is_valid_move(player_tile, x, y):
                    continue
                else:
                    k = 1
    return [x, y]


def get_computer_move(board, computer_tile):
    possible_moves = board.get_valid_moves(computer_tile)
    r.shuffle(possible_moves)
    best_move = [0, 0]
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]
    best_score = -1
    for x, y in possible_moves:
        board_copy = engine.Board(board)
        make_move(board_copy, computer_tile, x, y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def draw_board(board, window_surface):

    for cell in board.board_cells:
        window_surface.blit(cell['surface'], cell['rect'])
    pg.display.update()


def print_score(board, player_tile, computer_tile, window_surface, font):
    window_surface.fill(BACKGROUND_COLOR)
    scores = get_score_of_board(board)
    draw_text('Ваш счет: %s. Счет компьютера: %s.' % (scores[player_tile], scores[computer_tile]), font,
              window_surface, 0, int(WINDOW_HEIGHT - 15))


def play_game(board, player_tile, computer_tile, turn, window_surface, font, main_clock):
    show_hints = False
    board.get_new_board()
    while True:
        print('....')
        player_valid_moves = board.get_valid_moves(player_tile)
        computer_valid_moves = board.get_valid_moves(computer_tile)
        print_score(board, player_tile, computer_tile, window_surface, font)
        main_clock.tick(FPS)
        if player_valid_moves == [] and computer_valid_moves == []:
            return board

        elif turn == 'Человек':
            if player_valid_moves:
                if show_hints:
                    board.get_board_with_valid_moves(player_tile)
                draw_board(board, window_surface)
                for cell in board.board_cells:
                    if cell['tile'] in ['X', 'O']:
                        print(cell['cX'], cell['cY'], cell['tile'])
                move = get_player_move(board, player_tile)
                make_move(board, player_tile, move[0], move[1])
            turn = 'Компьютер'

        elif turn == 'Компьютер':
            if computer_valid_moves:
                draw_board(board, window_surface)
                for cell in board.board_cells:
                    if cell['tile'] in ['X', 'O']:
                        print(cell['cX'], cell['cY'], cell['tile'])
                print('move')
                move = get_computer_move(board, computer_tile)
                make_move(board, computer_tile, move[0], move[1])
            turn = 'Человек'


def final_scores(board, player_tile, computer_tile, window_surface, font):
    window_surface.fill(BACKGROUND_COLOR)
    scores = get_score_of_board(board)

    draw_text('X набрал %s очков. O набрал %s очков.' % (scores['X'], scores['O']), font, window_surface, 0, 0)
    if scores[player_tile] > scores[computer_tile]:
        draw_text(f'Вы победили компьютер.'
                  f'Поздравляем!', font, window_surface, 0, 30)
    elif scores[player_tile] < scores[computer_tile]:
        draw_text(f'Вы проиграли. Компьютер победил вас, обогнав '
                  f'на {scores[computer_tile] - scores[player_tile]} очков!', font, window_surface, 0, 30)
    else:
        draw_text('Ничья!', font, window_surface, 0, 30)

    draw_text('Хотите сыграть еще раз? (да или нет)', font, window_surface, 0, 60)
    pg.display.update()
    engine.wait_for_player_to_press_key()


def main():
    pg.init()
    main_clock = pg.time.Clock()
    window_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('Реверси')
    pg.mouse.set_visible(True)

    font = pg.font.SysFont(None, 20)
    window_surface.fill(BACKGROUND_COLOR)

    draw_text('Выберите цвет фишек, b - черные, w - белые', font, window_surface, 0, 0)
    pg.display.update()

    player_tile, computer_tile = enter_player_tile()

    while True:
        turn = who_goes_first()
        window_surface.fill(BACKGROUND_COLOR)
        board = engine.Board()
        draw_text(f'{turn} ходит первым.', font, window_surface, 0, 0)

        pg.display.update()
        engine.wait_for_player_to_press_key()
        window_surface.fill(BACKGROUND_COLOR)
        final_board = play_game(board, player_tile, computer_tile, turn, window_surface, font, main_clock)

        draw_board(final_board, window_surface)
        main_clock.tick(FPS)
        engine.wait_for_player_to_press_key()
        final_scores(final_board, player_tile, computer_tile, window_surface, font)


main()
