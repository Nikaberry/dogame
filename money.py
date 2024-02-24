import pygame
import random
score = 0

player_rect = pygame.Rect(0, 600 - 50, 50, 50)


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("imgs/coin.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Создаем группу для монеток
money_group = pygame.sprite.Group()

# Создаем монетки и добавляем их на платформы
platforms = [pygame.Rect(300, 500, 200, 30), pygame.Rect(100, 400, 200, 30)]
for platform in platforms:
    for i in range(10):
        money = Money(platform.x + 20*i, platform.y - 20)
        money_group.add(money)

def check_collision():
    global score
    for money in money_group:
        if player_rect.colliderect(money.rect):
            money_group.remove(money)
            score += 1
    for platform in platforms:
        if player_rect.colliderect(platform):
            if player_y_momentum > 0:
                player_rect.y = platform.top - player_rect.height
                player_y_momentum = 0
            elif player_y_momentum < 0:
                player_rect.y = platform.bottom
                player_y_momentum = 0