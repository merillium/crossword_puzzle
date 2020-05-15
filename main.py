import numpy as np
import pygame as pg
from Grid import Grid
from Clues import Clues

# define pg parameters
pg.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


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

    clues_dict = {
    'bingewatch': 'See the seasons pass quickly?',
    'esa': 'Celle-là, across the Pyrenees',
    'escaperoom': 'Something that requires thinking inside the box?',
    'evil': 'What mustache-twirling might suggest',
    'deathtraps': 'Dangerous places',
    'maxi': 'Dress style',
    'seas': "They're often high, but never dry",
    'nada': "Zippo",
    'pants': "Something Winnie-the-Pooh lacks",
    'pay': "Equal ___",
    'relight': "Fire a second time",
    'ohstop': "I'm blushing!",
    'females': "Sows and cows",
    'recut': "Edited, as a film",
    'sonic': "___ boom",
    'lee': "Common middle name",
    'earthshattering': "Momentous",
    'ode': "Labor of love?",
    'opals': "Stones that diffract light",
    'bossa': "___ nova",
    'healers': "Those who practice energy medicine",
    'looted': "Like many Egyptian pyramids",
    'sundeck': "Upper part of a cruise ship",
    'sos': "Help wanted sign",
    'antes': "Pays (up)",
    'nacl': "About 0.4 percent of the weight of the human body",
    'bmws': "Z4 and i3",
    'utep': "Lone Star State sch.",
    'makeitrain': "Give out cash freely",
    'nest': "Store one inside another",
    'idontwanna': "You can't make me!",
    'art': "Exhibits at an exhibition",
    'containing': "Bottling up",
    'beds': "Twins, e.g.",
    'isee': '"Gotcha"',
    'ncaa': "Org. that holds many conferences",
    'gats': "Prohibition-era guns",
    'eph': "N.T. book after Galatians",
    'wetnap': "Amenity in many a picnic box",
    'array': "Assemblage",
    'toad': "Its scientific name is Bufo bufo",
    'coparents': "Separated couple with kids, say",
    'hms': "Royal navy letters",
    'evangelist': "Proselytizer",
    'sixthsense': "Intuition",
    'alist': "Group of stars",
    'email': "Field added to the I.R.S.'s Form 1040 in 2019",
    'placebos': "Controls, of a sort", 
    'potholes': "Driving hazards",
    'emit': "Discharge",
    'oreo': "It may get a good licking",
    'headhunter': "Recruiter",
    'screentest': "Audition",
    'tut': "When repeated, a reproof",
    'foals': "Some farm births",
    'sharknado': "2013 disaster film with a cult following",
    'egad': '"Holy moly!"',
    'spec': "On ____ (without a firm commentment)",
    'roo': "Kanga's kid",
    'adept': "Crackerjack",
    'lolita': '1955 novel with the line "It was love at first sight, at last night, at ever and ever sight"',
    'sauna': "Part of a bathhouse",
    'scent': "Pine, for one",
    'akon': 'One-named singer with the 2006 hit "Smack that"',
    'bran': "Bread enricher",
    'mani': "Spa job, informally",
    'winn': "Because of ____-Dixie (2000 award-winning children's book)",
    'snag': "Slight problem",
    'mic': "Karaoke need",
    'twi': "Lead-in to light"
    }

    letter_grid = np.apply_along_axis(lambda x:list(x[0]), 1, word_grid)

    sample_grid = Grid(letter_grid, 0.8, x0, y0)
    sample_clues = Clues(sample_grid, clues_dict)

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # screen.fill((30, 30, 30))

            sample_grid.handle_event(event)

            pg.display.flip()
            clock.tick(30)

    pg.quit()