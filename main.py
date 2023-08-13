import pygame, sys, random
from Button import Button
from config import *
from pygame import mixer


pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH = SCREEN.get_width()
WINDOW_HEIGHT = SCREEN.get_height()
WINDOW_CENTER_X = WINDOW_WIDTH / 2
WINDOW_CENTER_Y = WINDOW_HEIGHT / 2

mixer.init()
theme = mixer.Sound("assets/music/theme.mp3")
theme.play(-1)
theme.set_volume(0.15)

line_dodge_sound = mixer.Sound("assets/music/line_dodge.wav")
line_dodge_sound.set_volume(0.20)

clock = pygame.time.Clock()


def get_image(name):
    return pygame.image.load("assets/images/" + name)


def get_font(name, size):
    return pygame.font.Font("assets/fonts/" + name, size)


def check_tetro_borders(grid, pos, move, tetro_code, tetro_n):
    new_pos_x = pos[0] + move[0]
    new_pos_y = pos[1] + move[1]

    # checking out borders for new position
    for i in range(4):
        if not (0 <= (new_pos_y + tetro_code[i][1]) < BOARD_HEIGHT) or not (0 <= (new_pos_x + tetro_code[i][0]) < BOARD_WIDTH):
            return False

    clear_pos(grid, pos, tetro_code)

    for i in range(4):
        # if there's any obstacle in new position then reverse   back to initial positions
        if grid[new_pos_y + tetro_code[i][1]][new_pos_x + tetro_code[i][0]] != 0:
            fill_pos(grid, pos, tetro_code, tetro_n)
            return False
    fill_pos(grid, pos, tetro_code, tetro_n)
    return True


# clear given position cells
def clear_pos(grid, pos, code):
    for i in range(4):
        if (0 <= (pos[1] + code[i][1]) < BOARD_HEIGHT) and (0 <= (pos[0] + code[i][0]) < BOARD_WIDTH):
            grid[pos[1] + code[i][1]][pos[0] + code[i][0]] = 0


# fill given position cells
def fill_pos(grid, pos, code, tetro_n):
    for i in range(4):
        if not (pos[1] + code[i][1] < BOARD_HEIGHT) or not (0 <= (pos[0] + code[i][0]) < BOARD_WIDTH):
            return -1
        if grid[pos[1] + code[i][1]][pos[0] + code[i][0]] != 0:
            return -1
    for i in range(4):
        if pos[1] + code[i][1] < 0:
            continue
        grid[pos[1] + code[i][1]][pos[0] + code[i][0]] = tetro_n


def rotate_tetro(grid, tetro_pos, tetro_code):
    for i in range(4):
        if not (0 <= (tetro_pos[0] - tetro_code[i][1]) < BOARD_WIDTH) or not (0 <= (tetro_pos[1] + tetro_code[i][0]) < BOARD_HEIGHT):
            return -1
    for i in range(4):
        rep = tetro_code[i][0]
        tetro_code[i][0] = -tetro_code[i][1]
        tetro_code[i][1] = rep


# gives figure fall positions
def get_fall_cells(grid, tetro_pos, tetro_code):
    x = tetro_pos[0]
    y = tetro_pos[1]
    fall_cells = []
    end_pos = (x, y)

    if (0 <= x < BOARD_WIDTH) and (0 <= y < BOARD_HEIGHT):
        end = False

        for yi in range(y + 1, BOARD_HEIGHT):

            for i in range(4):
                if check_own_cells((x + tetro_code[i][0], yi + tetro_code[i][1]), tetro_pos, tetro_code):
                    continue

                if (yi + tetro_code[i][1]) >= BOARD_HEIGHT or 0 < (x + tetro_code[i][0]) >= BOARD_WIDTH:
                    continue

                if grid[yi + tetro_code[i][1]][x + tetro_code[i][0]] != 0:
                    end_pos = (x, yi - 1)
                    end = True
                    break

                if (yi + tetro_code[i][1]) == (BOARD_HEIGHT - 1):
                    end_pos = (x, yi)
                    end = True
                    break

            if end:
                break

        for i in range(4):
            if 0 <= (end_pos[0] + tetro_code[i][0]) < BOARD_WIDTH and 0 <= (end_pos[1] + tetro_code[i][1]) < BOARD_HEIGHT:
                fall_cells.append((end_pos[0] + tetro_code[i][0], end_pos[1] + tetro_code[i][1]))

        return fall_cells
    else:
        return []


def get_end_pos(grid, tetro_pos, tetro_code):
    x = tetro_pos[0]
    y = tetro_pos[1]

    if (0 <= x < BOARD_WIDTH) and (0 <= y < BOARD_HEIGHT):
        end = False

        for yi in range(y + 1, BOARD_HEIGHT):

            for i in range(4):
                if check_own_cells((x + tetro_code[i][0], yi + tetro_code[i][1]), tetro_pos, tetro_code):
                    continue

                if (yi + tetro_code[i][1]) >= BOARD_HEIGHT or 0 < (x + tetro_code[i][0]) >= BOARD_WIDTH:
                    continue

                if grid[yi + tetro_code[i][1]][x + tetro_code[i][0]] != 0:
                    return x, yi - 1

                if (yi + tetro_code[i][1]) == (BOARD_HEIGHT - 1):
                    return x, yi

            if end:
                break
    else:
        return ()


# checks out does cell belong to given tetromino
def check_own_cells(cell_pos, tetro_pos, tetro_code):
    for i in range(4):
        if (cell_pos[0] == (tetro_pos[0] + tetro_code[i][0])) and (cell_pos[1] == (tetro_pos[1] + tetro_code[i][1])):
            return True
    return False


def remove_line(grid, line_n):
    if not (0 <= line_n < BOARD_HEIGHT):
        return -1

    for i in range(line_n, 0, -1):
        grid[i] = grid[i - 1].copy()


def get_full_lines(grid):
    lines = []

    for i in range(BOARD_HEIGHT):
        full = True
        for j in range(BOARD_WIDTH):
            if grid[i][j] == 0:
                full = False
                break
        if full:
            lines.append(i)

    return lines


def check_defeat(grid, next_pos, next_tetro):
    for i in range(4):
        if 0 <= (next_pos[0] + next_tetro[i][0]) < BOARD_WIDTH and 0 <= next_pos[1] + next_tetro[i][1] < BOARD_HEIGHT:
            if grid[next_pos[1] + next_tetro[i][1]][next_pos[0] + next_tetro[i][0]] != 0:
                return True
    return False


background_image = get_image("back.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


def settings():
    global DIFFICULTY

    label_text = get_font("domkrat-bold.ttf", 70).render("ВЫБЕРИТЕ СЛОЖНОСТЬ", True, "White")
    label_rect = label_text.get_rect()
    label_rect.center = (int(WINDOW_WIDTH / 2), 70)

    easy_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200), "ЛЕГКО", get_font("domkrat-bold.ttf", 50), BUTTON_TEXT_COLOR, "White")
    middle_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), "СРЕДНЕ", get_font("domkrat-bold.ttf", 50), BUTTON_TEXT_COLOR, "White")
    hard_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200), "СЛОЖНО", get_font("domkrat-bold.ttf", 50), BUTTON_TEXT_COLOR, "White")

    while True:
        clock.tick(FPS)

        SCREEN.blit(background_image, (0, 0))

        SCREEN.blit(label_text, label_rect)

        menu_mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.checkForInput(menu_mouse_pos):
                    DIFFICULTY = "EASY"
                    return
                if middle_button.checkForInput(menu_mouse_pos):
                    DIFFICULTY = "MIDDLE"
                    return
                if hard_button.checkForInput(menu_mouse_pos):
                    DIFFICULTY = "HARD"
                    return

        for button in [easy_button, middle_button, hard_button]:
            button.update(SCREEN)
            button.changeColor(menu_mouse_pos)

        pygame.display.flip()


def play():
    global MOVE_TIME

    SCORE = 0

    level_value_text = get_font("domkrat-bold.ttf", 35).render("Легкий", True, "White")

    if DIFFICULTY == "EASY":
        MOVE_TIME = EASY_DIFFICULTY_TIME
    if DIFFICULTY == "MIDDLE":
        MOVE_TIME = MIDDLE_DIFFICULTY_TIME
        level_value_text = get_font("domkrat-bold.ttf", 35).render("Средний", True, "White")
    if DIFFICULTY == "HARD":
        MOVE_TIME = HARD_DIFFICULTY_TIME
        level_value_text = get_font("domkrat-bold.ttf", 35).render("Сложный", True, "White")

    # TEXTS

    menu_text = get_font("domkrat-bold.ttf", 90).render("TETRIS", True, "White")
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WINDOW_WIDTH / 2, 70)

    next_text = get_font("domkrat-bold.ttf", 35).render("Следующая фигура:", True, "White")
    next_rect = next_text.get_rect()
    next_rect.center = (WINDOW_WIDTH * 0.73, WINDOW_HEIGHT * 0.23)
    next_pos = (next_rect.center[0] * 0.995, next_rect.center[1] + TILE_SIZE * 2.5)

    score_text = get_font("domkrat-bold.ttf", 35).render("Счет", True, "White")
    score_rect = score_text.get_rect()
    score_rect.center = (WINDOW_WIDTH * 0.30, WINDOW_HEIGHT * 0.70)

    score_number_text = get_font("domkrat-bold.ttf", 35).render(str(SCORE), True, "White")
    score_number_rect = score_text.get_rect()
    score_number_rect.center = (score_rect.center[0] * 1.05, score_rect.center[1] + TILE_SIZE * 1.5)

    defeat_text = get_font("domkrat-bold.ttf", 100).render("Конец игры", True, "White")
    defeat_rect = defeat_text.get_rect()
    defeat_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    level_text = get_font("domkrat-bold.ttf", 35).render("Уровень:", True, "White")
    level_rect = level_text.get_rect()
    level_rect.center = (WINDOW_WIDTH * 0.30, WINDOW_HEIGHT * 0.23)

    level_value_rect = level_value_text.get_rect()
    level_value_rect.center = (WINDOW_WIDTH * 0.30, WINDOW_HEIGHT * 0.28)

    back_button = Button(pygame.transform.scale(get_image("red_button.png"), (200, 50)), (120, 50), "НАЗАД",
                         get_font("domkrat-bold.ttf", 30), BUTTON_TEXT_COLOR, "White")

    # --------------------------------------------------------------------


    # list containing board information
    grid = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    curr_fig_n = random.randint(1, 6)
    curr_fig_code = TETRO_CODES[curr_fig_n]
    curr_fig_pos = [int(BOARD_WIDTH / 2), 0]

    next_fig_n = random.randint(1, 6)

    run = True
    move_timer = MOVE_TIME * FPS

    while True:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("black")

        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(next_text, next_rect)
        SCREEN.blit(score_text, score_rect)
        SCREEN.blit(score_number_text, score_number_rect)
        SCREEN.blit(level_text, level_rect)
        SCREEN.blit(level_value_text, level_value_rect)


        end_of_curr = False

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(mouse_pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT \
                        and check_tetro_borders(grid, curr_fig_pos, (-1, 0), curr_fig_code, curr_fig_n):
                    clear_pos(grid, curr_fig_pos, curr_fig_code)
                    curr_fig_pos[0] -= 1
                    fill_pos(grid, curr_fig_pos, curr_fig_code, curr_fig_n)
                if event.key == pygame.K_RIGHT \
                        and check_tetro_borders(grid, curr_fig_pos, (1, 0), curr_fig_code, curr_fig_n):
                    clear_pos(grid, curr_fig_pos, curr_fig_code)
                    curr_fig_pos[0] += 1
                    fill_pos(grid, curr_fig_pos, curr_fig_code, curr_fig_n)
                if event.key == pygame.K_SPACE:
                    clear_pos(grid, curr_fig_pos, curr_fig_code)
                    curr_fig_pos = get_end_pos(grid, curr_fig_pos, curr_fig_code)
                    fill_pos(grid, curr_fig_pos, curr_fig_code, curr_fig_n)

                    for line in get_full_lines(grid):
                        remove_line(grid, line)
                        SCORE += SCORE_NUMBER
                        line_dodge_sound.play()

                    if check_defeat(grid, (int(BOARD_WIDTH / 2), 0), TETRO_CODES[next_fig_n]):
                        run = False

                    curr_fig_n = next_fig_n
                    curr_fig_pos = [int(BOARD_WIDTH / 2), 0]
                    curr_fig_code = TETRO_CODES[next_fig_n]
                    next_fig_n = random.randint(1, 6)

                    move_timer = MOVE_TIME * FPS + FPS / 2
                    end_of_curr = True
                if event.key == pygame.K_DOWN:
                    move_timer = 0
                if event.key == pygame.K_UP:
                    if curr_fig_n != 3:
                        clear_pos(grid, curr_fig_pos, curr_fig_code)
                        rotate_tetro(grid, curr_fig_pos, curr_fig_code)
                        fill_pos(grid, curr_fig_pos, curr_fig_code, curr_fig_n)

        for button in [back_button]:
            button.update(SCREEN)
            button.changeColor(mouse_pos)

        # ----------------------- main game logic (begin) -----------------------------------

        board_begin_x = WINDOW_CENTER_X - (BOARD_WIDTH * TILE_SIZE) / 2
        board_begin_y = WINDOW_CENTER_Y - (BOARD_HEIGHT * TILE_SIZE) / 2

        if move_timer == 0 and not end_of_curr:
            clear_pos(grid, curr_fig_pos, curr_fig_code)

            if fill_pos(grid, (curr_fig_pos[0], curr_fig_pos[1] + 1), curr_fig_code, curr_fig_n) != -1:
                curr_fig_pos[1] += 1
            else:
                # if tetromino has reached end of his way
                fill_pos(grid, curr_fig_pos, curr_fig_code, curr_fig_n)

                for line in get_full_lines(grid):
                    remove_line(grid, line)
                    SCORE += SCORE_NUMBER
                    line_dodge_sound.play()

                score_number_text = get_font("domkrat-bold.ttf", 35).render(str(SCORE), True, "White")

                if check_defeat(grid, (int(BOARD_WIDTH / 2), 0), TETRO_CODES[next_fig_n]):
                    run = False

                move_timer = 1

                curr_fig_n = next_fig_n
                curr_fig_pos = [int(BOARD_WIDTH / 2), 0]
                curr_fig_code = TETRO_CODES[next_fig_n]

                next_fig_n = random.randint(1, 6)

        # board drawing
        for i in range(0, BOARD_WIDTH):
            for j in range(0, BOARD_HEIGHT):
                pygame.draw.rect(SCREEN, "#575353", pygame.Rect(board_begin_x + i * TILE_SIZE,
                                                              board_begin_y + j * TILE_SIZE,
                                                              TILE_SIZE,
                                                              TILE_SIZE), GRID_THICK, CELL_ANGLE)

                if grid[j][i] != 0:
                    pygame.draw.rect(SCREEN, TETRO_COLORS[grid[j][i]], pygame.Rect(board_begin_x + i * TILE_SIZE + 2,
                                                              board_begin_y + j * TILE_SIZE + 2,
                                                              TILE_SIZE - 4,
                                                              TILE_SIZE - 4), 0, CELL_ANGLE)

        # highlighting fall positions
        for cell in get_fall_cells(grid, curr_fig_pos, curr_fig_code):
            if run:
                pygame.draw.rect(SCREEN, TETRO_COLORS[curr_fig_n], pygame.Rect(board_begin_x + cell[0] * TILE_SIZE + 2,
                                                          board_begin_y + cell[1] * TILE_SIZE + 2,
                                                          TILE_SIZE - 4,
                                                          TILE_SIZE - 4), 2, CELL_ANGLE)

        # display next figure
        for i in range(4):
            pygame.draw.rect(SCREEN, "white", pygame.Rect(next_pos[0] + TETRO_CODES[next_fig_n][i][0] * TILE_SIZE,
                                                          next_pos[1] + TETRO_CODES[next_fig_n][i][1] * TILE_SIZE,
                                                          TILE_SIZE,
                                                          TILE_SIZE), GRID_THICK, CELL_ANGLE)
            pygame.draw.rect(SCREEN, TETRO_COLORS[next_fig_n],
                             pygame.Rect(next_pos[0] + TETRO_CODES[next_fig_n][i][0] * TILE_SIZE + 2,
                                         next_pos[1] + TETRO_CODES[next_fig_n][i][1] * TILE_SIZE + 2,
                                         TILE_SIZE - 4, TILE_SIZE - 4), 0, CELL_ANGLE)

        # timer update
        if move_timer == 0 and run:
            move_timer = MOVE_TIME * FPS
        else:
            move_timer -= 1

        # ----------------------- main game logic (end) -------------------------------------

        if not run:
            pygame.draw.rect(SCREEN, "black", defeat_rect)
            SCREEN.blit(defeat_text, defeat_rect)

        pygame.display.flip()


def main_menu():
    menu_text = get_font("domkrat-bold.ttf", 150).render("ГЛАВНОЕ МЕНЮ", True, "White")
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WINDOW_WIDTH / 2, 70)

    play_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200), "ИГРАТЬ",
                         get_font("domkrat-bold.ttf", 55), BUTTON_TEXT_COLOR, "White")
    settings_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), "НАСТРОЙКИ",
                             get_font("domkrat-bold.ttf", 55), BUTTON_TEXT_COLOR, "White")
    quit_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200), "ВЫЙТИ",
                         get_font("domkrat-bold.ttf", 55), BUTTON_TEXT_COLOR, "White")

    while True:
        clock.tick(FPS)

        SCREEN.blit(background_image, (0, 0))

        SCREEN.blit(menu_text, menu_rect)

        menu_mouse_pos = pygame.mouse.get_pos()

        for button in [play_button, settings_button, quit_button]:
            button.update(SCREEN)
            button.changeColor(menu_mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if settings_button.checkForInput(menu_mouse_pos):
                    settings()

        pygame.display.flip()


main_menu()
