# File contains the main game loop
# Takes logic and game rules from the model file
# Takes input from the player and passes it to the model file

from model import *
import time  # At the top of your file
import logic.config as config

class Tetris(Observable):
    speeds = {
        0: 0.6,  # 0.6 seconds per block
        1: 0.5,
        2: 0.4,
        3: 0.3,
        4: 0.2,
        5: 0.1,  # 0.1 second per block
        6: 0.08,
        7: 0.06,
        8: 0.04,
        9: 0.02,
        10: 0.01,
    }

    def __init__(self, window_size, fast_game):
        super().__init__()
        self.window_size = window_size
        self.muted = False
        self.level = 5 if fast_game else 0  # Set initial level based on game mode
        self.initialise()

    def initialise(self):
        """Initializes game variables."""
        (self.locked_positions, self.paused, self.change_piece, self.run, self.current_piece,
         self.next_piece, self.clock, self.fall_time, self.fall_speed, self.level_time, self.score,
         _) = initialize_game_state()
        self.ai_move = None
        self.fall_speed = self.speeds.get(self.level, self.speeds[0])

    def launch_game(self):
        """Main game loop that handles game progression."""
        pygame.mixer.music.load('sound/music.mp3')
        pygame.mixer.music.set_volume(0.1)  # Set between 0.0 and 1.0
        pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

        # Create an observer instance
        score_observer = ScoreObserver(self.window_size)
        # Add observer to the list of observers
        self.add_observer(score_observer)

        level_observer = LevelObserver(self.window_size)
        self.add_observer(level_observer)

        while self.run:
            self.game_cycle()

    def handle_events(self):
        """Handles user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                self.process_keydown_events(event)

    def process_keydown_events(self, event):
        """Processes keydown events for game actions."""
        if not config.AI_ENABLED:  # Only allow these controls if AI is not enabled
            if event.key == pygame.K_LEFT:
                shift_piece(self.current_piece, self.grid, "LEFT")
            elif event.key == pygame.K_RIGHT:
                shift_piece(self.current_piece, self.grid, "RIGHT")
            elif event.key == pygame.K_UP:
                shift_piece(self.current_piece, self.grid, "ROTATE")
        if event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            while self.paused:
                render_quit_dialog(self.window_size)
                pygame.display.flip()
                pygame.time.wait(100)
                self.run, self.paused = process_quit_events(self.paused, self.run, self.score, self.window_size)
                if not self.run:
                    break  #
        elif event.key == pygame.K_p:
            self.paused = not self.paused
            while self.paused:
                render_pause_dialog(self.window_size)
                pygame.display.flip()
                pygame.time.wait(100)
                self.paused = process_pause_events(self.paused)
        elif event.key == pygame.K_m:
            self.muted = not self.muted
            volume = 0 if self.muted else 0.1
            pygame.mixer.music.set_volume(volume)  # Mute/unmute the music accordingly

    # Call this method whenever the score changes
    def set_score(self, score):
        self.score = score
        self.notify_observers()

    def set_level(self, level):
        self.level = level
        self.fall_speed = self.speeds.get(self.level, self.speeds[0])
        self.notify_observers()

    def handle_AI(self):
        """Manages AI decision-making and actions."""
        if self.fall_time / 1000 <= self.fall_speed:
            return

        self.fall_time = 0
        if not hasattr(self, 'best_move') or not self.best_move:
            self.best_move = self.compute_best_move()

        # Move the piece according to AI's decision
        if self.best_move:
            self.move_piece_to_target(*self.best_move)

        pygame.event.pump()

        # Drop the piece
        self.drop_current_piece()

    def compute_best_move(self):
        """Computes the best move using the AI logic."""
        try:
            start_time = time.time()
            move = best_move(self.current_piece, self.grid, [1000, 500, 100, 300]) # Completed Lines | Board Height | Holes | Bumpiness
            elapsed_time = time.time() - start_time
            print(f"AI took {elapsed_time} seconds to compute.")

            if elapsed_time > 0.5:
                print("AI exceeded time limit!")
                # Handle excessive time if needed
            return move
        except Exception as e:
            print("Exception occurred during AI computation:", e)

    def move_piece_to_target(self, target_rotation, target_x_position):
        """Moves the current piece to the target x position."""
        rotation_attempts = 0
        while self.current_piece.spin != target_rotation and rotation_attempts < 4:
            shift_piece(self.current_piece, self.grid, "ROTATE")
            rotation_attempts += 1

        if self.current_piece.x_pos < target_x_position:
            shift_piece(self.current_piece, self.grid, "RIGHT")
        elif self.current_piece.x_pos > target_x_position:
            shift_piece(self.current_piece, self.grid, "LEFT")

    def drop_current_piece(self):
        """Drops the current piece by one unit and handles landing."""
        self.current_piece.y_pos += 1
        if not is_position_valid(self.current_piece, self.grid) and self.current_piece.y_pos > 0:
            self.current_piece.y_pos -= 1
            self.change_piece = True
            if not self.muted:
                config.block_land_sound.play()
            self.best_move = None


    def game_cycle(self):
        try:
            """Represents a single game cycle, updating game state, rendering, and handling events."""
            self.grid = generate_game_grid(self.locked_positions)
            self.fall_time += self.clock.get_rawtime()
            self.level_time += self.clock.get_rawtime()
            self.clock.tick()

            if config.AI_ENABLED:
                self.handle_AI()

            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    shift_piece(self.current_piece, self.grid, "DOWN")

                if self.fall_time / 1000 > self.fall_speed:
                    self.fall_time = 0
                    self.current_piece.y_pos += 1

            self.handle_events()

            # The shared logic
            if not is_position_valid(self.current_piece, self.grid) and self.current_piece.y_pos > 0:
                self.current_piece.y_pos -= 1
                self.change_piece = True
                if not self.muted:
                    config.block_land_sound.play()

            shape_pos = get_tetromino_positions(self.current_piece)
            for pos in shape_pos:
                x, y = pos
                if y > -1:
                    self.grid[y][x] = self.current_piece.colour

            if self.change_piece:
                for pos in shape_pos:
                    self.locked_positions[pos] = self.current_piece.colour
                self.current_piece = self.next_piece
                self.next_piece = fetch_random_tetromino()
                self.change_piece = False
                self.set_score(self.score + remove_full_rows(self.grid, self.locked_positions, self.muted))
                if config.FAST_GAME:
                    self.set_level(determine_level_hard(self.score))
                else:
                    self.set_level(determine_level_easy(self.score))

            render_game_window(self.window_size, self.grid, self.score, self.level)
            display_upcoming_piece(self.next_piece, self.window_size)
            self.notify_observers()  # Notify observers after rendering all other game elements
            pygame.display.update()  # Ensure this is the last line in this method

            if is_game_over(self.locked_positions):
                self.game_over_procedure()

        except Exception as e:
            print(f"Exception occurred in game_cycle: {e}")
            raise  # This will re-raise the exception after printing, giving you the full traceback.

    def game_over_procedure(self):
        """Procedure to run when the game is over."""
        if not self.muted:
            config.game_over_sound.play()
        render_centered_text(self.window_size, "Game Over", 80, (255, 255, 255))
        pygame.display.update()
        pygame.time.delay(1500)

        score_filename = 'scores.txt'

        # Try to load existing scores.
        try:
            with open(score_filename, 'r') as file:
                scores = [int(line.strip().split(' ', 1)[0]) for line in file.readlines()]
        except FileNotFoundError:
            scores = []

        # Check if the player's score is a top 10 score.
        if not scores or len(scores) < 10 or self.score > min(scores):
            if config.AI_ENABLED:
                username = input_box(self.window_size, ai_mode=True)
                update_score_file(score_filename, self.score, username)
            else:
                username = input_box(self.window_size)
                update_score_file(score_filename, self.score, username)
        else:
            # If the player's score is not a top 10 score,
            pass

        self.run = False
        #pygame.display.quit()


def play():
    # Start the game
    pygame.display.set_caption('Tetris')  # Set window caption
    game_window = pygame.display.set_mode((config.window_w, config.window_h))  # Set window size
    game = Tetris(game_window, config.FAST_GAME)  # Pass the FAST_GAME variable to Tetris class

    # The contents of the launch_game() method are now here
    pygame.mixer.music.load('sound/music.mp3')
    pygame.mixer.music.set_volume(0.1)  # Set between 0.0 and 1.0
    pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely

    # Create an observer instance
    score_observer = ScoreObserver(game.window_size)
    # Add observer to the list of observers
    game.add_observer(score_observer)

    level_observer = LevelObserver(game.window_size)
    game.add_observer(level_observer)

    while game.run:
        game.game_cycle()

    # Reset the game state before starting a new game
    game.initialise()
