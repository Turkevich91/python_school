import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

jungle_bg = pygame.image.load('jungle_bg.png').convert_alpha()
jungle_bg = pygame.transform.scale(jungle_bg, (screen_width, screen_height))
# Load the dinosaur sprites
dino_walk = pygame.image.load('dino_walk.png').convert_alpha()
dino_stay = pygame.image.load('dino_stay.png').convert_alpha()
dino_sit = pygame.image.load('dino_sit.png').convert_alpha()

platform_image = pygame.image.load('platform.png').convert_alpha()
platform_image = pygame.transform.scale(platform_image, (100, 44))
# If the sprite sheet contains multiple sprites for animation, you'll need to segment them here
platforms = [
    pygame.Rect(50, 450, 100, 44),
    pygame.Rect(350, 400, 100, 44),
    pygame.Rect(600, 300, 100, 44),
    pygame.Rect(350, 200, 100, 44),
    pygame.Rect(150, 100, 100, 44),
    pygame.Rect(600, 100, 100, 44),

]

# Current sprite
current_sprite = dino_stay
# Indicates if the sprite should be flipped
flip_sprite = False

# Character settings
character_stand_height = 100  # state height
character_sit_height = 50  # state height
character = pygame.Rect(100, screen_height - 150, 70, 100)  # Update size based on sprite
character_speed = 5
character_jump = False
character_crouch = False

# Gravity
gravity = 0.5
velocity_y = 0

# Platforms
floor = pygame.Rect(0, screen_height - 30, screen_width, 30 )

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()




    # Movement controls
    keys = pygame.key.get_pressed()
    moving = False  # Track whether the character is moving
    character_crouch = False  # Track whether the character is crouching

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        character.x -= character_speed
        current_sprite = pygame.transform.flip(dino_walk, True, False)  # Change to walking sprite
        flip_sprite = True  # Flip sprite to the left
        moving = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        character.x += character_speed
        current_sprite = dino_walk
        flip_sprite = False  # No need to flip when moving right
        moving = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        current_sprite = dino_sit if not flip_sprite else pygame.transform.flip(dino_sit, True, False)
        character_crouch = True  # The character is crouching
        moving = False  # Stop moving when crouching
    if character_crouch and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        character_crouch = False
        current_sprite = dino_stay if not flip_sprite else pygame.transform.flip(dino_stay, True, False)
    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        if not character_jump:
            character_jump = True
            velocity_y = -10
            # Update sprite to jumping animation
    if not moving and not character_crouch:
        current_sprite = dino_stay if not flip_sprite else pygame.transform.flip(dino_stay, True, False)

        # Physics
    if character_jump:
        velocity_y += gravity
        character.y += velocity_y
        if character.y >= floor.y - character.height:
            character.y = floor.y - character.height
            character_jump = False
            velocity_y = 0
            # Update sprite to standing animation

    if character_crouch:
        character.y = floor.y - character.height + 50  # Adjust character's y-position when crouching

    on_platform = False
    for platform in platforms:
        if character.colliderect(platform) and velocity_y >= 0:
            character.y = platform.y + (platform.height // 2 - character.height - 10)
            on_platform = True
            character_jump = False
            velocity_y = 0
            break


    if not on_platform and not character_jump:
        # Логика прыжка
        velocity_y += gravity
        character.y += velocity_y
        if character.y > floor.y - character.height:
            character.y = floor.y - character.height
            character_jump = False
            velocity_y = 0



    # Drawing
    screen.fill((0, 0, 100))
    screen.blit(jungle_bg, (0, 0))

    # Отображение платформ
    for platform in platforms:
        # pygame.draw.rect(screen, (225, 255, 0), platform)
        screen.blit(platform_image, platform)
    # Draw the dinosaur sprite instead of a rectangle
    screen.blit(current_sprite, (character.x, character.y))

    # Draw the platforms
    # pygame.draw.rect(screen, (0, 0, 255), floor)

    # Update the window
    pygame.display.flip()
    pygame.time.Clock().tick(60)
