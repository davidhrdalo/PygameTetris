


# Pygame imported for font and mixer module initialisations
import pygame

window_w, window_h = 1000, 800   # Main window width 1000 height 800
play_w, play_h = 300, 600  # Game board width 300 height 600
tetromino_wh = 30  # Tetromino width 30 height 30# File stores any global variables as well images and sounds

AI_ENABLED = False
FAST_GAME = False  # Set to False for slow mode

EXTENDED_GAME = False
LARGE_BOARD = False  # Set to False for standard board size
SMALL_BOARD = False  # Set to False for standard board size

# Standard dimensions
ROWS, COLS = 20, 10

# If LARGE_BOARD is True, adjust the dimensions
if LARGE_BOARD:
    ROWS, COLS = 20, 15

if SMALL_BOARD:
    ROWS, COLS = 16, 8

window_x = (window_w - play_w) // 5 # Game window top x
window_y = (window_h - play_h) - 20 # Game window top y

pygame.font.init()  # Pygame font module initialisation
pygame.mixer.init()  # Pygame sound mixer module initialisation


# Main game music
#pygame.mixer.music.load('path_to_your_music_file.mp3')
#pygame.mixer.music.set_volume(1.0)  # Set between 0.0 and 1.0
#pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

# Sound for blocks landing
block_land_sound = pygame.mixer.Sound('sound/bop.wav')
block_land_sound.set_volume(2)

# Game over/ player lost sound
game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
game_over_sound.set_volume(2)

# Cleared tiles sound
tiles_cleared_sound = pygame.mixer.Sound('sound/clear.wav')
tiles_cleared_sound.set_volume(2)

# Main game background image
background_image = pygame.image.load('images/background_image.jpg')
background_image = pygame.transform.scale(background_image, (window_w, window_h))
background_image = pygame.transform.scale(background_image, (window_w, window_h))

EMPTY_CELL = (0, 0, 0)  # This represents an empty cell