import pygame
import sys


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Марио на минималках')
screen_size = (806, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 50


def end():
    pygame.quit()
    sys.exit()


def start_screen():
    background = pygame.image.load('imgs/sky.jpg')
    intro_text = ["Правила игры",
                  "Управлять собакой клавишами: вверх, вправо влево",
                  "Цель игры: собрать монетки",
                  "и дойти до верхней и самой длинной платформы",
                  "Чтобы начать нажмите ПРОБЕЛ"]
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 45)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        pygame.display.flip()
        clock.tick(50)
