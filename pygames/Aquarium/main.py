import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aquarium with Fish and Slow Bubbles")

clock = pygame.time.Clock()

# Load background image
try:
    bg = pygame.image.load("bg.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
except Exception as e:
    print("Error loading bg.png:", e)
    bg = None  # if the file is not found, fallback to a solid color background

# Font for displaying text
font = pygame.font.SysFont("Arial", 18)

# Maximum number of fish in the aquarium
MAX_FISH = 50


# ====================================================================
# Bubble class (Bubbles will move upward slowly)
# ====================================================================
class Bubble:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        # Bubbles appear somewhere in the lower part of the screen
        self.y = random.randint(HEIGHT - 100, HEIGHT)
        self.radius = random.randint(3, 8)
        # Set speed: roughly 3 times slower than the base speed
        self.speed = random.uniform(1, 3) / 3.0
        # Bubble color (light blue)
        self.color = (200, 230, 255)

    def update(self):
        # Move upward; with reduced speed
        self.y -= self.speed
        # If the bubble goes off the top of the screen, reset it to the bottom with a new x position
        if self.y + self.radius < 0:
            self.y = HEIGHT + self.radius
            self.x = random.randint(50, WIDTH - 50)

    def draw(self, surface):
        # Draw the bubble outline
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius, 1)


# ====================================================================
# Fish and Salmon classes
# ====================================================================
def mix_colors(color1, color2):
    """ Average two colors (RGB channels) and return the new color. """
    r = (color1[0] + color2[0]) // 2
    g = (color1[1] + color2[1]) // 2
    b = (color1[2] + color2[2]) // 2
    return (r, g, b)


def draw_polygon(surface, color, center, radius, n):
    """
    Draw a regular polygon with n sides.
    The polygon is rotated so that the top vertex is upward.
    """
    points = []
    angle_offset = -90  # so that the top vertex is on top
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
        self.color = color  # (R, G, B)
        self.size = initial_size  # start with a very small size (a dot)
        self.speed = random.uniform(1, 3)
        self.direction = random.uniform(0, 360)
        self.cooldown = 0  # Timer between mating events (in frames)
        self.age = 0  # Age in frames
        self.mature_age = 200  # Considered mature (able to mate) at age 200 (hexagon shape and above)

    def move(self):
        rad = math.radians(self.direction)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)
        # Bounce off the screen edges
        if self.x < 0 or self.x > WIDTH:
            self.direction = 180 - self.direction
        if self.y < 0 or self.y > HEIGHT:
            self.direction = -self.direction

    def update(self):
        self.move()
        self.age += 1
        if self.cooldown > 0:
            self.cooldown -= 1

        # Set the target size based on age:
        # Age < 100: circle; 100–200: octagon; 200–400: hexagon; 400+: triangle.
        if self.age < 100:
            target_size = 3
        elif self.age < 200:
            target_size = 6
        elif self.age < 400:
            target_size = 10
        else:
            target_size = 15
        # Gradually grow the fish to the target size
        growth_rate = 0.05
        if self.size < target_size:
            self.size += growth_rate

    def draw(self, surface):
        # Draw the fish in different shapes according to its age:
        # < 100: circle; 100–200: octagon; 200–400: hexagon; 400+: triangle.
        if self.age < 100:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
        elif self.age < 200:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 8)
        elif self.age < 400:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 6)
        else:
            draw_polygon(surface, self.color, (self.x, self.y), self.size, 3)

    def is_close(self, other):
        # Check if two fish are close enough for mating interaction.
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < (self.size + other.size + 10)


class Salmon(Fish):
    def __init__(self, x, y, color, initial_size=2):
        super().__init__(x, y, color, initial_size)
        self.speed *= 1.5  # Salmon moves faster than a normal fish

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
    If both fish are ready (cooldown == 0), are mature (age >= mature_age),
    and the total number of fish is less than MAX_FISH, perform mating.
    After mating, both fish get an increased cooldown and are repelled from each other.
    """
    if (fish1.cooldown == 0 and fish2.cooldown == 0 and
            fish1.age >= fish1.mature_age and fish2.age >= fish2.mature_age):
        new_color = mix_colors(fish1.color, fish2.color)
        new_x = (fish1.x + fish2.x) / 2
        new_y = (fish1.y + fish2.y) / 2

        fish1.cooldown = 120
        fish2.cooldown = 120

        # Repulsion: move the fish away from each other
        repulsion_factor = 10
        dx = fish1.x - fish2.x
        dy = fish1.y - fish2.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        norm_dx = dx / distance
        norm_dy = dy / distance
        fish1.x += norm_dx * repulsion_factor
        fish1.y += norm_dy * repulsion_factor
        fish2.x -= norm_dx * repulsion_factor
        fish2.y -= norm_dy * repulsion_factor

        return Fish(new_x, new_y, new_color, initial_size=2)
    else:
        return None


# ====================================================================
# Create lists for fish and bubbles
# ====================================================================
fishes = []

# Add several random fish
for _ in range(5):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    fishes.append(Fish(x, y, color, initial_size=2))

# Add one salmon
x = random.randint(0, WIDTH)
y = random.randint(0, HEIGHT)
salmon_color = (255, 100, 100)
fishes.append(Salmon(x, y, salmon_color, initial_size=2))

# Create a list of bubbles
bubbles = [Bubble() for _ in range(10)]


# ====================================================================
# Function to draw the background
# ====================================================================
def draw_background(surface):
    if bg:
        surface.blit(bg, (0, 0))
    else:
        surface.fill((0, 0, 80))  # fallback solid background if bg.png is not found


# ====================================================================
# Main game loop
# ====================================================================
running = True
while running:
    clock.tick(30)  # 30 frames per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add a new fish on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            fishes.append(Fish(mouse_x, mouse_y, color, initial_size=2))

    # Draw the background image
    draw_background(screen)

    # Update and draw bubbles
    for bubble in bubbles:
        bubble.update()
        bubble.draw(screen)

    # Update and draw fish
    for fish in fishes:
        if isinstance(fish, Salmon):
            fish.hunt(fishes)
        fish.update()
    # Check for mating: create offspring if fish are close and total fish < MAX_FISH
    new_fishes = []
    for i in range(len(fishes)):
        for j in range(i + 1, len(fishes)):
            if fishes[i].is_close(fishes[j]):
                if len(fishes) + len(new_fishes) < MAX_FISH:
                    offspring = mate(fishes[i], fishes[j])
                    if offspring:
                        new_fishes.append(offspring)
    fishes.extend(new_fishes)

    for fish in fishes:
        fish.draw(screen)

    # Draw instructions
    instruction = font.render("Click to add a new fish", True, (255, 255, 255))
    screen.blit(instruction, (10, 10))

    pygame.display.flip()

pygame.quit()
