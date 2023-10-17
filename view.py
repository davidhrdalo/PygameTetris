import pygame
from controller import *
import logic.config as config


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FONT_SIZE = 36
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Start Screen")

# Create a font
font = pygame.font.Font(None, FONT_SIZE)

# Define buttons
play_button = pygame.Rect(400, 200, 200, 50)  # 'Play' button
exit_button = pygame.Rect(400, 440, 200, 50)  # 'Exit' button
score_button = pygame.Rect(400, 260, 200, 50)  # 'Score' button
configure_button = pygame.Rect(400, 320, 200, 50)  # 'Configure' button

back_button = pygame.Rect(20, 20, 80, 40)  # 'Back' button

# Configuration options
config_options = {
    "Game Mode": ["Normal Game", "Game with Extension"],
    "Field Size": ["Small 16x8", "Medium 20x10", "Large 20x15"],
    "Block Speed": ["Normal", "Fast"],
    "Play as AI": ["No", "Yes"]  # Include "Yes" option here
}

# Selected configuration
selected_config = {
    "Game Mode": "Normal Game",
    "Field Size": "Medium 20x10",
    "Block Speed": "Normal",
    "Play as AI": "No"
}


def read_top_10_players_from_file(filename):
    with open(filename, 'r') as file:
        # Read each line, split it, and store player and score
        players = [(line.split()[1], int(line.split()[0])) for line in file.readlines()]

        # Sort players based on score in descending order
        players.sort(key=lambda x: x[1], reverse=True)

        # Take top 10 players
        top_10_players = players[:10]

    return top_10_players

# Read from scores.txt
top_10_players = read_top_10_players_from_file('scores.txt')
print(top_10_players)

# Load the fancy font
fancy_font = pygame.font.Font("YoungSerif-Regular.ttf", 22)

user_control_button = pygame.Rect(300, 380, 200, 50)  # 'User Control' button
def draw_start_screen():
    # Load the background image
    background_image = pygame.image.load("game_page_background.jpg")

    # Blit the background image
    screen.blit(background_image, (0, 0))

    # Define dark blue color
    dark_blue = (0, 0, 139)  # RGB values for dark blue
    light_gray = (200, 200, 200)  # RGB values for light gray

    # Draw the game title with a fancy font
    title_text = fancy_font.render("Tetris", True, light_gray )  # Set the text color to sky blue
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_text, title_rect)

    # Get the current year and course code (you need to update these)
    current_year = "2023"  # Update with the current year
    course_code = "3815ICT/7805ICT"  # Update with the course code
    year_text = fancy_font.render(f"Year: {current_year}", True, light_gray )  # Set the text color to sky blue
    course_text = fancy_font.render(f"Course: {course_code}", True, light_gray )  # Set the text color to sky blue

    # Adjust the vertical positioning
    gap = 10
    title_height = title_rect.height
    year_rect = year_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + title_height + gap))
    course_rect = course_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + title_height + year_rect.height + gap))

    screen.blit(year_text, year_rect)
    screen.blit(course_text, course_rect)

    # Draw the 'Play' button
    pygame.draw.rect(screen, BUTTON_COLOR, play_button)
    play_text = font.render("Play", True, BUTTON_TEXT_COLOR)
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

    # Draw the 'Exit' button
    pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
    exit_text = font.render("Exit", True, BUTTON_TEXT_COLOR)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    screen.blit(exit_text, exit_text_rect)

    # Draw the 'Score' button
    pygame.draw.rect(screen, BUTTON_COLOR, score_button)
    score_text = font.render("Score", True, BUTTON_TEXT_COLOR)
    score_text_rect = score_text.get_rect(center=score_button.center)
    screen.blit(score_text, score_text_rect)

    # Draw the 'Configure' button
    pygame.draw.rect(screen, BUTTON_COLOR, configure_button)
    configure_text = font.render("Configure", True, BUTTON_TEXT_COLOR)
    configure_text_rect = configure_text.get_rect(center=configure_button.center)
    screen.blit(configure_text, configure_text_rect)

    # Define the 'User Control' button
    user_control_button = pygame.Rect(400, 380, 200, 50)  # 'User Control' button
    pygame.draw.rect(screen, BUTTON_COLOR, user_control_button)
    user_control_text = font.render("User Control", True, BUTTON_TEXT_COLOR)
    user_control_text_rect = user_control_text.get_rect(center=user_control_button.center)
    screen.blit(user_control_text, user_control_text_rect)

    # Define the color white
    white = (255, 255, 255)

    # Draw the list of students in your group (you need to update this)
    students = [
        "David Haardelo",
        "Syed Tahoor Imam",
        "Asad Bismil",
        "Malhar",
    ]

    # Define starting position for the text
    start_x = 10  # Starting x-coordinate (10 pixels from the left edge)
    start_y = 50  # Starting y-coordinate (10 pixels from the top edge)

    # Render the "Students:" text
    student_text = fancy_font.render("Students:", True, white)  # Set the text color to white
    screen.blit(student_text, (start_x, start_y))

    # Render each student's name
    for i, student in enumerate(students, 1):
        student_info = fancy_font.render(f"{i}. {student}", True, white)  # Set the text color to white
        screen.blit(student_info, (start_x, start_y + i * FONT_SIZE))

    pygame.display.flip()






def draw_score_screen():
    # Load the high score background image
    high_score_background = pygame.image.load("game_page_background.jpg")  # Update the path to your background image

    # Blit the background image
    screen.blit(high_score_background, (0, 0))

    # Calculate the total height of the top 10 players section
    total_height = len(top_10_players) * FONT_SIZE

    # Calculate the vertical position to center the top 10 players
    y_offset = (SCREEN_HEIGHT - total_height) // 2

    # Display top 10 players
    for i, (player, score) in enumerate(top_10_players, 1):
        player_text = font.render(f"{i}. {player} - {score}", True, BUTTON_TEXT_COLOR)
        player_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(player_text, player_rect)
        y_offset += FONT_SIZE

    # Draw the 'Back' button
    pygame.draw.rect(screen, BUTTON_COLOR, back_button)
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_text_rect = back_text.get_rect(topleft=(20, 20))
    screen.blit(back_text, back_text_rect)

    pygame.display.flip()



def draw_configure_screen():
    global AI_ENABLED, FAST_GAME, EXTENDED_GAME, LARGE_BOARD, SMALL_BOARD, ROWS, COLS

    # Load the configure page background image
    configure_page_background = pygame.image.load("game_page_background.jpg")  # Update the path to your background image

    # Blit the background image
    screen.blit(configure_page_background, (0, 0))

    # Define the y-offset for rendering options
    y_offset = 150

    # Display configuration options
    for option, values in config_options.items():
        option_text = font.render(option, True, BUTTON_TEXT_COLOR)
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(option_text, option_rect)
        y_offset += FONT_SIZE

        for value in values:
            value_text = font.render(value, True, BUTTON_TEXT_COLOR)
            value_rect = value_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))

            # Highlight the selected option
            if selected_config[option] == value:
                pygame.draw.rect(screen, BUTTON_TEXT_COLOR, value_rect, 2)

            # Check if an option is clicked
            if value_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selected_config[option] = value

                if option == "Play as AI":
                    config.AI_ENABLED = value == "Yes"
                elif option == "Block Speed":
                    config.FAST_GAME = value == "Fast"
                elif option == "Game Mode":
                    config.EXTENDED_GAME = value == "Game with Extension"
                elif option == "Field Size":
                    if value == "Large (20x40)":
                        config.LARGE_BOARD = True
                        config.ROWS, config.COLS = 20, 15
                    elif value == "Small (10x20)":
                        config.SMALL_BOARD = True
                        config.ROWS, config.COLS = 16, 8
                    else:
                        config.LARGE_BOARD = False
                        config.SMALL_BOARD = False
                        config.ROWS, config.COLS = 20, 10

            screen.blit(value_text, value_rect)
            y_offset += FONT_SIZE

    # Draw the 'Back' button
    pygame.draw.rect(screen, BUTTON_COLOR, back_button)
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_text_rect = back_text.get_rect(topleft=(20, 20))
    screen.blit(back_text, back_text_rect)

    pygame.display.flip()







def draw_user_control_screen():
    # Clear the screen
    screen.fill((0, 0, 0))

    # Define sky blue color
    sky_blue = (135, 206, 235)

    # Define the smaller font
    SMALL_FONT_SIZE = 18
    small_font = pygame.font.Font(None, SMALL_FONT_SIZE)

    # Draw the user manual title with a fancy font
    user_manual_title = fancy_font.render("Tetris Game User Manual", True, sky_blue)
    user_manual_title_rect = user_manual_title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(user_manual_title, user_manual_title_rect)

    # Add the user manual content with the smaller font
    user_manual_content = [
        "Welcome to Tetris User Manual!",
        "Controls:",
        "- Use the LEFT and RIGHT arrow keys to move the falling tetromino left and right.",
        "- Use the UP arrow key to rotate the tetromino.",
        "- Use the DOWN arrow key to make the tetromino fall faster.",
        "- Press the SPACEBAR to make the tetromino instantly reach the bottom.",
        "Objective:",
        "The objective of Tetris is to clear lines by filling them with tetrominoes. The more lines you clear, the higher your score.",
        "Enjoy the game!",
    ]

    y_offset = 150
    for line in user_manual_content:
        line_text = small_font.render(line, True, BUTTON_TEXT_COLOR)  # Use the smaller font here
        line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(line_text, line_rect)
        y_offset += SMALL_FONT_SIZE

    # Draw the 'Back' button
    pygame.draw.rect(screen, BUTTON_COLOR, back_button)
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_text_rect = back_text.get_rect(topleft=(20, 20))
    screen.blit(back_text, back_text_rect)

    pygame.display.flip()




# ... (previous code)

# Load the background image
background_image = pygame.image.load("game_page_background.jpg")

# Define the main function
def main():
    running = True
    show_score_screen = False
    show_configure_screen = False
    show_start_screen = True
    show_user_control_screen = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if show_start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if exit_button.collidepoint(event.pos):
                        running = False
                    elif play_button.collidepoint(event.pos):
                        play()
                    elif score_button.collidepoint(event.pos):
                        show_score_screen = True
                        show_start_screen = False
                    elif configure_button.collidepoint(event.pos):
                        show_configure_screen = True
                        show_start_screen = False
                    elif user_control_button.collidepoint(event.pos):
                        show_user_control_screen = True
                        show_start_screen = False

            elif show_score_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        show_score_screen = False
                        show_start_screen = True

            elif show_configure_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        show_configure_screen = False
                        show_start_screen = True
                    # Handle the "Confirm" button click (if applicable)

            elif show_user_control_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button.collidepoint(event.pos):
                        show_user_control_screen = False
                        show_start_screen = True

        screen.fill((0, 0, 0))

        if show_start_screen:
            screen.blit(background_image, (0, 0))
            draw_start_screen()
        elif show_score_screen:
            draw_score_screen()
        elif show_configure_screen:
            draw_configure_screen()
        elif show_user_control_screen:
            draw_user_control_screen()

        pygame.display.flip()

if __name__ == "__main__":
    main()


