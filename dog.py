import pygame


class Dog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_right = pygame.image.load("imgs/dog_right.jpg")
        self.image_left = pygame.image.load("imgs/dog_left.jpg")
        self.image = self.image_right  # Изначально устанавливаем изображение для движения вправо
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.y_momentum = 0

    def move_left(self):
        self.rect.x -= 1
        self.image = self.image_left

    def move_right(self):
        self.rect.x += 1
        self.image = self.image_right
