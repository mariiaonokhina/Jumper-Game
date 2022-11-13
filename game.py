# Jumper Game with PyGame

# Import pygame
import pygame
# Import random for random numbers
import random

# Importing keywords for convenience
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 60))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH - 25) / 2,
                SCREEN_HEIGHT - 30,
            )
        )
        self.speed = 5
    
    # Move the player based on user keypresses
    def update(self, pressed_keys):
        self.rect.move_ip(self.speed)
        
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Enemy class
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        platform_length = random.randint(20, 100)
        platform_width = 15
        self.surf = pygame.Surface((platform_length, platform_width))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(100, SCREEN_HEIGHT - 100),
                random.randint(100, SCREEN_WIDTH - 100),
            )
        )
        self.speed = random.randint(2, 6)
        
    # Move the sprite based on speed
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed = self.speed * (-1)
            self.rect.move_ip(self.speed, 0)
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed = self.speed * (-1)
            self.rect.move_ip(self.speed, 0)

# Initialize pygame
pygame.init()

# Set the window title
pygame.display.set_caption("Jumper Game!")

# Set up the drawing window with the specified width and height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADD_PLATFORM = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_PLATFORM, 5000)

# Create a Player
player = Player()

# Create groups to hold enemy sprites and all sprites
platforms = pygame.sprite.Group()    # Used for collision detection
all_sprites = pygame.sprite.Group()    # Used for rendering
all_sprites.add(player)     # Add player to all sprites

# Run until the user asks to quit
running = True

# MAIN LOOP
while running:
    # Did the user click the X button?
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop running the game
            if event.key == K_ESCAPE:
                running = False
        
        # Did the user click the "X" button?
        elif event.type == pygame.QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADD_PLATFORM:
            # Create a new enemy and add it to the sprite groups
            new_platform= Platform()
            platforms.add(new_platform)
            all_sprites.add(new_platform)

    # Get the set of pressed keys and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user input
    player.update(pressed_keys)
    
    # Update enemy position
    platforms.update()
    
    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, platforms):
        player.kill()
        running = False
    
    # Flip the display
    pygame.display.flip()

# Quitting the game
pygame.quit()