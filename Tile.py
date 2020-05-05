import numpy as np
import pygame as pg

# define pg parameters
pg.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TILE_SIZE = 50
COLOR_BLANK_TILE = pg.Color('black')
COLOR_INACTIVE_TILE = pg.Color('white')
COLOR_ACTIVE_TILE = pg.Color(154,0,255)
COLOR_ACTIVE_WORD = pg.Color(213,149,255)
TEXT_COLOR = pg.Color('black')
INCORRECT_COLOR = pg.Color('red')
BORDER_COLOR = pg.Color('black')
BORDER_WIDTH = 1
FONT = pg.font.Font(None, TILE_SIZE)
NUMBER_FONT = pg.font.Font(None, int(TILE_SIZE/4))
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

# two clicks in a row on a letter will activate the other word if the letter is shared between two words?

# the only parameters related to surrounding tiles are word_active, is_vertical, is_horizontal
# they also can't modify other tiles due to encapsulation of the tile class
class Tile:
    border_color = BORDER_COLOR
    def __init__(self, x, y, w = TILE_SIZE, h = TILE_SIZE, disp_letter='', actual_letter=''):
        self.rect = pg.Rect(x, y, w, h)
        self.disp_letter = disp_letter
        self.actual_letter = actual_letter
        self.background_color = COLOR_INACTIVE_TILE
        self.txt_surface = FONT.render(disp_letter, True, TEXT_COLOR)
        self.active = False
        self.word_active = False
        # these attributes are determined by the Grid class,
        # and each tile "knows" whether it is part of a horizontal word, vertical word, or neither
        self.is_horizontal = False
        self.is_vertical = False #
        # these attributes are to switch directions 
        # between horizontal/vertical for subsequent mouse clicks for an identical tile...
        self.active_horizontal = False 
        self.active_vertical = False

        # a number corresponding to a clue
        self.number = ''
        self.num_surface = NUMBER_FONT.render(self.number, True, TEXT_COLOR)

    def set_num_surface(self):
        self.num_surface = NUMBER_FONT.render(self.number, True, TEXT_COLOR)

    def handle_event(self, event):
        if (event.type == pg.MOUSEBUTTONDOWN) and (self.actual_letter != ''):
            # If the user clicked into the tile
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                print('you clicked on the tile', self.actual_letter)
                self.active = True
            else:
                self.active = False
            # Change the color of the background
            if self.word_active:
                if self.active:
                    print('Letter', self.actual_letter, 'is active')
                    self.background_color = COLOR_ACTIVE_TILE
                else:
                    print('Letter', self.actual_letter, 'is inactive')
                    self.background_color = COLOR_ACTIVE_WORD
            else:
                self.background_color = COLOR_INACTIVE_TILE
        # redraw the tile as needed
        self.check()

    def draw(self, screen):
        # we fill the rectangle and then draw the border and then the disp_letter over it 
        if self.active:
            pg.draw.rect(screen, self.background_color, self.rect, 0)
        else:
            pg.draw.rect(screen, self.background_color, self.rect, 0)
        pg.draw.rect(screen, self.border_color, self.rect, BORDER_WIDTH)
        # center the letters within the tile using (x,y) coordinates starting from upper left corner
        screen.blit(self.txt_surface, (self.rect.x+(TILE_SIZE/6), self.rect.y+(TILE_SIZE/5)))

        # set the number on top of the tile
        screen.blit(self.num_surface, (self.rect.x+(TILE_SIZE/10), self.rect.y+(TILE_SIZE/10)))
        self.check()

    # if the letter is wrong, it rerenders the color of the letter to red
    def check(self):
        if self.disp_letter != self.actual_letter:
            self.txt_surface = FONT.render(self.disp_letter, True, INCORRECT_COLOR)
        else:
            self.txt_surface = FONT.render(self.disp_letter, True, TEXT_COLOR)
