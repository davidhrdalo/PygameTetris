# File contains the game logic for the controller
# Defines game rules
# Defines actions based off of user input that has been received

import sys
import pygame
import random
from abc import ABC, abstractmethod
import logic.config as config
from logic.tetromino import *

def determine_level_easy(score):
    if 0 <= score < 300:
        return 0
    elif 300 <= score < 1000:
        return 1
    elif 1000 <= score < 2000:
        return 2
    elif 2000 <= score < 4000:
        return 3
    elif 4000 <= score < 6000:
        return 4
    elif 6000 <= score < 8000:
        return 5
    elif 8000 <= score < 10000:
        return 6
    elif 10000 <= score < 15000:
        return 7
    elif 15000 <= score < 20000:
        return 8
    elif 20000 <= score < 25000:
        return 9
    else:
        return 10

def determine_level_hard(score):
    if 0 <= score < 500:
        return 5
    elif 500 <= score < 1500:
        return 6
    elif 1500 <= score < 3000:
        return 7
    elif 3000 <= score < 5000:
        return 8
    elif 5000 <= score < 10000:
        return 9
    else:
        return 10

def update_score_file(filename, new_score, username):
    try:
        # Try to open the file and read the scores
        with open(filename, 'r') as f:
            scores = [line.strip().split(' ', 1) for line in f.readlines()]  # Read scores along with names
            scores = [(int(score), name) for score, name in scores]  # Convert score to int
    except FileNotFoundError:
        # If the file does not exist, create an empty scores list
        scores = []

    # Append the new score and sort the list in descending order of scores
    scores.append((new_score, username))
    scores.sort(key=lambda x: x[0], reverse=True)  # Sort by score

    # Write back the top 10 scores to the file
    with open(filename, 'w') as f:
        for score, name in scores[:10]:  # Keep only the top 10 scores
            f.write(f"{score} {name}\n")


def input_box(surface, ai_mode=False):
    user_name = 'AI' if ai_mode else ''

    while True:
        surface.fill((30, 30, 30))
        pygame.draw.rect(surface, (200, 200, 200), (config.window_w // 4, config.window_h // 3, config.window_w // 2, config.window_h // 3))

        font = pygame.font.SysFont('helvetica', 30)

        # Render "High Score!" text
        text = font.render("High Score!", 1, (255, 255, 255))
        surface.blit(text, (config.window_w // 4 + 50, config.window_h // 3 + 30))

        if not ai_mode:
            # Render additional message for players
            instruction_text = font.render("Type your name and press the enter key", 1, (255, 255, 255))
            surface.blit(instruction_text, (config.window_w // 4 + 50, config.window_h // 3 + 70))

        # Render the input field and the username
        input_field_color = (150, 150, 150)
        input_field_rect = pygame.Rect(config.window_w // 4 + 50, config.window_h // 2, config.window_w // 2 - 100, 50)
        pygame.draw.rect(surface, input_field_color, input_field_rect)

        user_text = font.render(user_name, 1, (0, 0, 0))
        surface.blit(user_text, (input_field_rect.x + 10, input_field_rect.y + 10))

        pygame.display.flip()

        if ai_mode:
            pygame.time.delay(2000)
            return user_name

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_name
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

def initialize_game_state():
    """ Stores game variables for a new game session. """
    # Define initial game state variables
    game_score = 0
    game_level = 0
    time_since_last_fall = 0
    speed_of_fall = 0.3 # if statement from the first file
    time_since_level_up = 0
    active_tetromino = fetch_random_tetromino()
    upcoming_tetromino = fetch_random_tetromino()
    game_time = pygame.time.Clock()
    game_paused = False
    need_to_change_tetromino = False
    game_running = True
    locked_blocks_positions = {}

    return (locked_blocks_positions, game_paused, need_to_change_tetromino, game_running , active_tetromino, upcoming_tetromino,
            game_time, time_since_last_fall , speed_of_fall , time_since_level_up , game_score , game_level )

def generate_game_grid(locked_pos=None):
    if locked_pos is None:
        locked_pos = {}
    grid = [[config.EMPTY_CELL for _ in range(config.COLS)] for _ in range(config.ROWS)]
    for row in range(config.ROWS):
        for col in range(config.COLS):
            if (col, row) in locked_pos:
                colour = locked_pos[(col, row)]
                grid[row][col] = colour
    return grid




def get_tetromino_positions(tetromino):
    """ Converts the tetromino format to a list and creates it on the game grid. """
    positions = []

    # Determine the current rotation format of the tetromino
    current_tetromino = tetromino.shape[tetromino.spin % len(tetromino.shape)]

    # Iterate through each block in the current tetromino format
    for i in range(len(current_tetromino)):
        for j in range(len(current_tetromino[i])):
            # If the block is an 'O', calculate its position on the grid
            if current_tetromino[i][j] == 'O':
                positions.append((tetromino.x_pos + j, tetromino.y_pos + i - 4))

    # Adjust the positions to fit within the game grid
    return [(x - 2, y) for x, y in positions]


def is_position_valid(tetromino, grid):
    """ Check if the given tetromino position is valid. """

    accepted_positions = []

    max_x = config.COLS - 1
    max_y = config.ROWS - 1

    # Collect all positions in the grid that are empty (unoccupied)
    for i in range(config.ROWS):
        for j in range(config.COLS):
            if grid[i][j] == config.EMPTY_CELL:
                accepted_positions.append((j, i))

    # Convert the tetromino format to its positions on the grid
    tetromino_positions = get_tetromino_positions(tetromino)

    # Boundary Check
    for pos in tetromino_positions:
        x, y = pos
        if x < 0 or x > max_x:
            return False
        if y > max_y:
            return False

    # Collision Check
    for position in tetromino_positions:
        x, y = position
        if y > -1 and position not in accepted_positions:
            return False

    return True





def is_game_over(positions):
    """ Determine if any tetromino position is above the game grid. """
    return any(pos[1] < 1 for pos in positions)


def fetch_random_tetromino():
    """ Generate a random tetromino at the top-middle of the game grid. """
    if config.EXTENDED_GAME:
        TetrominoFactory.add_extended_tetrominoes()

    tetromino_type = random.choice(list(TetrominoFactory.tetromino_classes.keys()))
    spawn_x = config.COLS // 2  # This will roughly center the tetromino on the game board
    return TetrominoFactory.create_tetromino(tetromino_type, spawn_x, 0)



def render_centered_text(surface, text, size, colour):
    """ Render and draw a text in the middle of the game surface. """
    font = pygame.font.SysFont("helvetica", size, bold=True)
    text = font.render(text, 1, colour)

    # Calculate the position for the box
    box_x = config.window_x + config.play_w / 2 - (text.get_width() / 2) - 10  # 10 is padding
    box_y = config.window_y + config.play_h / 2 - text.get_height() / 2 - 10  # 10 is padding
    box_width = text.get_width() + 20  # 20 is padding
    box_height = text.get_height() + 20  # 20 is padding

    # Draw the box with a specific colour (e.g., gray)
    pygame.draw.rect(surface, (128, 128, 128), (box_x, box_y, box_width, box_height))

    # Blit the label onto the surface
    surface.blit(text, (config.window_x + config.play_w / 2 - (text.get_width()/2), config.window_y + config.play_h/2 - text.get_height()/2))


def draw_vertical_grid_lines(surface, start_x, end_x, y):
    """ Draw vertical grid lines on the game surface. """
    grid_colour = (128, 128, 128)
    for x in range(start_x, start_x + config.COLS * config.tetromino_wh + 1, config.tetromino_wh):
        pygame.draw.line(surface, grid_colour, (x, y), (x, y + config.ROWS * config.tetromino_wh))

def draw_horizontal_grid_lines(surface, x, start_y, end_y):
    """ Draw horizontal grid lines on the game surface. """
    grid_colour = (128, 128, 128)
    for y in range(start_y, start_y + config.ROWS * config.tetromino_wh + 1, config.tetromino_wh):
        pygame.draw.line(surface, grid_colour, (x, y), (x + config.COLS * config.tetromino_wh, y))


def render_game_grid(surface, grid):
    """ Draw the game grid on the surface. """
    end_y = config.window_y + config.ROWS * config.tetromino_wh

    draw_vertical_grid_lines(surface, config.window_x, config.window_x + config.COLS * config.tetromino_wh, config.window_y)
    draw_horizontal_grid_lines(surface, config.window_x, config.window_y, end_y)


def remove_full_rows(grid, locked, muted):
    """ Clear full rows from the grid and update locked positions. """
    rows_cleared = 0
    rows_to_clear = []

    # Identify full rows
    for i, row in enumerate(reversed(grid)):
        if not any(cell == config.EMPTY_CELL for cell in row):
            rows_to_clear.append(len(grid) - 1 - i)

    # Remove full rows from locked positions
    for row_index in rows_to_clear:
        rows_cleared += 1
        for j in range(len(grid[0])):
            locked.pop((j, row_index), None)

    # Shift locked positions down
    if rows_cleared:
        if rows_cleared and not muted:
            config.tiles_cleared_sound.play()
        for (x, y), value in sorted(locked.items(), key=lambda item: item[0][1], reverse=True):
            if y < rows_to_clear[-1]:
                locked[(x, y + rows_cleared)] = locked.pop((x, y))

    # Calculate score based on number of lines cleared
    if rows_cleared == 1:
        return 100
    elif rows_cleared == 2:
        return 300
    elif rows_cleared == 3:
        return 600
    elif rows_cleared >= 4:
        return 1000
    else:
        return 0



def display_upcoming_piece(tetromino, surface):
    """ Display the next tetromino on the game surface. """
    font = pygame.font.SysFont('helvetica', 30)
    label = font.render('Next Tetromino', 1, (255, 255, 255))

    # Get the current spin of the tetromino
    current_tetromino_spin = tetromino.shape[tetromino.spin % len(tetromino.shape)]

    # Draw the tetromino on the surface
    for i in range(len(current_tetromino_spin)):
        for j in range(len(current_tetromino_spin[i])):
            if current_tetromino_spin[i][j] == 'O':
                x_pos = 680 + j * config.tetromino_wh
                y_pos = 410 + i * config.tetromino_wh
                pygame.draw.rect(surface, tetromino.colour, (x_pos, y_pos, config.tetromino_wh, config.tetromino_wh))

    # Position and display the label
    label_position = (config.window_x + 510, config.window_y + 175)
    surface.blit(label, label_position)


# SHOULD BE MOVED TO VIEW
def render_game_window(surface, grid, score=0, level=0):
    """ Render the game window with the current state, score, and level. """
    # Set the background image
    surface.blit(config.background_image, (0, 0))

    # Draw the main game rectangle
    pygame.draw.rect(surface, (40, 40, 40), (config.window_x+470, config.window_y, 300, 600))

    # Initialize font for text rendering
    pygame.font.init()

    # Display game title
    font = pygame.font.SysFont('helvetica', 60)
    text = font.render('T e t r i s', 1, (255, 255, 255))
    surface.blit(text, (400, 40))

    # Display group name
    font = pygame.font.SysFont('helvetica', 30)
    text = font.render('Group 19', 1, (255, 255, 255))
    surface.blit(text, (50, 40))

    # Display game mode options
    if config.AI_ENABLED:
        text = font.render('AI Mode', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+20))
    else:
        text = font.render('Player Mode', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+20))

    if config.EXTENDED_GAME:
        text = font.render('Extended Game', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+55))
    else:
        text = font.render('Normal Game', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+55))

    if config.SMALL_BOARD:
        text = font.render('Small Board 16x8', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+90))
    elif config.LARGE_BOARD:
        text = font.render('Large Board 20x15', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+90))
    else:
        text = font.render('Standard Board 20x10', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+90))

    if config.FAST_GAME:
        text = font.render('Speed: Fast', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+125))
    else:
        text = font.render('Speed: Slow', 1, (255, 255, 255))
        surface.blit(text, (config.window_x+510, config.window_y+125))

    # Draw the tetrominoes on the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (config.window_x + j*config.tetromino_wh, config.window_y + i*config.tetromino_wh, config.tetromino_wh, config.tetromino_wh), 0)

    # Draw the grid lines
    render_game_grid(surface, grid)


def shift_piece(current_piece, grid, direction):
    """
    Move the current tetromino piece in the specified direction.

    Parameters:
    - current_piece: The tetromino piece to move.
    - grid: Current game grid.
    - direction: The direction to move the piece ("LEFT", "RIGHT", "DOWN", "ROTATE").
    """
    # Move the piece to the left
    if direction == "LEFT":
        current_piece.x_pos -= 1
        if not is_position_valid(current_piece, grid):  # Check if the move is valid
            current_piece.x_pos += 1

    # Move the piece to the right
    elif direction == "RIGHT":
        current_piece.x_pos += 1
        if not is_position_valid(current_piece, grid):  # Check if the move is valid
            current_piece.x_pos -= 1

    # Move the piece downwards
    elif direction == "DOWN":
        current_piece.y_pos += 1
        if not is_position_valid(current_piece, grid):  # Check if the move is valid
            current_piece.y_pos -= 1

    # Rotate the piece
    elif direction == "ROTATE":
        current_piece.spin += 1
        if not is_position_valid(current_piece, grid):  # Check if the rotation is valid
            current_piece.spin -= 1


def process_quit_events(paused, run, score, window_size):
    """ Handle events during the game's pause state. """
    for pause_event in pygame.event.get():
        # Check for game exit event
        if pause_event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        # Check for unpause event (Escape key)
        if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_ESCAPE:
            paused = False
        # Check for mouse click events
        if pause_event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Check if "No" button is clicked
            if config.window_w // 4 + 50 <= x <= config.window_w // 4 + 200 and config.window_h // 2 <= y <= config.window_h // 2 + 50:
                paused = False
            # Check if "Yes" button is clicked
            elif config.window_w // 2 - 50 <= x <= config.window_w // 2 + 100 and config.window_h // 2 <= y <= config.window_h // 2 + 50:
                run = False
                score_filename = 'scores.txt'

                # Try to load existing scores.
                try:
                    with open(score_filename, 'r') as file:
                        scores = [int(line.strip().split(' ', 1)[0]) for line in file.readlines()]
                except FileNotFoundError:
                    scores = []

                # Check if the player's score is a top 10 score.
                if not scores or len(scores) < 10 or score > min(scores):  # Use score directly
                    if config.AI_ENABLED:
                        username = input_box(window_size, ai_mode=True)  # Use window_size directly
                        update_score_file(score_filename, score, username,)
                    else:
                        username = input_box(window_size)  # Use window_size directly
                        update_score_file(score_filename, score, username)  # Use score directly
                else:
                    # If the player's score is not a top 10 score,
                    # you might want to display a message or do something else here.
                    pass
                #pygame.quit()
                #sys.exit()
                #return run, paused
                pygame.event.clear()  # Clear the event queue
                return run, paused


    return run, paused

def render_quit_dialog(surface):
    """ Creates a dialog box asking if the user wants to quit. """
    # Draw the main dialog box
    pygame.draw.rect(surface, (200, 200, 200), (config.window_w // 4, config.window_h // 3, config.window_w // 2, config.window_h // 3))

    # Display the question text
    font = pygame.font.SysFont('helvetica', 30)
    text = font.render("Do you want to quit?", 1, (0, 0, 0))
    surface.blit(text, (config.window_w // 4 + 50, config.window_h // 3 + 30))

    # Draw the "No" and "Yes" buttons
    pygame.draw.rect(surface, (169, 169, 169), (config.window_w // 4 + 50, config.window_h // 2, 150, 50))
    pygame.draw.rect(surface, (255, 255, 255), (config.window_w // 2 - 50, config.window_h // 2, 150, 50))
    text_continue = font.render("No", 1, (0, 0, 0))
    text_return = font.render("Yes", 1, (0, 0, 0))
    surface.blit(text_continue, (config.window_w // 4 + 75, config.window_h // 2 + 15))
    surface.blit(text_return, (config.window_w // 2 - 25, config.window_h // 2 + 15))


def render_pause_dialog(surface):
    """ Creates a dialog box during the game's pause state. """
    pygame.draw.rect(surface, (200, 200, 200), (config.window_w // 4, config.window_h // 3, config.window_w // 2, config.window_h // 3))

    font = pygame.font.SysFont('helvetica', 30)
    text = font.render("Game Paused", 1, (0, 0, 0))
    surface.blit(text, (config.window_w // 4 + 50, config.window_h // 3 + 30))

    pygame.draw.rect(surface, (169, 169, 169), (config.window_w // 4 + 50, config.window_h // 2, 150, 50))
    text_continue = font.render("Resume", 1, (0, 0, 0))
    surface.blit(text_continue, (config.window_w // 4 + 75, config.window_h // 2 + 15))

def process_pause_events(paused):
    """ Handle events during the game's pause state. """
    for pause_event in pygame.event.get():
        if pause_event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:  # Changed to 'P' key for pausing
            paused = False
        if pause_event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if config.window_w // 4 + 50 <= x <= config.window_w // 4 + 200 and config.window_h // 2 <= y <= config.window_h // 2 + 50:  # Resume button area
                paused = False
    return paused



class Observable:
    def __init__(self):
        """Initiates the Observable object with an empty list of observers"""
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        """ Removes an observer from the list of observers """
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)


class Observer(ABC):
    """Defines the interface for the Observer in the Observer Design Pattern"""
    @abstractmethod
    def update(self, observable):
        pass


class ScoreObserver(Observer):
    def __init__(self, surface):
        """Initializes the ScoreObserver with a surface to render text on"""
        self.surface = surface
        self.font = pygame.font.SysFont('helvetica', 30)  # Initialize the font once

    def update(self, observable):
        score = observable.score
        text = self.font.render('Score: ' + str(score), 1, (255, 255, 255))
        text_rect = text.get_rect(topleft=(config.window_x+510, config.window_y+450))

        # Fill only the rect where the score is displayed
        #self.surface.fill((0, 0, 0), text_rect)

        self.surface.blit(text, text_rect.topleft)


class LevelObserver(Observer):
    def __init__(self, surface):
        """Initializes the LevelObserver with a surface to render text on"""
        self.surface = surface
        self.font = pygame.font.SysFont('helvetica', 30)  # Initialize the font once

    def update(self, observable):
        level = observable.level
        text = self.font.render('Current Level: ' + str(level), 1, (255, 255, 255))
        text_rect = text.get_rect(topleft=(config.window_x + 510, config.window_y + 490))

        # Fill only the rect where the level is displayed
        #self.surface.fill((0, 0, 0), text_rect)

        self.surface.blit(text, text_rect.topleft)


def is_move_valid(move, piece, grid):
    rotation, x_position = move
    test_piece = piece.copy()

    for _ in range(rotation):
        shift_piece(test_piece, grid, "ROTATE")

    test_piece.x_pos = x_position
    test_piece.y_pos = 0

    while is_position_valid(test_piece, grid):
        test_piece.y_pos += 1
    test_piece.y_pos -= 1

    return is_position_valid(test_piece, grid)


def possible_moves(piece, grid):
    moves = [(rotation, x) for rotation in range(4) for x in range((config.window_w // 30) - piece.width())]
    return [move for move in moves if is_move_valid(move, piece, grid)]


def evaluate_board(board, weights):
    a, b, c, d = weights
    completed_lines = sum(1 for row in board if all(cell != (0, 0, 0) for cell in row))
    filled_cells_y = [y for y, row in enumerate(board) if any(cell != (0, 0, 0) for cell in row)]
    board_height = max(filled_cells_y) - min(filled_cells_y) + 1 if filled_cells_y else 0
    holes = sum(1 for col in zip(*board) for i, cell in enumerate(col) if
                cell == (0, 0, 0) and any(x != (0, 0, 0) for x in col[:i]))
    column_heights = [max([i for i, cell in enumerate(col) if cell != (0, 0, 0)], default=0) for col in zip(*board)]
    bumpiness = sum(abs(column_heights[i] - column_heights[i + 1]) for i in range(len(column_heights) - 1))

    # Print out the individual components for debugging
    print(f"Completed Lines: {completed_lines}")
    print(f"Board Height: {board_height}")
    print(f"Holes: {holes}")
    print(f"Bumpiness: {bumpiness}")

    return a * completed_lines - b * board_height - c * holes - d * bumpiness



def best_move(current_piece, grid, weights):
    moves = possible_moves(current_piece, grid)
    if not moves:
        return None

    evaluations = {}
    for move in moves:
        test_piece = current_piece.copy()
        test_grid = [row.copy() for row in grid]

        rotation, x_position = move
        for _ in range(rotation):
            shift_piece(test_piece, test_grid, "ROTATE")
        test_piece.x_pos = x_position

        while is_position_valid(test_piece, test_grid):
            test_piece.y_pos += 1
        test_piece.y_pos -= 1

        shape_positions = get_tetromino_positions(test_piece)
        for pos in shape_positions:
            x, y = pos
            if y > -1:
                test_grid[y][x] = test_piece.colour

        evaluations[move] = evaluate_board(test_grid, weights)

    best_evaluation_move = max(evaluations, key=evaluations.get)
    return best_evaluation_move
