# from project_game.log import logger
# logger.info()

import math
import time
import pygame
import random
import sys


class Game:

    def init(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.obstacles = []
        for _ in range(18):
            obstacle_width = random.choice([4, 8]) * 10
            obstacle_height = random.choice([4, 8]) * 10
            obstacle_x = random.randint(0, self.screen_width - obstacle_width)
            obstacle_y = random.randint(0, self.screen_height - obstacle_height)
            self.obstacles.append((obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            if not (obstacle_x < 400 < obstacle_x + obstacle_width and obstacle_y < 300 < obstacle_y + obstacle_height):
                self.obstacles.append((obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
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
        self.bullets = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def check_collision(self, obstacles, dx, dy):
        for obstacle in obstacles:
            if (self.x + dx < obstacle[0] + obstacle[2] and
                    self.x + self.width + dx > obstacle[0] and
                    self.y + dy < obstacle[1] + obstacle[3] and
                    self.y + self.height + dy > obstacle[1]):
                return True
        return False

    def move(self, dx, dy, obstacles):
        if not self.check_collision(obstacles, dx, 0):
            self.x += dx
        if not self.check_collision(obstacles, 0, dy):
            self.y += dy

    def rotate(self):
        pass

    def shoot(self, mouse_x, mouse_y):
        bullet_speed = 5
        angle = math.atan2(mouse_y - (self.y + self.height // 2), mouse_x - (self.x + self.width // 2))
        bullet_dx = math.cos(angle) * bullet_speed
        bullet_dy = math.sin(angle) * bullet_speed
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy, (255, 0, 0))
        self.bullets.append(bullet)

    def update(self, mouse_x, mouse_y):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button press
                if event.button == 1:  # Check for left mouse button press
                    self.shoot(mouse_x, mouse_y)  # Fire a bullet
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(game.screen)


class Bullet:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.width = 5
        self.height = 5

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


if __name__ == "__main__":
    game = Game()
    game.init()
    hero = Hero(400, 300)
    try:
        while game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False

            hero.rotate()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                hero.move(-5, 0, game.obstacles)
            if keys[pygame.K_RIGHT]:
                hero.move(5, 0, game.obstacles)
            if keys[pygame.K_UP]:
                hero.move(0, -5, game.obstacles)
            if keys[pygame.K_DOWN]:
                hero.move(0, 5, game.obstacles)

            game.screen.fill((255, 255, 255))
            for obstacle in game.obstacles:
                pygame.draw.rect(game.screen, (0, 0, 0),
                                 pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            hero.draw(game.screen)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hero.update(mouse_x, mouse_y)

            pygame.display.flip()
            game.clock.tick(60)

    except KeyboardInterrupt:
        game.quit()

