import numpy as np
import pygame as pg
from itertools import cycle
from Tile import Tile

pg.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 50
COLOR_BLANK_TILE = pg.Color('black')
COLOR_INACTIVE_TILE = pg.Color('white')

# purple for active tile, light purple for active word
COLOR_ACTIVE_TILE = pg.Color(154,0,255)
COLOR_ACTIVE_WORD = pg.Color(213,149,255)
TEXT_COLOR = pg.Color('black')
INCORRECT_COLOR = pg.Color('red')
BORDER_COLOR = pg.Color('black')
BORDER_WIDTH = 1
FONT = pg.font.Font(None, TILE_SIZE)
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

# tile_grid is 2D array of Tiles (represented by characters below):
# [['w', 'a', 'r', 'm', 'e', 'd'],
#  ['a', 'l', '', 'e', '', 'o'],
#  ['s', 'e', 'd', 'g', 'e', 's'], 
#  ['p', '', '', 'a' , 'l', 'e'],
#  ['s', 'a', 'p', '', 'm', 'e']])

# the class takes in a grid of np.array([[...], [...])
# to initialize the tiles and their locations, and their behavior

# each tile is at MOST a part of two words 
# the tile will figure out how many words it is a part of based on the layout

# helper function to loop through grid without double loop
# this allows both loops to be broken at the same time 
def loop_through_grid(m_end, n_end, m_start = 0, n_start = 0):
    for i in range(m_start, m_end):
        for j in range(n_start, n_end):
            yield i, j

# this creates an iterator to go forward through the (i,j) index
# Note: by switching start and end, we can make the iterator go backwards
def cycle_grid_horizontally(m_end, n_end, m_start = 0, n_start = 0, backwards = False):
    if backwards == True:
        grid_list = []
        for i in reversed(range(m_start, m_end)):
            for j in reversed(range(n_start, n_end)):
                grid_list.append([i,j])
        return cycle(grid_list)
    else:
        grid_list = []
        for i in range(m_start, m_end):
            for j in range(n_start, n_end):
                grid_list.append([i,j])
        return cycle(grid_list)

def cycle_grid_vertically(m_end, n_end, m_start = 0, n_start = 0, backwards = False):
    if backwards == True:
        grid_list = []
        for i in reversed(range(m_start, m_end)):
            for j in reversed(range(n_start, n_end)):
                grid_list.append([j,i])
        return cycle(grid_list)
    else:
        grid_list = []
        for i in range(m_start, m_end):
            for j in range(n_start, n_end):
                grid_list.append([j,i])
        return cycle(grid_list)

class Grid:
    def __init__(self, letter_grid, x_start = 0, y_start = 0):
        self.x_start = x_start
        self.y_start = y_start
        self.nrows = letter_grid.shape[0]
        self.ncols = letter_grid.shape[1]
        self.tile_grid = np.empty([self.nrows, self.ncols], dtype=object)

        # these two attributes will be changed during events in the game
        # row_col_tuple keeps track of the previous tile that was clicked
        self.row_col_tuple = (None, None)
        self.buildGrid(letter_grid)

    # build_grid will initialize the 2D array of tile objects
    # ... and determine self.rect as well for each tile
    # 
    def buildGrid(self, letter_grid):
        # might consider vectorization for readability
        # each tile has a (x,y) position 
        for i,j in loop_through_grid(self.nrows, self.ncols):
            self.tile_grid[i][j] = Tile(
                x=self.x_start+j*TILE_SIZE, 
                y=self.y_start+i*TILE_SIZE, 
                actual_letter=letter_grid[i][j])
        self.setTileDirections()
        self.setNumbers()
        # self.printTiles()

    # remember to check BOTH neighboring tiles except for first row/column, last row/column
    def setTileDirections(self):
        for i,j in loop_through_grid(self.nrows, self.ncols):
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

    # this sets the clue numbers for each word
    # we number only the first tile of each word
    def setNumbers(self):
        number = 1
        for i,j in loop_through_grid(self.nrows, self.ncols):
            if (self.tile_grid[i][j].actual_letter != ''):
                # check the first row
                if i == 0:
                    # check the first column
                    if j == 0:
                        # if there are horizontal tile after, then this is the first horizontal tile
                        if (self.tile_grid[i][j+1].actual_letter != '') and self.tile_grid[i][j+1].is_horizontal:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                        # if there is a vertical tile after, then this is the first vertical tile
                        elif (self.tile_grid[i+1][j].actual_letter != '') and self.tile_grid[i+1][j].is_vertical:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                        # we are horizontally behind a blank tile
                        elif self.tile_grid[i][j+1].actual_letter == '' and self.tile_grid[i+1][j].is_vertical:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                        else:
                            print("How did we get to this line? Debug.")

                    # for last column, only need to test vertical tile below
                    elif j == self.ncols - 1:
                        if self.tile_grid[i+1][j].is_vertical:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                    # check the interior of the first row
                    else:
                        # tile is first horizontal tile after blank
                        if (self.tile_grid[i][j-1].actual_letter == '') and self.tile_grid[i][j+1].is_horizontal:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                        # tile is first vertical tile after blank
                        elif self.tile_grid[i+1][j].is_vertical:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1

                # check the last row
                # NOTE: there cannot be any vertical tiles beginning here
                elif i == self.nrows - 1:
                    # check the first column
                    if j == 0:
                        # if there are horizontal tile after, then this is the first horizontal tile
                        if (self.tile_grid[i][j+1].actual_letter != '') and self.tile_grid[i][j+1].is_horizontal:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1
                        else:
                            print("How did we get to this line? Debug.")

                    # the last column of the last row cannot be numbered
                    # check the interior of the row
                    else:
                        # tile is first horizontal tile after blank
                        if (self.tile_grid[i][j-1].actual_letter == '') and self.tile_grid[i][j+1].is_horizontal:
                            self.tile_grid[i][j].number = str(number)
                            self.tile_grid[i][j].set_num_surface()
                            number += 1

                # check the first column
                elif j == 0:
                    # if there are horizontal tile after, then this is the first horizontal tile
                    if (self.tile_grid[i][j+1].actual_letter != '') and self.tile_grid[i][j+1].is_horizontal:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1
                    # if there is a vertical tile after, then this is the first vertical tile
                    elif (self.tile_grid[i+1][j].actual_letter != '') and self.tile_grid[i+1][j].is_vertical:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1
                    # we are horizontally behind a blank tile
                    elif self.tile_grid[i][j+1].actual_letter == '' and self.tile_grid[i+1][j].is_vertical:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1
                    # we are vertically behind a blank tile?
                    else:
                        continue

                # check last column, interior rows
                # NOTE: none of these can be horizontal
                # if the previous vertical tile was blank, and the next tile is vertical... 
                # then this tile is the beginning of a vertical word
                elif j == self.ncols - 1:
                    if (self.tile_grid[i-1][j].actual_letter == '') and self.tile_grid[i+1][j].is_vertical:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1

                # all other interior rows and interior columns 
                # only interior tiles following blank tiles (horizontally or vertically) can be numbered
                else:
                    if (self.tile_grid[i][j-1].actual_letter == '') and self.tile_grid[i][j+1].is_horizontal:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1
                    if (self.tile_grid[i-1][j].actual_letter == '') and self.tile_grid[i+1][j].is_vertical:
                        self.tile_grid[i][j].number = str(number)
                        self.tile_grid[i][j].set_num_surface()
                        number += 1
                    
            # skip over tiles that are blank
            else: 
                continue
        # self.printTiles()

    def printTiles(self):
        row = []
        for i in range(0, self.tile_grid.shape[0]):
            for j in range(0, self.tile_grid.shape[1]):
                row.append(self.tile_grid[i][j].disp_letter)
            print(row)
            row = []

        row = []
        print('\n')
        for i in range(0, self.tile_grid.shape[0]):
            for j in range(0, self.tile_grid.shape[1]):
                if self.tile_grid[i][j].active:
                    row.append('Active')
                else:
                    row.append('')
            print(row)
            row = []
    
    # when tiles are being updated... between clicks or otherwise...
    # this resets all tile colors and attributes EXCEPT for any tiles located at (i, j)
    # since we need to know if a tile was clicked in order to change directions

    # has the option to leave out a tile by tuple dimension
    # default is to leave out a tile located at (-1, -1)... which doesn't leave out any tiles
    def resetTiles(self, leave_out = (-1, -1)):
        for i,j in loop_through_grid(self.nrows, self.ncols):
            if i == leave_out[0] and j == leave_out[1]:
                continue
            elif (self.tile_grid[i][j].actual_letter != ''): 
                self.tile_grid[i][j].background_color = COLOR_INACTIVE_TILE
                self.tile_grid[i][j].word_active = False
                self.tile_grid[i][j].active = False
                self.active_horizontal = False 
                self.active_vertical = False 

    # these two helper functions take in a location on the grid (i,j), 
    # and set the neighboring tiles depending on whether we want to set horizontal/vertical
    def setHorizontalTiles(self, i, j):
        # change the current tile to be active and horizontal
        self.tile_grid[i][j].active = True
        self.tile_grid[i][j].word_active = True
        self.tile_grid[i][j].background_color = COLOR_ACTIVE_TILE
        self.tile_grid[i][j].active_horizontal = True
        self.tile_grid[i][j].active_vertical = False
        # loop backwards within the row to find other tiles that are part of the same word
        for k in range(j-1, -1, -1):
            if self.tile_grid[i][k].is_horizontal and (self.tile_grid[i][k].actual_letter != ''):
                self.tile_grid[i][k].word_active = True
                # additional precaution! make sure that other surrounding tiles become inactive
                # because if the user types a letter, that tile should not stay active
                # once the grid automatically moves over to highlight the next tile
                self.tile_grid[i][k].active = False
                self.tile_grid[i][k].background_color = COLOR_ACTIVE_WORD
            else: break
        # loop forwards within the row to find other tiles that are part of the same word
        for k in range(j+1, self.tile_grid.shape[1]):
            if self.tile_grid[i][k].is_horizontal and self.tile_grid[i][k].actual_letter != '':
                self.tile_grid[i][k].word_active = True
                self.tile_grid[i][k].active = False
                self.tile_grid[i][k].background_color = COLOR_ACTIVE_WORD
            else: break

    def setVerticalTiles(self, i, j):
        # change the current tile to be active and vertical
        self.tile_grid[i][j].active = True
        self.tile_grid[i][j].word_active = True
        self.tile_grid[i][j].background_color = COLOR_ACTIVE_TILE
        self.tile_grid[i][j].active_horizontal = False
        self.tile_grid[i][j].active_vertical = True
        # loop backwards within the column to find other tiles that are part of the same word
        for k in range(i-1, -1, -1):
            if self.tile_grid[k][j].is_vertical and self.tile_grid[k][j].actual_letter != '':
                self.tile_grid[k][j].word_active = True
                self.tile_grid[k][j].active = False
                self.tile_grid[k][j].background_color = COLOR_ACTIVE_WORD
            else: break
        # loop forwards within the column to find other tiles that are part of the same word
        for k in range(i+1, self.tile_grid.shape[0]):
            if self.tile_grid[k][j].is_vertical and self.tile_grid[k][j].actual_letter != '':
                self.tile_grid[k][j].word_active = True
                self.tile_grid[k][j].active = False
                self.tile_grid[k][j].background_color = COLOR_ACTIVE_WORD
            else: break

    # bug: when going to the next row, it still 'thinks' the 
    # tile at the end of the row is active

    def setNextHorizontalTile(self, m, n, forward = True):
        if forward == True:
            grid_loop = cycle_grid_horizontally(self.nrows, self.ncols)
        # loop backwards through the iteration cycle
        else:
            # print("setting up backward loop...")
            grid_loop = cycle_grid_horizontally(self.nrows, self.ncols, backwards = True)
        ## warning! this loops forever so make sure breaks are in place
        for i,j in grid_loop:
            # print("setting position in grid_loop")
            if (i == m) and (j == n):
                break

        # get the loop to the right point!
        for i,j in grid_loop:
            
            # if you are at the end of a row of a horizontal word
            # print("testing (i,j) value to set next horizontal tile:", (i,j))

            # the first letter will never be the next horizontal letter... 
            # ... but the next letter could be, so program this as if it is! 
            if self.tile_grid[i][j].actual_letter != '':
                # going to the next tile
                # the next tile is either part of the same word
                if self.tile_grid[i][j].is_horizontal:
                    self.resetTiles()
                    # print("setting this tile horizontal:", (i,j))
                    self.setHorizontalTiles(i,j)
                    # print("tiles look like after setting horizontal tiles:")
                    self.printTiles()
                    break
                # we could be moving from blank tile to a vertical tile 
                elif self.tile_grid[i][j].is_vertical:
                    self.resetTiles()
                    print("setting the next tile vertical:", (i,j))
                    self.setVerticalTiles(i,j)
                    break
                # not sure how this situation is possible
                else: 
                    print("Runtime error: figure out why this line is printing...")
                break

            # the next tile is a blank letter OR we are looping around again
            else:
                print("next tile is blank")
                continue  

    def setNextVerticalTile(self, m, n, forward = True): 
        if forward == True:
            vertical_grid_loop = cycle_grid_vertically(self.ncols, self.nrows)
        else:
            vertical_grid_loop = cycle_grid_vertically(self.ncols, self.nrows, backwards = True)
        ## warning! this loops forever so make sure breaks are in place
        for i,j in vertical_grid_loop:
            print("Testing position:", (i,j))
            if (i == m) and (j == n):
                print("found current vertical position:", (i,j))
                break

        # get the loop to the right point!
        for i,j in vertical_grid_loop:
            
            # if you are at the end of a row of a horizontal word
            print("testing (i,j) value to set next vertical tile:", (i,j))

            # the first letter will never be the next horizontal letter... 
            # ... but the next letter could be, so program this as if it is! 
            if self.tile_grid[i][j].actual_letter != '':
                # going to the next tile
                # the next tile is either part of the same word
                if self.tile_grid[i][j].is_vertical:
                    self.resetTiles()
                    self.setVerticalTiles(i,j)
                    break
                # we could be moving from blank tile to a horizontal tile 
                elif self.tile_grid[i][j].is_horizontal:
                    self.resetTiles()
                    self.setHorizontalTiles(i,j)
                    break
                # not sure how this situation is possible
                else: 
                    print("Runtime error: figure out why this line is printing...")
                break

            # the next tile is a blank letter OR we are looping around again
            else:
                print("next tile is blank")
                continue       

    def handle_event(self, event):
        # when the user clicks, every tile is looped through to detect where they clicked
        if (event.type == pg.MOUSEBUTTONDOWN):
            for i,j in loop_through_grid(self.nrows, self.ncols):
                # if previously clicked, it must change directions: 
                # horizontal --> vertical, vertical --> horizontal
                if self.tile_grid[i][j].rect.collidepoint(event.pos) and (self.tile_grid[i][j].actual_letter != ''):
                    #### get the previous tile 
                    if self.row_col_tuple != (None, None):
                        (m,n) = self.row_col_tuple
                        print(self.row_col_tuple)
                        #### set previous tile inactive
                        self.tile_grid[m][n].active = False
                    ####
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
                        # print("you clicked the same tile!")
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

                # set background color of blank tile, leave all other attributes FALSE
                elif self.tile_grid[i][j].actual_letter == '':
                    self.tile_grid[i][j].background_color = COLOR_BLANK_TILE
                # for other tiles not affected by the mouseclick event...
                else:
                    continue

            self.printTiles()    

        # typing in a letter takes you to the next tile for whatever direction you are are going
        elif event.type == pg.KEYDOWN:
            for i,j in loop_through_grid(self.tile_grid.shape[0], self.tile_grid.shape[1]):
                # this is necessary so if you click somewhere else and type, nothing happens
                if self.tile_grid[i][j].active == True:
                    self.row_col_tuple = (i,j)
                    if pg.K_a <= event.key <= pg.K_z:
                        # set the tile to the letter and move forward
                        # print("setting", (i,j), "to the letter:", event.unicode)
                        self.tile_grid[i][j].disp_letter = event.unicode

                        # if you are on a tile that is part of a horizontal word...
                        if self.tile_grid[i][j].active_horizontal == True:
                            # print("calling setNextHorizontalTile with (i,j) =", (i,j))
                            self.setNextHorizontalTile(i,j)
                            # after this point the tile from the previous row and the next tile are active
                            # when NEITHER should be active
                            self.printTiles()
                        elif self.tile_grid[i][j].active_vertical == True:
                            # switching i and j should change the behavior to vertical!
                            self.setNextVerticalTile(i,j)
                    elif event.key == pg.K_RIGHT:
                        self.setNextHorizontalTile(i, j, forward = True)
                    elif event.key == pg.K_LEFT:
                        self.setNextHorizontalTile(i, j, forward = False)
                    elif event.key == pg.K_DOWN:
                        self.setNextVerticalTile(i, j, forward = True)
                    elif event.key == pg.K_UP:
                        self.setNextVerticalTile(i, j, forward = False)
                    elif event.key == pg.K_BACKSPACE:
                        if self.tile_grid[i][j].active_horizontal == True:
                            self.setNextHorizontalTile(i, j, forward = False)
                            self.tile_grid[i][j].disp_letter = ''
                        elif self.tile_grid[i][j].active_vertical == True:
                            self.setNextVerticalTile(i, j, forward = False)
                            self.tile_grid[i][j].disp_letter = ''
                    break
                else: 
                    continue
        else:
            pass

        self.update_grid(event)

    def update_grid(self, event):
        # redraw the tiles for a word whenever there is an event
        for i,j in loop_through_grid(self.nrows, self.ncols):
            self.tile_grid[i][j].handle_event(event)
            self.tile_grid[i][j].draw(screen)
