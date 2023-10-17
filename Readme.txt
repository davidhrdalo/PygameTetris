Tetris Game Project - Software Design (3815ICT/7805ICT)
Group 19

The following Readme.txt file will provide details on the design and development of the Tetris game project.
This game was developed using the Pygame module.


Contents:
    File Structure - A visual understanding of how the project files have been layout.
    File Descriptions - A description of each file and its purpose.
    Line Count - A count of lines for each individual file and the total lines.
    Naming convention - A description of naming conventions


-----File Structure:-----

/main
    controller.py
    model.py
    view.py
    Readme.txt
    /logic
        config.py
        tetromino.py
    /images
        background_image.jpg
    /sounds
        bop.wav
        clear.wav
        game_over.wav
        music.mp3


-----File Descriptions:-----

controller.py
    Length = 134 lines
    This file launches the main game loop and takes user input and updates the view accordingly.
    This file is responsible for calling the main logic stored in the model file.

model.py
    Length = 364 lines
    This file contains the logic behind the game, including most functions.
    This logic is passed to the controller file.
    Settings and logic for the game can be tweaked through this file.

view.py
    Length = 133 lines
    This file is responsible for rendering the main UI for the player.
    This file renders the start screen.

config.py
    Length = 31 lines
    This file holds global variables and loads assets.
    Standard window height and length is defined in this file.
    All images and sounds are loaded through this file.

tetromino.py
    Length = 248 lines
    This file holds the logic for creating tetrominoes.
    Both normal and extended tetrominoes can be found here.


-----Line Count:-----

controller.py = 134 lines
model.py = 364 lines
view.py = 133 lines
config.py = 31 lines
tetromino.py = 248 lines

TOTAL = 910 lines


-----Naming Convention:-----

Naming conventions have been applied for classes, objects, functions and variables.

Classes:
    Use CamelCase with the first letter capitalised.
    Class names describe their purpose.

Objects:
    Use CamelCase with the first letter capitalised.
    Object names describe their purpose.

Functions:
    Use snake_case with a verb-noun structure.
    Function names describe what the function does.
    
Variables:
    Use snake_case.
    Variable names describe their purpose or what is assigned to them.
