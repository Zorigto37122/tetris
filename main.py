import pygame, sys
from Button import Button
from config import *


pygame.init()

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WINDOW_WIDTH = SCREEN.get_width()
WINDOW_HEIGHT = SCREEN.get_height()

clock = pygame.time.Clock()


def get_image(name):
    return pygame.image.load("assets/images/" + name)


def get_font(name, size):
    return pygame.font.Font("assets/fonts/" + name, size)


def lvl_choose():
    pass


background_image = get_image("back.png")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

def settings():
    global DIFFICULTY

    label_text = get_font("domkrat-bold.ttf", 70).render("ВЫБЕРИТЕ СЛОЖНОСТЬ", True, "White")
    label_rect = label_text.get_rect()
    label_rect.center = (WINDOW_WIDTH / 2, 70)

    easy_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200), "ЛЕГКО", get_font("domkrat-bold.ttf", 50), "#FCD029", "White")
    middle_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), "СРЕДНЕ", get_font("domkrat-bold.ttf", 50), "#FCD029", "White")
    hard_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200), "СЛОЖНО", get_font("domkrat-bold.ttf", 50), "#FCD029", "White")

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
    menu_text = get_font("domkrat-bold.ttf", 90).render("TETRIS", True, "White")
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WINDOW_WIDTH / 2, 70)

    while True:
        clock.tick(FPS)

        SCREEN.fill("black")

        SCREEN.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        pygame.display.flip()


def main_menu():
    menu_text = get_font("domkrat-bold.ttf", 150).render("ГЛАВНОЕ МЕНЮ", True, "White")
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WINDOW_WIDTH / 2, 70)

    play_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200), "ИГРАТЬ",
                         get_font("domkrat-bold.ttf", 55), "#FCD029", "White")
    settings_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), "НАСТРОЙКИ",
                             get_font("domkrat-bold.ttf", 55), "#FCD029", "White")
    quit_button = Button(get_image("red_button.png"), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 200), "ВЫЙТИ",
                         get_font("domkrat-bold.ttf", 55), "#FCD029", "White")


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
