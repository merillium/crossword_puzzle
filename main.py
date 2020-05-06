import numpy as np
import pygame as pg
from Grid import Grid

# define pg parameters
pg.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
screen = pg.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

if __name__ == '__main__':
    clock = pg.time.Clock()
    done = False

    x0, y0 = 10, 10

    word_grid = np.array([
        ['bingewatch  esa'],
        ['escaperoom evil'],
        ['deathtraps maxi'], 
        ['seas nada pants'],
        ['    pay relight'],
        ['ohstop females '],
        ['recut sonic lee'],
        ['earthshattering'],
        ['ode opals bossa'],
        [' healers looted'],
        ['sundeck sos    '],
        ['antes nacl bmws'],
        ['utep makeitrain'],
        ['nest idontwanna'],
        ['art  containing']
        ])

    letter_grid = np.apply_along_axis(lambda x:list(x[0]), 1, word_grid)

    sample_grid = Grid(letter_grid, x0, y0)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            screen.fill((30, 30, 30))

            sample_grid.handle_event(event)

            pg.display.flip()
            clock.tick(30)

    pg.quit()