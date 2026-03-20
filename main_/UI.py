import pygame
import time
from inventory import Inventory, Item
from utils import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
TILE_SIZE = 64
FPS = 60

class Text:
    """
    The class to represent a text object drawn on the screen.

    Attributes
    ----------
        lines : list[str] / None
            a list of lines if the text is written on multiple lines, otherwise None

        font : Font
            an instance of the font class,
            module that allows loading and rendering fonts

        text : Surface
            desired text saved on a surface

        coordinates : tuple[int, int]
            position where the text will be drawn on screen

        text_rect : Rect
            An instance of the rect class
            helps with displaying the text on the game screen

    Methods
    -------
        draw(surface):
            draws the text onto the given surface,
            handles multi-line text if applicable
    """

    def __init__(self, text, size, coordinates, colour=(255, 255, 255)):
        if '\n' in text:
            self.lines = text.split("\n")
        else:
            self.lines = None

        self.font = pygame.font.SysFont('Arial', size)
        self.text = self.font.render(text, True, colour)
        self.coordinates = coordinates
        self.text_rect = self.text.get_rect(center=self.coordinates)

    def draw(self, surface):
        if self.lines != None:
            x, y = self.coordinates[0], self.coordinates[1]
            line_height = self.font.get_height()

            for i, line in enumerate(self.lines):
                rendered_line = self.font.render(line, True, (255, 255, 255))
                surface.blit(rendered_line, (x, y + i * line_height))
        else:
            pos = (self.text_rect.x, self.text_rect.y)
            surface.blit(self.text, pos)


class Menu:
    """
    The class that manages all menus displayed throughout the game.

    Attributes
    ----------
        game : Game
            an instance of the game class,
            gives access to the main game class attributes

        pause_bg : Surface
            an instance of the surface class,
            the background image displayed when the game is paused

        pause_bg_rect : Rect
            an instance of the rect class,
            helps with positioning pause background on the screen

        start_bg : Surface
            an instance of the surface class,
            the background image displayed on the start screen

        start_bg_rect : Rect
            an instance of the rect class,
            helps with positioning start background on the screen

        death_bg : Surface
            an instance of the surface class,
            the background image displayed when the player dies

        death_bg_rect : Rect
            an instance of the rect class,
            helps with positioning death background on the screen

        start : Button
            an instance of the button class,
            the button that initiates the game from the start screen

        resume : Button
            an instance of the button class,
            the button that closes the currently opened menu

        settings : Button
            an instance of the button class,
            the button that opens the settings menu

        save : Button
            an instance of the button class,
            the button that saves the current progress of the user

        load : Button
            an instance of the button class,
            the button that loads the data from the last save file

        quit : Button
            an instance of the button class,
            the button that closes the game

        sounds_plus : Button
            an instance of the button class,
            the button that increases the volume

        sounds_minus : Button
            an instance of the button class,
            the button that decreases the volume

        starting_menu_flag : bool
            checks if the starting menu should be displayed

        settings_flag : bool
            checks if the settings menu should be displayed

        death_screen_flag : bool
            checks if the death screen should be displayed

        ending_screen_flag : bool
            checks if the ending screen should be displayed

        inventory_flag : bool
            checks if the inventory should be displayed

        tooltip_flag : bool
            checks if a tooltip should be displayed

        pause_flag : bool
            checks if the pause menu should be displayed

        saved : int
            helps with confirmation of the saving process

        last_update : int
            helps with the cooldown of equipping a new weapon

        inventory : Inventory
            an instance of the inventory class,
            manages the player's collected items and has 27 slots

        tooltip_surf : Surface
            an instance of the surface class,
            used to render the details of the item on

        tooltip_rect : Rect
            an instance of the rect class,
            helps with displaying the tooltip on the inventory menu

    Methods
    -------
        start_menu():
            displays the start screen and handles its button interactions

        pause_menu():
            displays the pause menu and handles its button interactions

        settings_menu():
            displays the settings menu and handles its button interactions

        death_screen():
            displays the death screen and handles its button interactions

        inventory_menu():
            displays the inventory and handles equipping, dropping and tooltip display

        ending_screen():
            displays the ending screen when the player completes all available levels

        saving():
            serialises and saves the current game state to a JSON file

        loading():
            loads the last saved game state from a JSON file
    """

    def __init__(self, parent_class):
        self.game = parent_class
        self.pause_bg = pygame.image.load('assets/menu/background.png')
        self.pause_bg = pygame.transform.scale(self.pause_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pause_bg_rect = self.pause_bg.get_rect()
        self.start_bg = pygame.image.load('assets/menu/start_screen.png')
        self.start_bg = pygame.transform.scale(self.start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_bg_rect = self.start_bg.get_rect()
        self.death_bg = pygame.image.load('assets/menu/death_screen.png')
        self.death_bg = pygame.transform.scale(self.death_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.death_bg_rect = self.death_bg.get_rect()

        self.start = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/start.png', 5)
        self.resume = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 250, f'assets/menu/buttons/resume.png', 5)
        self.settings = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150, f'assets/menu/buttons/settings.png', 5)
        self.save = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50, f'assets/menu/buttons/save.png', 5)
        self.load = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 50, f'assets/menu/buttons/restart.png', 5)
        self.exit = Button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 150, f'assets/menu/buttons/quit.png', 5)
        self.sounds_plus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 175,
                                  f'assets/menu/buttons/arrow_up.png', 5)
        self.sounds_minus = Button((SCREEN_WIDTH // 2) + 300, (SCREEN_HEIGHT // 2) - 75,
                                   f'assets/menu/buttons/arrow_down.png', 5)

        self.starting_menu_flag = True
        self.settings_flag = False
        self.death_screen_flag = False
        self.ending_screen_flag = False
        self.inventory_flag = False
        self.tooltip_flag = False
        self.pause_flag = False
        self.saved = 0

        self.last_update = 0

        self.inventory = Inventory(27)

        self.tooltip_text = Text('', 50, (0, 0), (255, 255, 255))
        self.tooltip_surf = pygame.Surface((500, 200), pygame.SRCALPHA).convert_alpha()
        self.tooltip_rect = self.tooltip_surf.get_rect()
        self.tooltip_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def start_menu(self):
        if self.settings_flag:
            self.settings_menu()

        else:
            self.buttons = [self.start, self.settings, self.load, self.exit]

            self.game.screen.blit(self.start_bg, self.start_bg_rect)
            for button in self.buttons:
                button.collision = True
                button.draw_and_collision(self.game.screen)

            if self.start.active:
                self.starting_menu_flag = False

            if self.settings.active:
                self.settings_flag = True

            if self.load.active:
                self.loading()

                self.starting_menu_flag = False

            if self.exit.active:
                self.game.running = False
                self.starting_menu_flag = False

            for button in self.buttons:
                button.collision = False

    def pause_menu(self):
        self.pause_flag = True
        self.buttons = [self.resume, self.settings, self.save, self.load, self.exit]
        paused = Text('Paused', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))

        self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        paused.draw(self.game.screen)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)

        if self.resume.active and not self.settings_flag:
            self.pause_flag = False

        if self.settings.active:
            self.settings_flag = True

        if self.settings_flag:
            self.settings_menu()

        if self.save.active:
            self.saving()

        if self.saved * FPS > 0:
            text = Text('Saved Successfully', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 400))
            text.draw(self.game.screen)
            self.saved -= 1

        if self.load.active:
            self.loading()

            self.pause_flag = False

        if self.exit.active:
            self.game.running = False
            self.pause_flag = False

        for button in self.buttons:
            button.collision = False

    def settings_menu(self):
        self.buttons = [self.resume, self.sounds_plus, self.sounds_minus]
        settings = Text('Settings', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 400))
        volume = Text(f'Volume: {int(self.game.volume * 100)}', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 125))
        controls = Text('A - move left \nD - move right \nSPACE - jump \nESC - pause \nI - open inventory \nLEFT MOUSE BUTTON - melee attack \nRIGHT MOUSE BUTTON - fireball \n \nIn the inventory: \n \nLEFT MOUSE BUTTON - equip \nRIGHT MOUSE BUTTON - drop \nI - close inventory', 20, (SCREEN_WIDTH // 2 - 450, SCREEN_HEIGHT // 2))

        self.game.screen.blit(self.pause_bg, self.pause_bg_rect)
        settings.draw(self.game.screen)
        volume.draw(self.game.screen)
        controls.draw(self.game.screen)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)
            time.sleep(0.0228)

        if self.resume.active:
            self.settings_flag = False
            time.sleep(0.1)

        if self.sounds_plus.active:
            if self.game.volume + 0.05 <= 1:
                self.game.volume += 0.05
            self.game.bg_music_channel.set_volume(self.game.volume)
            self.game.attack_channel.set_volume(self.game.volume)
            self.game.misc_channel.set_volume(self.game.volume)

        if self.sounds_minus.active:
            if self.game.volume - 0.05 >= 0:
                self.game.volume -= 0.05
            self.game.bg_music_channel.set_volume(self.game.volume)
            self.game.attack_channel.set_volume(self.game.volume)
            self.game.misc_channel.set_volume(self.game.volume)

        for button in self.buttons:
            button.collision = False
            button.active = False

    def death_screen(self):
        self.buttons = [self.settings, self.load, self.exit]

        self.game.screen.blit(self.death_bg, self.death_bg_rect)
        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)

        if self.settings.active:
            self.settings_flag = True
        if self.settings_flag:
            self.settings_menu()

        if self.load.active:
            self.loading()

            self.death_screen_flag = False

        if self.exit.active:
            self.game.running = False
            self.death_screen_flag = False

        for button in self.buttons:
            button.collision = False

    def inventory_menu(self):
        self.game.screen.fill((0, 0, 0))
        self.inventory.draw(self.game.screen)

        mouse_pos = pygame.mouse.get_pos()
        count = 0
        delay = 500
        current_time = pygame.time.get_ticks()

        if self.last_update == 0:
            self.last_update = current_time

        for item in self.inventory.slots:
            if item != None:
                if point_collision(mouse_pos, item.rect) and pygame.mouse.get_pressed()[0]:
                    if current_time - self.last_update > delay:
                        self.inventory.equip(count)
                        self.last_update = current_time

                if point_collision(mouse_pos, item.rect) and pygame.mouse.get_pressed()[2]:
                    self.inventory.drop(item)
                    self.tooltip_flag = False
                elif point_collision(mouse_pos, item.rect):
                    self.tooltip_flag = True
                    self.tooltip_text = Text(item.details(), 50, ((SCREEN_WIDTH // 2 - self.tooltip_rect.center[0], SCREEN_HEIGHT // 2 - self.tooltip_rect.center[1])),(255, 255, 255))
            count += 1

        if self.tooltip_flag:
            self.tooltip_surf.fill((255, 255, 255, 100))
            self.tooltip_text.draw(self.tooltip_surf)
            self.game.screen.blit(self.tooltip_surf, self.tooltip_rect)

    def ending_screen(self):
        self.buttons = [self.start, self.exit]
        text = Text('Thank you for playing', 50, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game.screen.fill((0, 0, 0))
        text.draw(self.game.screen)

        for button in self.buttons:
            button.collision = True
            button.draw_and_collision(self.game.screen)

        if self.start.active:
            self.ending_screen_flag = False
            self.game.level_count = 1

        if self.exit.active:
            self.game.running = False
            self.ending_screen_flag = False

    def saving(self):
        item_list = []
        for item in self.inventory.slots:
            if item != None:
                item_list.append({'name': item.name, 'img_path': item.img_path, 'damage': item.damage})
        write_json({'name': 'Vandi', 'level_count': self.game.level_count, 'inventory': item_list,
                    'weapon': {'name': self.inventory.weapon.name, 'img_path': self.inventory.weapon.img_path,
                               'damage': self.inventory.weapon.damage}}, 'vandi')
        self.saved = 10

    def loading(self):
        self.game.bg_music_channel.unpause()
        try:
            data = read_json('vandi')

            for item in self.inventory.slots:
                self.inventory.drop(item)

            for dict in data['inventory']:
                self.inventory.add(Item(dict['name'], dict['img_path'], dict['damage']))
            self.inventory.weapon = Item(data['weapon']['name'], data['weapon']['img_path'], data['weapon']['damage'])
            self.game.level_count = data['level_count']
            self.game.level_count_check = 0

            if self.game.level_count != self.game.level_count_check:
                self.game.level_count_check = self.game.level_count
                self.game.level_load()
        except:
            self.game.level_count_check = self.game.level_count
            self.game.level_load()


class Button:
    """
    The class to represent a clickable button in the game's menus.

    Attributes
    ----------
        image : Surface
            an instance of the surface class,
            contains the displayed model of the button

        rect : Rect
            an instance of the rect class,
            represents the hitbox of the button

        active : bool
            determines if the button has been pressed

        collision : bool
            checks if collision should be active
            depends on the self.active attribute

    Methods
    -------
        draw_and_collision(surface):
            draws the button onto the given surface and checks if it has been clicked,
            returns True if the button is clicked, False otherwise
    """
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.active = False
        self.collision = False

    def draw_and_collision(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

        mouse_pos = pygame.mouse.get_pos()

        self.active = False
        if point_collision(mouse_pos, self.rect) and self.collision:
            if pygame.mouse.get_pressed()[0] and not self.active:
                self.active = True

        return self.active

    def set_pos(self, pos):
        self.rect.center = pos