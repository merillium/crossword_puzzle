### Running the crossword puzzle program
###### You need to have the PyGame library installed.
###### pip3 install pygame

###### Then clone repo, cd into the directory, and type the following commands into terminal: (the first command increases the limit on the number of open files from the MacBook Air default of 256):
###### pip install -r requirements
###### ulimit -n 1000
###### python3 -i main.py

##### If you want to run it in a web browser locally, you can use `pygbag` and follow the instructions ![here](https://pygame-web.github.io/wiki/pygbag/#detailed-documentation):


##### Features that need to be added: 
###### (1) Perhaps the clue text can be linked to the grid (i.e. clicking on a clue activates the corresponding word) </br> (2) clues should be bound in a box with calculations performed instead of hardcoding in the font size or length of text wrapping </br> (3) clue font size should adjust automatically to the size of the grid </br> (4) implement a button to check for correctness of the grid (instead of incorrect colors immediately displaying as red) </br> (5) The one crossword puzzle grid is currently hard-coded. A webscraper to obtain completed NYT-style crosswords or even a NYT-style crossword generator (very computationally intensive but challenging problem to leave as relatively few blanks!) would be a nice feature. 

###### Currently this is what the Pygame console looks like when it loads with a sample grid [1].
![crossword example image](https://github.com/merillium/crossword_puzzle/blob/master/images/sample_crossword.png)

##### ** This is a work in a progress! Check back for updates **

##### References:
##### [1] https://nytcrosswordanswers.com/612009/new-york-times-crossword-february-28-2020-answers/
