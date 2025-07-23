import random
import pygame

SCREEN_WIDTH = 1920 #1280
SCREEN_HEIGHT = 1080 #900
FPS = 60

class Game:
    def __init__(self):
        # general setup
        self.pygame_init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.sprites=[]
        self.tile_size=60 #50

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        while self.running:

            keys=self.input_handling()

            self.draw()
            self.draw_grid()

            self.endframe()

        pygame.quit()

    def input_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()

        return keys

    def draw(self):
        self.screen.fill((50, 50, 50))

    def draw_grid(self):
        for line in range(0, 50):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * self.tile_size), (SCREEN_WIDTH, line * self.tile_size))
            pygame.draw.line(self.screen, (255, 255, 255), (line * self.tile_size, 0), (line * self.tile_size, SCREEN_HEIGHT))

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

if __name__ == '__main__':
    game = Game()
    game.main_screen()