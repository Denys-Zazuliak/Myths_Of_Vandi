import random
import pygame

SCREEN_WIDTH = 1280 #1600
SCREEN_HEIGHT = 960 #900
TILE_SIZE=64 #50
FPS = 60

class Game:
    def __init__(self):
        # general setup
        self.setting_up()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.count = 1
        self.sprites=[]

    def setting_up(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        print(SCREEN_WIDTH / TILE_SIZE)
        print(SCREEN_HEIGHT / TILE_SIZE)
        while self.running:

            keys=self.input_handling()

            self.draw()

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
        self.draw_grid()
        self.level1()

    def draw_grid(self):
        for line in range(0, 80):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_SIZE), (SCREEN_WIDTH, line * TILE_SIZE))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_SIZE, 0), (line * TILE_SIZE, SCREEN_HEIGHT))


    def level1(self):
        layout=[
            ['B20'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A9', 'B1', 'A8', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['B1', 'A18', 'B1'],
            ['A3', 'B17'],
        ]
        world=World(layout)
        level1=world.load_level()

        for tile in level1:
            self.screen.blit(tile[0], tile[1])

    def endframe(self):
        # updating display and game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

class World():
    def __init__(self, data):
        self.tile_list=[]
        self.data = data

        self.block=pygame.image.load(f'assets/block.jpg')

        self.tile_count=0
        self.row_count=0

    def load_level(self):
        self.row_count=0
        for row in self.data:
            self.tile_count=0
            for tile in row:
                if tile[0]=='A':
                    self.tile_count+=int(tile[1:])
                if tile[0]=='B':
                    for i in range(int(tile[1:])):
                        img=pygame.transform.scale(self.block,(TILE_SIZE,TILE_SIZE))
                        img_rect=img.get_rect()
                        img_rect.x = TILE_SIZE*self.tile_count
                        img_rect.y= TILE_SIZE*self.row_count

                        tile=(img, img_rect)
                        self.tile_list.append(tile)

                        self.tile_count = self.tile_count + 1

            self.row_count+=1

        return self.tile_list



if __name__ == '__main__':
    game = Game()
    game.main_screen()