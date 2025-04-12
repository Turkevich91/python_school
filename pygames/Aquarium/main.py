import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция рыбок: рост, форма и репульсия")

clock = pygame.time.Clock()

# Шрифт для отображения текста
font = pygame.font.SysFont("Arial", 18)

# Глобальное ограничение на число рыбок в аквариуме
MAX_FISH = 50

def mix_colors(color1, color2):
    """
    Смешивание двух цветов путем усреднения значений RGB.
    """
    r = (color1[0] + color2[0]) // 2
    g = (color1[1] + color2[1]) // 2
    b = (color1[2] + color2[2]) // 2
    return (r, g, b)

def draw_polygon(surface, color, center, radius, n):
    """
    Отрисовка правильного многоугольника с n сторонами.
    Устанавливаем сдвиг, чтобы фигура была ориентирована "вверх".
    """
    points = []
    angle_offset = -90  # поворачиваем так, чтобы верхняя вершина была наверху
    for i in range(n):
        angle = math.radians(angle_offset + i * (360 / n))
        x_i = center[0] + radius * math.cos(angle)
        y_i = center[1] + radius * math.sin(angle)
        points.append((x_i, y_i))
    pygame.draw.polygon(surface, color, points)

class Fish:
    def __init__(self, x, y, color, initial_size=2):
        self.x = x
        self.y = y
        self.color = color  # формат (R, G, B)
        self.size = initial_size  # начинаем с маленького размера (точка)
        self.speed = random.uniform(1, 3)
        self.direction = random.uniform(0, 360)
        self.cooldown = 0      # Таймер между спариваниями (в кадрах)
        self.age = 0           # Возраст в кадрах
        self.mature_age = 200  # Рыбка считается взрослой (и может спариваться) начиная с возраста 200

    def move(self):
        rad = math.radians(self.direction)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

        # Отскок от краёв окна
        if self.x < 0 or self.x > WIDTH:
            self.direction = 180 - self.direction
        if self.y < 0 or self.y > HEIGHT:
            self.direction = -self.direction

    def update(self):
        """
        Обновление положения, возраста, таймера cooldown и постепенный рост рыбки.
        """
        self.move()
        self.age += 1
        if self.cooldown > 0:
            self.cooldown -= 1

        # Определяем целевой размер в зависимости от возраста:
        # < 100: маленькая рыбка (кружок)
        # 100 ≤ возраст < 200: восьмиугольник (но ещё не взрослая)
        # 200 ≤ возраст < 400: шестиугольник (взрослая, способна спариваться)
        # ≥ 400: треугольник (самая старая)
        if self.age < 100:
            target_size = 3    # маленькая рыбка
        elif self.age < 200:
            target_size = 6
        elif self.age < 400:
            target_size = 10
        else:
            target_size = 15

        # Медленный рост: постепенно увеличиваем размер до целевого
        growth_rate = 0.05
        if self.size < target_size:
            self.size += growth_rate

    def draw(self, surface):
        """
        Отрисовка рыбки в зависимости от её возраста:
         - Менее 100 кадров: кружок.
         - От 100 до 200: восьмиугольник.
         - От 200 до 400: шестиугольник.
         - 400 и старше: треугольник.
        """
        if self.age < 100:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
        elif self.age < 200:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 8)
        elif self.age < 400:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 6)
        else:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 3)

    def is_close(self, other):
        """
        Проверка, находятся ли две рыбки достаточно близко для спаривания.
        """
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.size + other.size + 10)

class Salmon(Fish):
    def __init__(self, x, y, color, initial_size=2):
        super().__init__(x, y, color, initial_size)
        self.speed *= 1.5  # Лосось движется быстрее обычной рыбки

    def hunt(self, fishes):
        for fish in fishes:
            if fish is not self and self.is_close(fish):
                dx = fish.x - self.x
                dy = fish.y - self.y
                if dx != 0 or dy != 0:
                    self.direction = math.degrees(math.atan2(dy, dx))
                break

def mate(fish1, fish2):
    """
    Если обе рыбки готовы к спариванию (cooldown == 0, взрослые особи: возраст >= mature_age),
    и общее число рыбок меньше MAX_FISH, создается новая рыбка.
    При этом после спаривания у рыбок устанавливается увеличенный cooldown,
    а также применяется эффект репульсии, чтобы рыбки оттолкнулись друг от друга.
    """
    if (fish1.cooldown == 0 and fish2.cooldown == 0 and
        fish1.age >= fish1.mature_age and fish2.age >= fish2.mature_age):
        new_color = mix_colors(fish1.color, fish2.color)
        new_x = (fish1.x + fish2.x) / 2
        new_y = (fish1.y + fish2.y) / 2

        # Устанавливаем увеличенный период ожидания после спаривания (например, 120 кадров)
        fish1.cooldown = 120
        fish2.cooldown = 120

        # Применяем репульсию: отталкиваем рыбок друг от друга, чтобы избежать повторного немедленного спаривания
        repulsion_factor = 10
        dx = fish1.x - fish2.x
        dy = fish1.y - fish2.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1  # чтобы избежать деления на ноль
        norm_dx = dx / distance
        norm_dy = dy / distance
        fish1.x += norm_dx * repulsion_factor
        fish1.y += norm_dy * repulsion_factor
        fish2.x -= norm_dx * repulsion_factor
        fish2.y -= norm_dy * repulsion_factor

        # Новая рыбка появляется с маленьким размером и возрастом 0
        return Fish(new_x, new_y, new_color, initial_size=2)
    else:
        return None

# Создаем список рыбок
fishes = []

# Добавляем несколько случайных рыбок
for _ in range(5):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    # Для яркости цвета используем диапазон от 50 до 255
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    fishes.append(Fish(x, y, color, initial_size=2))

# Добавляем одного лосося
x = random.randint(0, WIDTH)
y = random.randint(0, HEIGHT)
salmon_color = (255, 100, 100)
fishes.append(Salmon(x, y, salmon_color, initial_size=2))

running = True
while running:
    clock.tick(30)  # 30 кадров в секунду

    # Обработка событий: выход и добавление новой рыбки при клике мыши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            fishes.append(Fish(mouse_x, mouse_y, color, initial_size=2))

    # Обновляем состояние всех рыбок
    for fish in fishes:
        if isinstance(fish, Salmon):
            fish.hunt(fishes)
        fish.update()

    # Попытка спаривания: создаем offspring, если рыбки рядом и если общее число рыб меньше MAX_FISH
    new_fishes = []
    for i in range(len(fishes)):
        for j in range(i + 1, len(fishes)):
            if fishes[i].is_close(fishes[j]):
                if len(fishes) + len(new_fishes) < MAX_FISH:
                    offspring = mate(fishes[i], fishes[j])
                    if offspring:
                        new_fishes.append(offspring)
    fishes.extend(new_fishes)

    # Отрисовка
    screen.fill((30, 30, 30))
    instruction = font.render("Кликни, чтобы добавить новую рыбку", True, (255, 255, 255))
    screen.blit(instruction, (10, 10))
    for fish in fishes:
        fish.draw(screen)

    pygame.display.flip()

pygame.quit()
