import pygame
import random

# Ініціалізація pygame
pygame.init()

# Встановлення розмірів вікна
win_size = (600, 400)
window = pygame.display.set_mode(win_size)

# Встановлення початкових координат
x = random.randint(0, 600)
y = random.randint(0, 400)

# Встановлення початкових напрямків руху
x_direction = 1
y_direction = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення координат
    x += x_direction
    y += y_direction

    # Перевірка меж і зміна напрямку руху при необхідності
    if x <= 0+11 or x >= 600-11:
        x_direction = -x_direction
    if y <= 0+11 or y >= 400-11:
        y_direction = -y_direction

    # Очищення полотна і відображення нової точки
    window.fill((55, 255, 255))
    pygame.draw.circle(window, (255, 55, 0), (x, y), 15)

    # Відображення дисплею
    pygame.display.update()

    pygame.time.delay(10)

# Завершення роботи pygame
pygame.quit()
