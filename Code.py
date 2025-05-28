import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Load sound effects
eat_sound = pygame.mixer.Sound("eat.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")
pygame.mixer.music.load("bgmusic.wav")  # Background music
pygame.mixer.music.set_volume(0.5) 
pygame.mixer.music.play(-1)  # Loop forever

# Set the dimensions of the game window
red = (255, 0, 0)
blue = (51, 153, 255)
grey = (200, 200, 200)
green = (51, 102, 0)
yellow = (0, 255, 255)

# Create the game window
win_width = 600
win_height = 400

window = pygame.display.set_mode((win_width, win_height))
time.sleep(1)

# Set the window title
pygame.display.set_caption("Snake Game")

# Snake properties
snake = 10
snake_speed = 10

clock = pygame.time.Clock()

# Define fonts for rendering text
font_style = pygame.font.SysFont("bahnschrift", 26)
score_font = pygame.font.SysFont("comicsansms", 30)


# Displays the score on the screen
def user_score(score):
    number = score_font.render("Your Score: " + str(score), True, red)
    window.blit(number, [0, 0])


# Draws the snake on the screen
def game_snake(snake, snake_length_list):
    for x in snake_length_list:
        pygame.draw.rect(window, green, [x[0], x[1], snake, snake])

# Dispalys the message on the screen
def message(msg):
    mesg = font_style.render(msg, True, red)
    window.blit(mesg, [win_width / 6, win_height / 3])


# Main game loop function
def game_loop():
    gameOver = False
    gameClose = False

    x1 = win_width / 2
    y1 = win_height / 2

    x1_change = snake
    y1_change = 0

    snake_Length_list = []
    snake_length = 1   # Initial length of the snake
    
    # Food's initial position
    foodx = round(random.randrange(0, win_width - snake) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - snake) / 10.0) * 10.0

    while not gameOver:

        # Check if the game is over and display the Game Over message
        while gameClose:
            window.fill(grey)
            message("You Lost! Press P-Play Again or Q-Quit")
            user_score(snake_length - 1)
            pygame.display.update()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        gameClose = False
                    if event.key == pygame.K_p:
                        game_loop()
                        return
                    
        # Handle key presses for controlling the snake's movement
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake

        # Check if the snake hits the wall, then end the game
        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            pygame.mixer.Sound.play(gameover_sound)
            gameClose = True

        # Update the snake's position
        x1 += x1_change
        y1 += y1_change
        window.fill(grey)

        # Draw the food
        pygame.draw.rect(window, blue, [foodx, foody, snake, snake])

        # Add the snake's new position to the body
        snake_size = [x1, y1]
        snake_Length_list.append(snake_size)

        # Collision with self
        for block in snake_Length_list[:-1]:
            if block == snake_size:
                pygame.mixer.Sound.play(gameover_sound)
                gameClose = True

        if len(snake_Length_list) > snake_length:
            del snake_Length_list[0]

        game_snake(snake, snake_Length_list)  # Draw the snake on the screen
        user_score(snake_length - 1)        # Display the current score

        pygame.display.update()   # Update the screen

        # # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, win_width - snake) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - snake) / 10.0) * 10.0
            snake_length += 1
            pygame.mixer.Sound.play(eat_sound)

        clock.tick(snake_speed)

    pygame.quit()
    quit()   # Quit the game


game_loop()  # Start the game loop
pygame.mixer.music.stop()  # Stop background music when the game ends

