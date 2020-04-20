import pygame as pg
from string import ascii_lowercase
from itertools import cycle 

pg.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TILE_SIZE = 32
COLOR_INACTIVE_TILE = pg.Color('white')
COLOR_ACTIVE_TILE = pg.Color('lightblue')
COLOR_ACTIVE_WORD = pg.Color('azure2')
TEXT_COLOR = pg.Color('black')
INCORRECT_COLOR = pg.Color('red')
BORDER_COLOR = pg.Color('black')
BORDER_WIDTH = 1
FONT = pg.font.Font(None, 32)
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))


# Word contains a list of tiles, oriented either 'across' or 'down' specified by direciton attribute
# 4/19/20: Updated up-down-left-right key functionality
class Word:
    def __init__(self, x_start, y_start, actual_word, direction = 'across', tile_size = TILE_SIZE):
        self.x_start = x_start
        self.y_start = y_start 
        self.actual_word = actual_word
        self.direction = direction
        self.tile_size = tile_size
        # self.rect depends on the orientation 'across' or 'down'
        if direction == 'across':
            self.rect = pg.Rect(x_start, y_start, tile_size*len(actual_word), tile_size)
        if direction == 'down':
            self.rect = pg.Rect(x_start, y_start, tile_size, tile_size*len(actual_word))
        self.active = False
        self.word_tiles = []
        self.build()
    def build(self):
        for index, letter in enumerate(self.actual_word):
            if self.direction == 'across':
                self.word_tiles.append(Tile(self.x_start + index*(self.tile_size - BORDER_WIDTH), self.y_start, 
                    self.tile_size, self.tile_size, '', self.actual_word[index]))
            if self.direction == 'down':
                self.word_tiles.append(Tile(self.x_start, self.y_start + index*(self.tile_size - BORDER_WIDTH), 
                    self.tile_size, self.tile_size, '', self.actual_word[index]))
    def showTiles(self):
        for index, tile in enumerate(self.word_tiles):
            print('Tile', tile.actual_letter, ':', getattr(tile, 'active'))

    # Note: this function runs constantly in the background 
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # if the user clicks into the word
            if self.rect.collidepoint(event.pos):
                 # Toggle the word_active attribute for the group of tiles of the word
                for tile in self.word_tiles:
                    setattr(tile, 'word_active', True)
                    setattr(tile, 'background_color', COLOR_ACTIVE_TILE)
            else:
                for tile in self.word_tiles:
                    setattr(tile, 'word_active', False)
            self.showTiles()
            self.update_word(event)
        ## implemented left-right arrow keys 
        elif event.type == pg.KEYDOWN:
            if (self.direction == 'across') and (event.key == pg.K_RIGHT):
                print('right arrow key pressed')
                for index, tile in enumerate(self.word_tiles):
                    if index == len(self.word_tiles) - 1 and getattr(tile, 'active'):
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[0], 'active', True)
                        setattr(self.word_tiles[0], 'background_color', COLOR_ACTIVE_TILE)
                    elif getattr(tile, 'active') == True:
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index + 1], 'active', True)
                        setattr(self.word_tiles[index + 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            elif (self.direction == 'across') and (event.key == pg.K_LEFT):
                print('left arrow key pressed')
                for index, tile in enumerate(self.word_tiles):
                    if index == 0 and getattr(tile, 'active'):
                        print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[0], 'active', False)
                        setattr(self.word_tiles[0], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[-1], 'active', True)
                        setattr(self.word_tiles[-1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    elif getattr(tile, 'active') == True:
                        print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index - 1], 'active', True)
                        setattr(self.word_tiles[index - 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            elif (self.direction == 'down') and (event.key == pg.K_DOWN):
                # print('down arrow key pressed')
                for index, tile in enumerate(self.word_tiles):
                    if index == len(self.word_tiles) - 1 and getattr(tile, 'active'):
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[0], 'active', True)
                        setattr(self.word_tiles[0], 'background_color', COLOR_ACTIVE_TILE)
                    elif getattr(tile, 'active') == True:
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index + 1], 'active', True)
                        setattr(self.word_tiles[index + 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            elif (self.direction == 'down') and (event.key == pg.K_UP):
                # print('up arrow key pressed')
                for index, tile in enumerate(self.word_tiles):
                    if index == 0 and getattr(tile, 'active'):
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[0], 'active', False)
                        setattr(self.word_tiles[0], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[-1], 'active', True)
                        setattr(self.word_tiles[-1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    elif getattr(tile, 'active') == True:
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index - 1], 'active', True)
                        setattr(self.word_tiles[index - 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            # backspace should act similarly to left arrow / up arrow
            # the event already acts on the tile class, so no need to change the disp_letter attribute
            # direction of the word does NOT need to be specified since indexing of the word works either way
            elif event.key == pg.K_BACKSPACE:
                for index, tile in enumerate(self.word_tiles):
                    if index == 0 and getattr(tile, 'active'):
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        # the following line is redundant since backspace event is a tile event? 
                        ### something is wrong as this line isn't being executed
                        setattr(self.word_tiles[index], 'disp_letter', '')
                        ###
                        setattr(self.word_tiles[-1], 'active', True)
                        setattr(self.word_tiles[-1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    elif getattr(tile, 'active') == True:
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index], 'disp_letter', '')
                        setattr(self.word_tiles[index - 1], 'active', True)
                        setattr(self.word_tiles[index - 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            # typing any other letter behaves similarly to right/down arrow
            # when you type in a letter, the tile should no longer be active
            # this is irregardless of direction 
            elif pg.K_a <= event.key <= pg.K_z:
                for index, tile in enumerate(self.word_tiles):
                    if index == len(self.word_tiles) - 1 and getattr(tile, 'active'):
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index], 'disp_letter', event.unicode)
                        setattr(self.word_tiles[0], 'active', True)
                        setattr(self.word_tiles[0], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    elif getattr(tile, 'active') == True:
                        # print('found active tile:', tile.actual_letter)
                        setattr(tile, 'active', False)
                        setattr(self.word_tiles[index], 'active', False)
                        setattr(self.word_tiles[index], 'background_color', COLOR_ACTIVE_WORD)
                        setattr(self.word_tiles[index], 'disp_letter', event.unicode)
                        setattr(self.word_tiles[index + 1], 'active', True)
                        setattr(self.word_tiles[index + 1], 'background_color', COLOR_ACTIVE_TILE)
                        break
                    else: pass
            # update the tiles, redrawing each of them
            self.showTiles()
            self.update_word(event)
        else: self.update_word(event)
    # Note: update_word will run constantly
    def update_word(self, event):
        # redraw the tiles for a word whenever there is an event
        for tile in self.word_tiles:
            tile.handle_event(event)
            tile.draw(screen)
                        
# current fixes: two words that share a letter are problematic 
# we can layer the two words by changing the order in which we draw them, 
# and alternate the layer depending on which word is selected? --> this might select both words

# two clicks in a row on a letter will activate the other word if the letter is shared between two words?

# each tile has a background color rectangle drawn with no border,
# followed by a black border which is a rectangle of width = 1
# followed by the text 

# tiles do not "know" about other tiles
class Tile:
    border_color = BORDER_COLOR
    def __init__(self, x, y, w, h, disp_letter='', actual_letter=''):
        self.rect = pg.Rect(x, y, w, h)
        self.disp_letter = disp_letter
        self.actual_letter = actual_letter
        self.background_color = COLOR_INACTIVE_TILE
        self.txt_surface = FONT.render(disp_letter, True, TEXT_COLOR)
        self.active = False
        self.word_active = False # is the tile part of an active word 
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked into the tile
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                print('you clicked on the tile', self.actual_letter)
                self.active = not self.active
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
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        self.check()

    # if the letter is wrong, it rerenders the color of the letter to red
    def check(self):
        if self.disp_letter != self.actual_letter:
            self.txt_surface = FONT.render(self.disp_letter, True, INCORRECT_COLOR)
        else:
            self.txt_surface = FONT.render(self.disp_letter, True, TEXT_COLOR)

def main():
    clock = pg.time.Clock()
    done = False

    x0, y0 = 10, 10
    sample_word = Word(x0, y0, 'abcdefghijk', 'across')
    # sample_word_2 = Word(x0, y0 + 2*TILE_SIZE, 'tiffany', 'across')
    sample_word_2 = Word(x0, y0 + 2*TILE_SIZE, 'henlo', 'down')

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            screen.fill((30, 30, 30))

            sample_word.handle_event(event)
            sample_word_2.handle_event(event)

            pg.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    main()
    pg.quit()