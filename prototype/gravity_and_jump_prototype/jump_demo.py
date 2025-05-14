import pygame
from random import randint

# -----------------------------
# Initialisation Phase
# -----------------------------

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('My Game')
background_colour = (1, 33, 97)
font = pygame.font.SysFont(None, 60)
font_large = pygame.font.SysFont(None, 90)

# Set up the clock for frame rate control
clock = pygame.time.Clock()
fps = 60

# Set some game parameters
game = {
    'acceleration': 0.2,
    'game_over': False,
}

# Define the initial properties for player1
player1 = {
    'color': (255, 0, 0),  # Red color
    'radius': 50,
    'x': SCREEN_WIDTH // 2,
    'y': SCREEN_HEIGHT // 2,
    'speed': 8,
    'horizontal_move': None,
    'vertical_move': None,
    'on_target': False,
    'score': 0,
    'shots': 10,
    'shot_ready': False,
}

target = {
    'color': (255, 255, 0),  # Yellow color
    'radius': 20,
    'x': 0,
    'y': SCREEN_HEIGHT - 5,
    'speed': 5,
    'v_x': randint(10, 15),
    'v_y': randint(-30, -15),
    'status': 'ready',
}

class Jumper:
    def __init__(self):
        self.color = (255, 255, 255)
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.radius = 20
        self.velocity = [0, -10]
        self.on_ground = False

    def update(self):
        self.velocity[1] += game['acceleration']
        self.position[1] += self.velocity[1]

    def jump(self):
        self.velocity[1] = -10

jumper = Jumper()

# --------------------------
# Sub programs
# --------------------------

def handle_input():
    """ This sub-program will listen for user inputs and make changes to the objects depending on
        inputs"""
    # This checks to see if the pygame window has been closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Change horizontal movement
    if keys[pygame.K_LEFT]:
        player1['horizontal_move'] = 'left'
    elif keys[pygame.K_RIGHT]:
        player1['horizontal_move'] = 'right'
    else:
        player1['horizontal_move'] = None
    # Change vertical movement
    if keys[pygame.K_UP]:
        player1['vertical_move'] = 'up'
    elif keys[pygame.K_DOWN]:
        player1['vertical_move'] = 'down'
    else:
        player1['vertical_move'] = None

    # Launch the target if the Enter key is pressed
    if keys[pygame.K_RETURN] and target['status'] == 'ready':
        target['status'] = 'launched'
        player1['shot_ready'] = True

    if keys[pygame.K_SPACE] and player1['shot_ready']:
        player1['shots'] -= 1
        player1['shot_ready'] = False
        if player1['on_target']:
            player1['score'] += 10
            reset_target()

    if keys[pygame.K_x]:
        jumper.jump()
    # keeps game_loop going
    return True


def update():
    # update player1 position
    if player1['horizontal_move'] == 'left' and player1['x'] > 0:
        player1['x'] -= player1['speed']
    elif player1['horizontal_move'] == 'right' and player1['x'] < SCREEN_WIDTH:
        player1['x'] += player1['speed']
    if player1['vertical_move'] == 'up' and player1['y'] > 0:
        player1['y'] -= player1['speed']
    elif player1['vertical_move'] == 'down' and player1['y'] < SCREEN_HEIGHT:
        player1['y'] += player1['speed']

    # update target position if it has been launched
    if target['status'] == 'launched':
        target['v_y'] += game['acceleration']
        target['x'] += target['v_x']
        target['y'] += target['v_y']

    # Check if target has finished it's path and if so reset it.
    if target['y'] > SCREEN_HEIGHT or target['x'] > SCREEN_WIDTH:
        reset_target()

    # Check if the player is touching the target (collision check)
    if find_square_distance(player1, target) < (player1['radius'] + target['radius']) ** 2:
        player1['on_target'] = True
    else:
        player1['on_target'] = False

    jumper.update()


def reset_target():
    target['y'] = SCREEN_HEIGHT - 5
    target['x'] = 0
    target['v_y'] = randint(-30, -15)
    target['v_x'] = randint(10, 15)
    target['status'] = 'ready'
    # if the player has not fired their shot yet, they lose 1 shot
    if player1['shot_ready']:
        player1['shots'] -= 1
    # Check if the player has no shots left, if so set game_over to True
    if player1['shots'] == 0:
        game['game_over'] = True


def find_square_distance(a, b):
    return (a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2


def draw():
    # Clear the screen
    screen.fill(background_colour)

    if not game['game_over']:
        # Draw Player 1
        pygame.draw.circle(screen, player1['color'], (player1['x'], player1['y']), player1['radius'])

        # Draw target
        pygame.draw.circle(screen, target['color'], (target['x'], target['y']), target['radius'])

        # Draw jumper
        pygame.draw.circle(screen, jumper.color, jumper.position, jumper.radius)

    else:
        game_over_text = font_large.render(f"Game Over", True, (255, 255, 255))
        continue_text = font.render(f"Press Enter to Play Again", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.4))
        screen.blit(continue_text, (SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.6))

    # Draw the score and the shots
    score_text = font.render(f"Score = {player1['score']}", True, (255, 255, 255))
    shots_text = font.render(f"Shots left = {player1['shots']}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.02))
    screen.blit(shots_text, (SCREEN_WIDTH * 0.7, SCREEN_HEIGHT * 0.02))

    # Update the display
    pygame.display.flip()


# --------------------------
# Main Program
# --------------------------

# Main game loop
running = True
while running:
    running = handle_input()
    update()
    draw()

    # Keeps the game running at a constant frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()
