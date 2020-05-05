import numpy as np
import pygame as pg


# define pg parameters
pg.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
TILE_SIZE = 50
COLOR_BLANK_TILE = pg.Color('black')
COLOR_INACTIVE_TILE = pg.Color('white')
COLOR_ACTIVE_TILE = pg.Color('lightblue')
COLOR_ACTIVE_WORD = pg.Color('azure2')
TEXT_COLOR = pg.Color('black')
INCORRECT_COLOR = pg.Color('red')
BORDER_COLOR = pg.Color('black')
BORDER_WIDTH = 1
FONT = pg.font.Font(None, TILE_SIZE)
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))


# depending on the layout of the tiles, methods in this class will enable each tile
# to "figure out" whether or not it is part of a word, and which way the word goes

# tile_grid is 2D array of Tiles (represented by characters below):
# [['w', 'a', 'r', 'm', 'e', 'd'],
#  ['a', 'l', 'o', 'e', '', 'o'],
#  ['s', 'e', 'd', 'g', 'e', 's'], 
#  ['p', '', '', 'a' , 'l', 'e'],
#  ['s', 'a', 'p', '', 'm', 'e']])

# the class takes in a grid of np.array([[...], [...])
# to initialize the tiles and their locations, and their behavior

# each tile is at MOST a part of two words 
# this doesn't need to be a class attribute: 
# the tile will figure out how many words it is a part of based on the layout

# when user clicks a tile, the across grid lights up
class Grid:
    def __init__(self, letter_grid, x_start = 0, y_start = 0):
        self.x_start = x_start
        self.y_start = y_start
        self.tile_grid = np.empty([letter_grid.shape[0], letter_grid.shape[1]], dtype=object)
        # these two attributes will be changed during events in the game
        self.row_col_tuple = (None, None)
        print(self.tile_grid)
        self.buildGrid(letter_grid)

    # build_grid will initialize the 2D array of tile objects
    # ... and determine self.rect as well for each tile
    # 
    def buildGrid(self, letter_grid):
        # might consider vectorization for readability
        # each tile has a (x,y) position 
        for i in range(0, letter_grid.shape[0]):
            for j in range(0, letter_grid.shape[1]):
                self.tile_grid[i][j] = Tile(
                    x=self.x_start+j*TILE_SIZE, 
                    y=self.y_start+i*TILE_SIZE, 
                    actual_letter=letter_grid[i][j])
        self.setTileDirections()
        # self.printTiles()

    # default is the across position for whatever word the tile is a part of

    # remember to check BOTH neighboring tiles except for first row/column, last row/column
    def setTileDirections(self):
        # i goes through the rows
        for i in range(0, self.tile_grid.shape[0]):
            # j goes through the columns in each row
            for j in range(0, self.tile_grid.shape[1]):
                if (self.tile_grid[i][j].actual_letter != ''):
                    # check the first row
                    if i == 0:
                        # check the first column
                        if j == 0:
                            if (self.tile_grid[i][j+1].actual_letter != ''): self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i+1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True
                        # check the last column
                        elif j == self.tile_grid.shape[0] - 1:
                            if (self.tile_grid[i][j-1].actual_letter != ''): self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i+1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True
                        # check the interior of the first row
                        else:
                            if (self.tile_grid[i][j-1].actual_letter != '') or (self.tile_grid[i][j+1].actual_letter != ''):
                                self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i+1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True

                    # check the last row
                    elif i == self.tile_grid.shape[0] - 1:
                        # check the first column
                        if j == 0:
                            if (self.tile_grid[i][j+1].actual_letter != ''): self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i-1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True
                        # check the last column
                        elif j == self.tile_grid.shape[1] - 1:
                            print('checking the last column of the last row:', i, j)
                            if (self.tile_grid[i][j-1].actual_letter != ''): self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i-1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True
                                # setting last row, last column as vertical
                        # check the interior columns of the last row
                        else:
                            # print('checking the interior columns of the last row')
                            # print('i =', i, 'j =', j)
                            if (self.tile_grid[i][j-1].actual_letter != '') or (self.tile_grid[i][j+1].actual_letter != ''):
                                self.tile_grid[i][j].is_horizontal = True
                            if (self.tile_grid[i-1][j].actual_letter != ''): self.tile_grid[i][j].is_vertical = True

                    # check the first column (but only need to check interior now)
                    elif j == 0:
                        if self.tile_grid[i][j+1].actual_letter != '': self.tile_grid[i][j].is_horizontal = True
                        if (self.tile_grid[i-1][j].actual_letter != '') or (self.tile_grid[i+1][j].actual_letter != ''):
                            self.tile_grid[i][j].is_vertical = True

                    # check last column, interior rows
                    elif j == self.tile_grid.shape[1] - 1:
                        if self.tile_grid[i][j-1].actual_letter != '': self.tile_grid[i][j].is_horizontal = True
                        if (self.tile_grid[i-1][j].actual_letter != '') or (self.tile_grid[i+1][j].actual_letter != ''):
                            self.tile_grid[i][j].is_vertical = True

                    # all other interior rows and interior columns 
                    else:
                        if (self.tile_grid[i][j-1].actual_letter != '') or (self.tile_grid[i][j+1].actual_letter != ''):
                            self.tile_grid[i][j].is_horizontal = True
                        if (self.tile_grid[i-1][j].actual_letter != '') or (self.tile_grid[i+1][j].actual_letter != ''):
                            self.tile_grid[i][j].is_vertical = True

                # the display tile is not a letter!
                else: 
                    self.tile_grid[i][j].background_color = COLOR_BLANK_TILE
        # self.printTiles()

    def printTiles(self):
        for i in range(0, self.tile_grid.shape[0]):
            for j in range(0, self.tile_grid.shape[1]):
                if self.tile_grid[i][j].is_horizontal and self.tile_grid[i][j].is_vertical:
                    print(self.tile_grid[i][j].actual_letter, ': h, v')
                elif self.tile_grid[i][j].is_horizontal and not self.tile_grid[i][j].is_vertical:
                    print(self.tile_grid[i][j].actual_letter, ': h')
                elif not self.tile_grid[i][j].is_horizontal and self.tile_grid[i][j].is_vertical:
                    print(self.tile_grid[i][j].actual_letter, ': v')
                else: print("Blank tile: neither horizontal nor vertical")
    
    # when tiles are being updated... between clicks or otherwise...
    # this resets all tile colors and attributes EXCEPT for any tiles located at (i, j)
    # since we need to know if a tile was clicked in order to change directions

    # has the option to leave out a tile by tuple dimension
    # default is to leave out a tile located at (-1, -1)... which doesn't leave out any tiles
    def resetTiles(self, leave_out = (-1, -1)):
        for i in range(0, self.tile_grid.shape[0]):
            for j in range(0, self.tile_grid.shape[1]):
                if i == leave_out[0] and j == leave_out[1]:
                    continue
                elif (self.tile_grid[i][j].actual_letter != ''): 
                    self.tile_grid[i][j].background_color = COLOR_INACTIVE_TILE
                    self.tile_grid[i][j].word_active = False
                    self.active = False
                    self.active_horizontal = False 
                    self.active_vertical = False 

    # these two helper functions take in a location on the grid (i,j), 
    # and set the neighboring tiles depending on whether we want to set horizontal/vertical
    def setHorizontalTiles(self, i, j):
        # change the current tile to be active and horizontal
        self.tile_grid[i][j].word_active = True
        self.tile_grid[i][j].background_color = COLOR_ACTIVE_TILE
        self.tile_grid[i][j].active_horizontal = True
        self.tile_grid[i][j].active_vertical = False
        # loop backwards within the row to find other tiles that are part of the same word
        for k in range(j-1, -1, -1):
            if self.tile_grid[i][k].is_horizontal and (self.tile_grid[i][k].actual_letter != ''):
                self.tile_grid[i][k].word_active = True
                self.tile_grid[i][k].background_color = COLOR_ACTIVE_WORD
            else: break
        # loop forwards within the row to find other tiles that are part of the same word
        for k in range(j+1, self.tile_grid.shape[1]):
            if self.tile_grid[i][k].is_horizontal and self.tile_grid[i][k].actual_letter != '':
                self.tile_grid[i][k].word_active = True
                self.tile_grid[i][k].background_color = COLOR_ACTIVE_WORD
            else: break

    def setVerticalTiles(self, i, j):
        # change the current tile to be active and vertical
        self.tile_grid[i][j].word_active = True
        self.tile_grid[i][j].background_color = COLOR_ACTIVE_TILE
        self.tile_grid[i][j].active_horizontal = False
        self.tile_grid[i][j].active_vertical = True
        # loop backwards within the column to find other tiles that are part of the same word
        for k in range(i-1, -1, -1):
            if self.tile_grid[k][j].is_vertical and self.tile_grid[k][j].actual_letter != '':
                self.tile_grid[k][j].word_active = True
                self.tile_grid[k][j].background_color = COLOR_ACTIVE_WORD
            else: break
        # loop forwards within the column to find other tiles that are part of the same word
        for k in range(i+1, self.tile_grid.shape[0]):
            if self.tile_grid[k][j].is_vertical and self.tile_grid[k][j].actual_letter != '':
                self.tile_grid[k][j].word_active = True
                self.tile_grid[k][j].background_color = COLOR_ACTIVE_WORD
            else: break

    # this function finds the next horizontal tile using recursion:
    # it calls itself again if the next tile over is blank
    def setNextHorizontalTile(self, i, j):
        # if you are at the end of a column of a horizontal word
        self.resetTiles()
        if j == self.tile_grid.shape[1] - 1:
            if self.tile_grid[i][j+1].word_active and self.tile_grid[i][j+1].actual_letter != '':
                if self.tile_grid[i+1][0].is_horizontal:
                    # self.resetTiles()
                    self.setHorizontalTiles(i+1, 0)
                elif self.tile_grid[i+1][0].is_vertical:
                    # self.resetTiles()
                    self.setVerticalTiles(i+1, 0)
                # if the next horizontal tile is blank, call the function on the next tile                 
                elif self.tile_grid[i][j+1].actual_letter == '':
                    self.setNextHorizontalTile(i, j+1)

            # the next tile is part of the same word...
        elif self.tile_grid[i][j+1].word_active and self.tile_grid[i][j+1].actual_letter != '':
            if self.tile_grid[i][j+1].is_horizontal:
                # self.resetTiles()
                self.setHorizontalTiles(i, j+1)
            elif self.tile_grid[i][j+1].is_vertical:
                # self.resetTiles()
                self.setVerticalTiles(i, j+1)

        # the next tile is a blank letter! oh no! 
        elif self.tile_grid[i][j+1].actual_letter != '':
            # self.resetTiles()
            self.setNextHorizontalTile(i, j+1)

    def handle_event(self, event):
        # when the user clicks, every tile is looped through to detect where they clicked
        if (event.type == pg.MOUSEBUTTONDOWN):
            for i in range(0, self.tile_grid.shape[0]):
                for j in range(0, self.tile_grid.shape[1]):
                    # if previously clicked, it must change directions: 
                    # horizontal --> vertical, vertical --> horizontal

                    if self.tile_grid[i][j].rect.collidepoint(event.pos) and (self.tile_grid[i][j].actual_letter != ''):
                        # if a tile is clicked on, it is both active and part of an active word
                        self.tile_grid[i][j].word_active = True
                        self.tile_grid[i][j].active = True
                        
                        # no tiles have been clicked previously but this one is horizontal
                        if self.tile_grid[i][j].is_horizontal and self.row_col_tuple == (None, None):
                            self.row_col_tuple = (i,j)
                            self.setHorizontalTiles(i,j)

                        # no tiles have been clicked previously but this one is vertical
                        elif self.tile_grid[i][j].is_vertical and self.row_col_tuple == (None, None): 
                            self.row_col_tuple = (i,j)
                            self.setVerticalTiles(i,j)

                        # tiles HAVE been clicked previously but not the same one 
                        # reset ALL of the tiles except the tile clicked
                        # then highlight word for whichever direction this new tile is in
                        elif (i,j) != self.row_col_tuple:
                            self.row_col_tuple = (i,j)
                            self.resetTiles(leave_out = (i,j))
                            if self.tile_grid[i][j].is_horizontal:
                                self.setHorizontalTiles(i,j)
                            elif self.tile_grid[i][j].is_vertical:
                                self.setVerticalTiles(i,j)
                        
                        # tile was clicked previously AND it is the same one:
                        # then we need to change directions: 
                        # horizontal --> vertical
                        # vertical --> horizontal
                        elif (i,j) == self.row_col_tuple:
                            self.row_col_tuple = (i,j)
                            self.resetTiles(leave_out = (i, j)) 

                            # if the tile can go both ways, then have it switch directions
                            # if the same tile was previously horizontal, then it switches to vertical
                            # if the same tile was previously vertical, then it switches to horizontal
                            if self.tile_grid[i][j].is_horizontal and self.tile_grid[i][j].is_vertical:  
                                if self.tile_grid[i][j].active_horizontal == True:
                                    self.setVerticalTiles(i,j)
                                elif self.tile_grid[i][j].active_vertical == True:
                                    self.setHorizontalTiles(i,j)

                            # the tile is only horizontal --> set horizontal tiles and don't change direction
                            elif self.tile_grid[i][j].is_horizontal and not self.tile_grid[i][j].is_vertical:
                                self.setHorizontalTiles(i,j)

                            # the tile is only vertical --> set vertical tiles and don't change direction
                            elif not self.tile_grid[i][j].is_horizontal and self.tile_grid[i][j].is_vertical:
                                self.setVerticalTiles(i,j)
                            else:
                                print("Runtime error: tile is neither horizontal nor vertical.")
                                break
                        else: 
                            print("Runtime Error: figure out how this line printed")
                            break

                    elif self.tile_grid[i][j].actual_letter == '':
                        self.tile_grid[i][j].background_color = COLOR_BLANK_TILE
                    # for other tiles not affected by the mouseclick event...
                    else:
                        continue

        # self.printTiles()
        # KEYDOWN takes you to the next tile... depending on your direction
        elif event.type == pg.KEYDOWN:
            for i in range(0, self.tile_grid.shape[0]):
                for j in range(0, self.tile_grid.shape[1]):
                    # this is necessary so if you click somewhere else and type, nothing happens
                    if self.tile_grid[i][j].active == True:
                        if pg.K_a <= event.key <= pg.K_z:
                            # set the tile to the letter and move forward
                            self.tile_grid[i][j].disp_letter = event.unicode

                            # if you are on a tile that is part of a horizontal word...
                            if self.tile_grid[i][j].is_horizontal == True:
                                print("setting next horizontal tile")
                                self.setNextHorizontalTile(i,j)

                    else: continue
                break

        self.update_grid(event)

    def update_grid(self, event):
        # redraw the tiles for a word whenever there is an event
        for i in range(0, self.tile_grid.shape[0]):
            for j in range(0, self.tile_grid.shape[1]):
                self.tile_grid[i][j].handle_event(event)
                self.tile_grid[i][j].draw(screen)

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

    setup_grid = np.array(
        [['w', 'a', 'r', 'm', 'e', 'd'],
        ['a', 'l', 'o', 'e', '', 'o'],
        ['s', 'e', 'd', 'g', 'e', 's'], 
        ['t', '', '', '' , '', ''],
        ['e', 'r', 'a', 's', 'e', 'd'],
        ['r', 'a', 'p', 'p', 'e', 'r'],
        ['s', '', 'p', 'a', 'p', '']])

    sample_grid = Grid(setup_grid, x0, y0)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            screen.fill((30, 30, 30))

            sample_grid.handle_event(event)
            # sample_word.handle_event(event)
            # sample_word_2.handle_event(event)
            # sample_word_3.handle_event(event)

            pg.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    main()
    pg.quit()