import pygame as pg
from Grid import Grid

# this class contains all of the horizontal and vertical clues
# they are then displayed on the screen

pg.init()
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 980

screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

class Clues:
	def __init__(self, display_grid, clues_dict):
		self.horizontal_dict, self.vertical_dict = display_grid.getWords()
		self.x_start = 750
		self.y_start = 10
		self.clue_color = pg.Color('violet')
		self.clue_font = pg.font.Font(None, 28)
		self.clues_dict = clues_dict
		self.draw()

	def draw(self):
		print("Drawing clues in...")
		count = 1
		for key, label in self.horizontal_dict.items():
			textsurface = self.clue_font.render(str(key) + ') ' + self.clues_dict[label], False, self.clue_color)
			screen.blit(textsurface, (self.x_start, self.y_start))
			self.y_start += 18

