import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Окно
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Игра с прыжком и платформами")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# Загрузка изображения собаки
dog_image = pygame.image.load("imgs/dog.jpg")

# Уменьшение размера изображения собаки
dog_image = pygame.transform.scale(dog_image, (50, 50))

# Переменные для собаки
dog_rect = dog_image.get_rect()
dog_rect.bottomleft = (0, WINDOW_HEIGHT)  # Начальное положение собаки

# Переменные для движения собаки
dog_y_momentum = 0
jumping = False

# Переменная, отслеживающая, был ли совершен прыжок
jump_pressed = False

# Платформы
platforms = [pygame.Rect(300, 500, 150, 20), pygame.Rect(100, 400, 150, 20),
             pygame.Rect(300, 300, 150, 20), pygame.Rect(500, 400, 150, 20),
             pygame.Rect(150, 200, 50, 20), pygame.Rect(230, 180, 100, 20),
             pygame.Rect(400, 100, 100, 20), pygame.Rect(520, 50, 280, 20)]

# Переменная для хранения счета игрока
score = 0

# Шрифт для отображения счета
font = pygame.font.Font(None, 36)

# Класс для монеток
class Money(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 10  # Радиус монетки
        self.color = yellow
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 2 * self.radius, 2 * self.radius)

# Создаем группу для монеток
money_group = pygame.sprite.Group()

# Создаем монетки и добавляем их на платформы
for platform in platforms:
    for _ in range(2):
        x = random.randint(platform.left, platform.right)
        y = platform.top - 20
        money = Money(x, y)
        money_group.add(money)


def check_collision():
    global jumping, dog_y_momentum, score
    # Проверка столкновения с монетками
    for money in money_group:
        if dog_rect.colliderect(money.rect):
            money_group.remove(money)
            score += 1

    # Проверка столкновения с платформами
    for platform in platforms:
        if dog_rect.colliderect(platform):
            # Если собака падает на платформу
            if dog_y_momentum > 0:
                dog_rect.y = platform.top - dog_rect.height
                dog_y_momentum = 0
                jumping = False
            # Если собака подпрыгивает под платформу
            elif dog_y_momentum < 0:
                dog_rect.y = platform.bottom
                dog_y_momentum = 0

    # Если собака достигает нижней границы окна
    if dog_rect.bottom >= WINDOW_HEIGHT:
        dog_rect.bottom = WINDOW_HEIGHT
        jumping = False
        dog_y_momentum = 0

    # Если собака достигает верхней границы окна
    if dog_rect.top <= 0:
        dog_rect.top = 0
        dog_y_momentum = 0

    # Если собака выходит за границы по горизонтали
    if dog_rect.left < 0:
        dog_rect.left = 0
    if dog_rect.right > WINDOW_WIDTH:
        dog_rect.right = WINDOW_WIDTH

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dog_rect.x -= 1
    if keys[pygame.K_RIGHT]:
        dog_rect.x += 1

    # Обработка прыжка
    if not jumping or dog_rect.bottom == WINDOW_HEIGHT:
        if keys[pygame.K_SPACE]:
            jumping = True
            dog_y_momentum = -5

    # Гравитация
    dog_y_momentum += 0.2

    # Перемещение собаки
    dog_rect.y += dog_y_momentum

    # Коллизии с платформами
    for platform in platforms:
        if dog_rect.colliderect(platform):
            if dog_y_momentum > 0:
                dog_y_momentum = 0
                dog_rect.bottom = platform.top
                jumping = False

    # Проверка на выход за края окна
    if dog_rect.left < 0:
        dog_rect.left = 0
    if dog_rect.right > WINDOW_WIDTH:
        dog_rect.right = WINDOW_WIDTH

    # Остановка прыжка при достижении нижней границы окна или на платформе/полу
    if dog_rect.bottom > WINDOW_HEIGHT:
        jumping = False
        dog_y_momentum = 0

    # Сброс переменной прыжка при отпускании клавиши
    if not keys[pygame.K_SPACE]:
        jump_pressed = False

    screen.fill(white)
    screen.blit(dog_image, dog_rect)
    for platform in platforms:
        pygame.draw.rect(screen, black, platform)
    for money in money_group:
        pygame.draw.circle(screen, money.color, money.rect.center, money.radius)

    # Отображение счета
    score_text = font.render("Score: " + str(score), True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    # Проверяем столкновения
    check_collision()
