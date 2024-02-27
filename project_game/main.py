# # from project_game.log import logger
# # logger.info()

import math
import time
import pygame
import random


class Menu:
    def __init__(self):
        self.players = []

    def display_menu(self):
        # Display menu options and buttons
        register_button = pygame.Rect(50, 50, 200, 50)
        game_button = pygame.Rect(50, 150, 200, 50)
        statistics_button = pygame.Rect(50, 250, 200, 50)

        pygame.draw.rect(game_screen, (0, 255, 0), register_button)
        pygame.draw.rect(game_screen, (0, 255, 0), game_button)
        pygame.draw.rect(game_screen, (0, 255, 0), statistics_button)

        font = pygame.font.Font(None, 36)
        text_register = font.render('Register', True, (255, 255, 255))
        text_game = font.render('Game', True, (255, 255, 255))
        text_statistics = font.render('Statistics', True, (255, 255, 255))

        game_screen.blit(text_register, (register_button.x + 10, register_button.y + 10))
        game_screen.blit(text_game, (game_button.x + 10, game_button.y + 10))
        game_screen.blit(text_statistics, (statistics_button.x + 10, statistics_button.y + 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if register_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                self.register_player()

        if game_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                game.run()

        if statistics_button.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                self.view_player_list()

    def register_player(self):
        player_name = input("Enter player name: ")
        with open('player_names.txt', 'a') as file:
            file.write(player_name + '\n')
        print(f"Player {player_name} registered successfully!")

    def view_player_list(self):
        with open('player_names.txt', 'r') as file:
            players = file.readlines()
            print("List of registered players:")
            for player in players:
                print(player.strip())


class Game:

    def init(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.obstacles = []
        self.running = True
        self.collisions_count = 0



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

    def check_collision(self, player, hero):
        if (player.x < hero.x + hero.width and
                player.x + player.width > hero.x and
                player.y < hero.y + hero.height and
                player.y + player.height > hero.y):
            return True
        return False

    def quit(self):
        pygame.quit()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (100, 255, 10)
        self.bullets = []

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy, obstacles):
        new_x = self.x + dx
        new_y = self.y + dy
        if not self.collides_with_obstacles(new_x, new_y, obstacles):
            self.x = new_x
            self.y = new_y

    def collides_with_obstacles(self, x, y, obstacles):
        for obstacle in obstacles:
            if (x < obstacle[0] + obstacle[2] and x + self.width > obstacle[0]
                    and y < obstacle[1] + obstacle[3] and y + self.height > obstacle[1]):
                return True
        return False

    def bot_move(self, hero):
        dx = hero.x - self.x
        dy = hero.y - self.y
        angle = math.atan2(dy, dx)
        speed = 2
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        self.move(dx, dy, game.obstacles)

    def shoot_at(self, target):
        bullet_speed = 8
        angle = math.atan2(target.y - (self.y + self.height // 2), target.x - (self.x + self.width // 2))
        bullet_dx = math.cos(angle) * bullet_speed
        bullet_dy = math.sin(angle) * bullet_speed
        bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy, (255, 0, 0))
        self.bullets.append(bullet)

    def reset_position(self, x, y):
        self.x = x
        self.y = y


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = (100, 100, 100)
        self.bullets = []
        self.shoot_cooldown = 5
        self.last_shot_time = 0
        self.angle = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

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
        self.angle += 1

    def collides_with_hero(self, bullet):
        if (bullet.x < hero.x + hero.width and
                bullet.x + bullet.width > hero.x and
                bullet.y < hero.y + hero.height and
                bullet.y + bullet.height > hero.y):
            return True
        return False

    def collides_with_player(self, bullet):
        if (bullet.x < player.x + player.width and
                bullet.x + bullet.width > player.x and
                bullet.y < player.y + player.height and
                bullet.y + bullet.height > player.y):
            return True
        return False

    def shoot(self, mouse_x, mouse_y):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time
            bullet_speed = 8
            angle = math.atan2(mouse_y - (self.y + self.height // 2), mouse_x - (self.x + self.width // 2))
            bullet_dx = math.cos(angle) * bullet_speed
            bullet_dy = math.sin(angle) * bullet_speed
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2, bullet_dx, bullet_dy, (255, 0, 0))
            self.bullets.append(bullet)

    def update(self, mouse_x, mouse_y):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot(mouse_x, mouse_y)
        for bullet in self.bullets:
            bullet.update()
            bullet.draw(game.screen)

        for bullet in self.bullets:
            if self.collides_with_player(bullet):
                player.reset_position(10, 10)
                game.collisions_count += 1
                self.bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 5
        self.height = 5
        self.radius = 3
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    # def move(self):
    #     self.x += self.dx
    #     self.y += self.dy

    def check_collision(self, screen_width, screen_height):
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            return True
        return False


if __name__ == "__main__":
    game = Game()
    game.init()
    pygame.init()
    player = Player(10, 10)
    hero = Hero(10, 500)
    screen_width = 800
    screen_height = 600
    game_screen = pygame.display.set_mode((screen_width, screen_height))
    collisions_count = 0
    try:
        while game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        player.shoot_at(hero)

            hero.rotate()
            player.bot_move(hero)
            # player.shoot_at(hero)

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
            player.draw(game_screen)

            hero.move(0, 0, game.obstacles)

            hero.draw(game.screen)

            for obstacle in game.obstacles:
                pygame.draw.rect(game.screen, (0, 0, 0),
                                 pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hero.update(mouse_x, mouse_y)

            if game.check_collision(player, hero):
                game.running = False

            pygame.display.flip()
            game.clock.tick(60)

        new_window = pygame.display.set_mode((675, 400))
        font = pygame.font.Font(None, 36)
        text = font.render(f'You hit your opponent {game.collisions_count} times, loser', True, (255, 255, 255))
        new_window.blit(text, (150, 200))
        pygame.display.flip()
        time.sleep(3)

        game.quit()

    except KeyboardInterrupt:
        game.quit()





