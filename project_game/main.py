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
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            pygame.display.flip()
            self.clock.tick(60)

    def quit(self):
        pygame.quit()


# class Hero:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.width = 50
#         self.height = 50
#         self.color = (100, 100, 100)
#
#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
#
#     def move(self, dx, dy):
#         self.x += dx
#         self.y += dy
#
#     def rotate(self):
#         # Implement rotation logic
#         pass
#
#     def update(self):
#         # Implement logic for updating hero's state
#         pass


if __name__ == "__main__":
    game = Game()
    game.__init__()
    game.run()
    game.quit()
    # hero = Hero

    try:
        game.run()
    except KeyboardInterrupt:
        game.quit()

