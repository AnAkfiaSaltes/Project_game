# from project_game.log import logger
# logger.info()

import pygame
import sys
import random


class Game:

    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.obstacles = []
        for _ in range(15):
            obstacle_width = random.choice([4, 8]) * 10
            obstacle_height = random.choice([4, 8]) * 10
            obstacle_x = random.randint(0, self.screen_width - obstacle_width)
            obstacle_y = random.randint(0, self.screen_height - obstacle_height)
            self.obstacles.append((obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            # for obstacle in self.obstacles:
            #     pygame.draw.rect(self.screen, (0, 0, 0),
            #                      pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            pygame.display.flip()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (100, 100, 100)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        pass

    def update(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.__init__()
    hero = Hero(400, 300)
    try:
        while game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False

            hero.rotate()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                hero.move(-5, 0)
            if keys[pygame.K_RIGHT]:
                hero.move(5, 0)
            if keys[pygame.K_UP]:
                hero.move(0, -5)
            if keys[pygame.K_DOWN]:
                hero.move(0, 5)

            game.screen.fill((255, 255, 255))
            for obstacle in game.obstacles:
                pygame.draw.rect(game.screen, (0, 0, 0),
                                 pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            hero.draw(game.screen)

            pygame.display.flip()
            game.clock.tick(60)

    except KeyboardInterrupt:
        game.quit()

