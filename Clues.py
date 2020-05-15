import pygame as pg
import textwrap
from Grid import Grid

# this class contains all of the horizontal and vertical clues
# they are then displayed on the screen

pg.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

class Clues:
	def __init__(self, display_grid, clues_dict):
		self.horizontal_dict, self.vertical_dict = display_grid.getWords()
		self.x_start = None
		self.y_start = None
		self.clue_color = pg.Color(100,0,255)
		self.clue_font = pg.font.Font(None, 24)
		self.clues_dict = clues_dict
		self.setCoordinates(display_grid)
		self.drawClues(display_grid)

	def setCoordinates(self, display_grid):
		grid_screen_ratio = display_grid.grid_screen_ratio
		nrows = display_grid.nrows
		ncols = display_grid.ncols
		TILE_SIZE = int(min(grid_screen_ratio*SCREEN_HEIGHT/nrows, grid_screen_ratio*SCREEN_WIDTH/ncols))
		self.x_start = TILE_SIZE * 1.05 * ncols
		self.y_start = display_grid.y_start

	# draws in the clues with a set width for text wrapping
	# To-do: calculate the appropriate width instead of hard-coding it
	def drawClues(self, display_grid, width = 32):
		# print("Drawing clues in...")
		# write in the title
		textsurface = self.clue_font.render("Horizontal Clues", True, self.clue_color)
		screen.blit(textsurface, (self.x_start, self.y_start))

		self.y_start += 18
		# adjust for the next line
		for key, label in self.horizontal_dict.items():
			clue_string = str(key) + ') ' + self.clues_dict[label]
			clue_wrapped = textwrap.fill(clue_string, width).split('\n')
			for clue_part in clue_wrapped:
				textsurface = self.clue_font.render(clue_part, True, self.clue_color)
				screen.blit(textsurface, (self.x_start, self.y_start))
				self.y_start += 18
		self.x_start += 9*width
		self.y_start = display_grid.y_start
		# write in the title
		textsurface = self.clue_font.render("Vertical Clues", True, self.clue_color)
		screen.blit(textsurface, (self.x_start, self.y_start))

		self.y_start += 18
		# adjust for the next line
		for key, label in self.vertical_dict.items():
			clue_string = str(key) + ') ' + self.clues_dict[label]
			clue_wrapped = textwrap.fill(clue_string, 40).split('\n')
			for clue_part in clue_wrapped:
				textsurface = self.clue_font.render(clue_part, True, self.clue_color)
				screen.blit(textsurface, (self.x_start, self.y_start))

				self.y_start += 18


