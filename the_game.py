import math
import random

import pygame, sys

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
FPS = 60

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1

    def main_screen(self):
        # game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys = pygame.key.get_pressed()

            self.screen.fill((135, 200, 235))

            # updating display and game
            pygame.display.flip()
            self.clock.tick(FPS)
            self.count += 1

        pygame.quit()

class Player:
    def __init__(self):
        pass

if __name__ == '__main__':
    game = Game()
    game.main_screen()