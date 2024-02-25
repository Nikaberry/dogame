import pygame
import sys
import random
from dog import Dog
from platform import Platform
from coin import Coin
from begin import start_screen


class Game:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Doggame")
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.dog = Dog(0, 600)
        self.platforms = [Platform(300, 500, 150, 20), Platform(100, 400, 150, 20),
                          Platform(300, 300, 150, 20), Platform(500, 400, 150, 20),
                          Platform(150, 200, 50, 20), Platform(230, 180, 100, 20),
                          Platform(400, 100, 400, 20)]
        self.coins = pygame.sprite.Group()
        with open("score.txt", "r") as file:
            self.score = int(file.read())
        self.font = pygame.font.Font(None, 36)

        for platform in self.platforms:
            for _ in range(2):
                x = random.randint(platform.rect.left, platform.rect.right)
                y = platform.rect.top - 20
                coin = Coin(x, y)
                self.coins.add(coin)

    def check_collision(self):
        for coin in self.coins:
            if self.dog.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1

        for platform in self.platforms:
            if self.dog.rect.colliderect(platform.rect):
                if self.dog.y_momentum > 0:
                    self.dog.y_momentum = 0
                    self.dog.rect.bottom = platform.rect.top
                    self.jumping = False
                elif self.dog.y_momentum < 0:
                    self.dog.rect.y = platform.rect.bottom
                    self.dog.y_momentum = 0

        if self.dog.rect.bottom >= self.height:
            self.dog.rect.bottom = self.height
            self.jumping = False
            self.dog.y_momentum = 0

        if self.dog.rect.top <= 0:
            self.dog.rect.top = 0
            self.dog.y_momentum = 0

        if self.dog.rect.left < 0:
            self.dog.rect.left = 0
        if self.dog.rect.right > self.width:
            self.dog.rect.right = self.width

    def run(self):
        start_screen()
        self.jumping = False
        self.jump_pressed = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("score.txt", "w") as file:
                        file.write(str(self.score))
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.dog.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.dog.move_right()
            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and (not self.jumping or self.dog.rect.bottom == self.height):
                self.jumping = True
                self.dog.y_momentum = -5

            self.dog.y_momentum += 0.2
            self.dog.rect.y += self.dog.y_momentum

            for platform in self.platforms:
                if self.dog.rect.colliderect(platform.rect):
                    if self.dog.y_momentum > 0:
                        self.dog.y_momentum = 0
                        self.dog.rect.bottom = platform.rect.top
                        self.jumping = False

            if self.dog.rect.left < 0:
                self.dog.rect.left = 0
            if self.dog.rect.right > self.width:
                self.dog.rect.right = self.width

            if self.dog.rect.bottom > self.height:
                self.jumping = False
                self.dog.y_momentum = 0

            if not keys[pygame.K_SPACE]:
                self.jump_pressed = False

            self.screen.fill(self.white)
            self.screen.blit(self.dog.image, self.dog.rect)
            for platform in self.platforms:
                pygame.draw.rect(self.screen, self.black, platform.rect)
            for coin in self.coins:
                pygame.draw.circle(self.screen, self.yellow, coin.rect.center, coin.radius)
            score_text = self.font.render("Score: " + str(self.score), True, self.black)
            self.screen.blit(score_text, (10, 10))
            pygame.display.update()
            self.check_collision()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
