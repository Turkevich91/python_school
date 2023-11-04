import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Встановлення розмірів екрану
screen = pygame.display.set_mode((800, 600))

# Встановлення швидкості м'яча і ракеток
ball_speed = [1, 1]
paddle_speed = 1

# Створення м'яча і ракеток
ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()
paddle = pygame.image.load("paddle.png")
paddle1 = paddle.get_rect()
paddle2 = paddle.get_rect()

# Встановлення початкових позицій ракеток
paddle1.midleft = (50, 300)
paddle2.midright = (750, 300)

# Встановлення шрифту для відображення рахунку
font = pygame.font.Font(None, 36)

# Ініціалізація рахунку гравців
score_player_1 = 0
score_player_2 = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Оновлення позиції м'яча
    ballrect = ballrect.move(ball_speed)

    # Відбивання м'яча від меж екрану
    if ballrect.left < 0:
        ball_speed[0] = -ball_speed[0]
        score_player_2 += 1  # Додаємо очко другому гравцю
    if ballrect.right > 800:
        ball_speed[0] = -ball_speed[0]
        score_player_1 += 1  # Додаємо очко першому гравцю
    if ballrect.top < 0 or ballrect.bottom > 600:
        ball_speed[1] = -ball_speed[1]

    # Оновлення позицій ракеток
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1 = paddle1.move([0, -paddle_speed])
    if keys[pygame.K_s]:
        paddle1 = paddle1.move([0, paddle_speed])
    if keys[pygame.K_UP]:
        paddle2 = paddle2.move([0, -paddle_speed])
    if keys[pygame.K_DOWN]:
        paddle2 = paddle2.move([0, paddle_speed])

    # Відбивання м'яча від ракеток
    if paddle1.colliderect(ballrect) or paddle2.colliderect(ballrect):
        ball_speed[0] = -ball_speed[0]

    # Малювання м'яча і ракеток на екрані
    screen.fill((0, 0, 0))
    screen.blit(ball, ballrect)
    screen.blit(paddle, paddle1)
    screen.blit(paddle, paddle2)

    # Відображення рахунку
    score_text = font.render(f"{score_player_1} : {score_player_2}", True, (255, 255, 255))
    screen.blit(score_text, (375, 10))

    pygame.display.flip()
    pygame.time.delay(5)
