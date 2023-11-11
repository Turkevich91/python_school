import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball settings
ball_speed_x = 2
ball_speed_y = 2
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)

# Paddle settings
paddle_speed = 3
player_paddle = pygame.Rect(50, screen_height / 2 - 70, 10, 140)
computer_paddle = pygame.Rect(screen_width - 60, screen_height / 2 - 70, 10, 140)

# Score variables
player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed_x *= -1

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_s] and player_paddle.bottom < screen_height:
        player_paddle.y += paddle_speed

    # Computer AI movement
    if computer_paddle.centery < ball.centery:
        computer_paddle.y += min(paddle_speed, ball.centery - computer_paddle.centery)
    elif computer_paddle.centery > ball.centery:
        computer_paddle.y -= min(paddle_speed, computer_paddle.centery - ball.centery)

    # Prevent the computer paddle from moving out of the screen
    if computer_paddle.top <= 0:
        computer_paddle.top = 0
    if computer_paddle.bottom >= screen_height:
        computer_paddle.bottom = screen_height

    # Ball reset if it goes past paddle
    if ball.left <= 0:
        ball_speed_x *= -1
        computer_score += 1
        ball.center = (screen_width / 2, screen_height / 2)
        pygame.time.delay(500)
    elif ball.right >= screen_width:
        ball_speed_x *= -1
        player_score += 1
        ball.center = (screen_width / 2, screen_height / 2)
        pygame.time.delay(500)

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Scoring display
    player_text = font.render(f'{player_score}', False, WHITE)
    screen.blit(player_text, (screen_width / 2 + 20, 20))

    computer_text = font.render(f'{computer_score}', False, WHITE)
    screen.blit(computer_text, (screen_width / 2 - computer_text.get_width() - 20, 20))

    # Updating the window
    pygame.display.flip()
    pygame.time.Clock().tick(60)
