import numpy as np
import pygame as pg
from Grid import Grid

# define pg parameters
pg.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

if __name__ == '__main__':
    clock = pg.time.Clock()
    done = False

    x0, y0 = 10, 10

    setup_grid = np.array(
        [['w', 'a', '', '', 'e', 'd'],
        ['a', 'l', '', 'a', '', 'o'],
        ['s', 'e', 'd', 'g', 'e', 's'], 
        ['', 'e', '', '' , '', ''],
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

            pg.display.flip()
            clock.tick(30)

    pg.quit()