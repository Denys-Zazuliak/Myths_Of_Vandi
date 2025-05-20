import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 60

class Game:
    def __init__(self):
        # general setup
        self.pygame_init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.count = 1
        self.blocks=[]
        self.gravity=0.5

    def create_player(self):
        PLAYER_WIDTH = pygame.display.get_window_size()[0] // 200
        PLAYER_HEIGHT = pygame.display.get_window_size()[1] // 200
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.player=Player()

    def create_block(self, x, y, width, height, colour=(0,0,0)):
        block=Block(x, y, width, height, colour)
        self.blocks.append(block)

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption('Myths Of Vandi')

    def main_screen(self):
        # game loop
        self.create_player()
        self.create_block(500, 1000, 100, 50)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            keys=self.input_handling()

            if keys[pygame.K_SPACE] and self.player.on_ground:
                self.player.jump()

            self.draw()

            self.player.update()

            self.player.wall_collisions()

            self.player.collision(self.blocks)

            self.endframe()

        pygame.quit()

    def input_handling(self):
        keys = pygame.key.get_pressed()

        return keys

    def draw(self):
        self.screen.fill((135, 200, 235))
        pygame.draw.rect(self.screen, (255, 255, 255), self.player.rect)
        for block in self.blocks:
            pygame.draw.rect(self.screen, block.colour, block.rect)

    def endframe(self):
        # updating  game
        pygame.display.flip()
        self.clock.tick(FPS)
        self.count += 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.rect = pygame.Rect(500, 500, 64, 64)
        self.on_ground = True
        self.velocity=[0, 0]

    def jump(self):
        self.on_ground = False
        self.velocity[1] = -10

    def update(self):
        if not self.on_ground:
            self.velocity[1] += game.gravity
        self.rect.move_ip(self.velocity[0], self.velocity[1])

    def wall_collisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True

    def collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block):
                # if self.rect.left < block.rect.right and self.rect.left > block.rect.left:
                #     self.rect.left = block.rect.right
                # elif self.rect.right > block.rect.left:
                #     self.rect.right = block.rect.left
                # elif self.rect.top <= block.rect.bottom:
                #     self.rect.top = block.rect.bottom
                # elif self.rect.bottom >= block.rect.top:
                #     self.rect.bottom = block.rect.top
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.velocity[1] = 0


    def get_on_ground(self):
        return self.on_ground

class Block:
    def __init__(self, x, y, width, height, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour



if __name__ == '__main__':
    game = Game()
    game.main_screen()

# Lyrics of Bohemian Raphsody because i like it

# Is this the real life? Is this just fantasy?
# Caught in a landslide, no escape from reality
# Open your eyes, look up to the skies and see
# I'm just a poor boy, I need no sympathy
# Because I'm easy come, easy go
# Little high, little low
# Any way the wind blows doesn't really matter to me, to me
# Mama, just killed a man
# Put a gun against his head, pulled my trigger, now he's dead
# Mama, life had just begun
# But now I've gone and thrown it all away
# Mama, ooh, didn't mean to make you cry
# If I'm not back again this time tomorrow
# Carry on, carry on as if nothing really matters
# Too late, my time has come
# Sends shivers down my spine, body's aching all the time
# Goodbye, everybody, I've got to go
# Gotta leave you all behind and face the truth
# Mama, ooh (any way the wind blows)
# I don't wanna die
# I sometimes wish I'd never been born at all
# I see a little silhouetto of a man
# Scaramouche, Scaramouche, will you do the Fandango?
# Thunderbolt and lightning, very, very frightening me
# (Galileo) Galileo, (Galileo) Galileo, Galileo Figaro, magnifico
# But I'm just a poor boy, nobody loves me
# He's just a poor boy from a poor family
# Spare him his life from this monstrosity
# Easy come, easy go, will you let me go?
# No, we will not let you go (let him go)
# We will not let you go (let him go)
# We will not let you go (let me go)
# Will not let you go (let me go)
# Will not let you go (never, never, never, never let me go)
# No, no, no, no, no, no, no
# Oh, mamma mia, mamma mia
# Mamma mia, let me go
# Beelzebub has a devil put aside for me, for me, for me
# So you think you can stone me and spit in my eye?
# So you think you can love me and leave me to die?
# Oh, baby, can't do this to me, baby
# Just gotta get out, just gotta get right outta here
# Ooh
# Ooh, yeah, ooh, yeah
# Nothing really matters, anyone can see
# Nothing really matters
# Nothing really matters to me