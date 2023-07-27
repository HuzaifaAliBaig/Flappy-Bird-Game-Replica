import pygame
import random
import sys

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
GRAVITY = 0.5    
FLAP_SPEED = -4
PIPE_GAP = 150
PIPE_SPACING = 300
PIPE_WIDTH = 50
BIRD_WIDTH = 50
BIRD_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird By Huzaifa Baig")

# Load assets
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.image.load("pipe.png")
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_SPEED

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT or self.y < 0

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP

    def update(self):
        self.x -= 2

    def draw(self):
        screen.blit(pipe_image, (self.x, 0), (0, 0, PIPE_WIDTH, self.top_height))
        screen.blit(pipe_image, (self.x, SCREEN_HEIGHT - self.bottom_height), (0, 500 - self.bottom_height, PIPE_WIDTH, self.bottom_height))

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

# Game setup
def reset_game():
    global bird, pipes, score
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * PIPE_SPACING) for i in range(3)]
    score = 0

reset_game()
clock = pygame.time.Clock()
game_active = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    game_active = True
                    reset_game()
                else:
                    bird.flap()

    # Update
    if game_active:
        bird.update()

        # Collision detection
        if bird.is_off_screen():
            game_active = False

        for pipe in pipes:
            pipe.update()
            if pipe.is_off_screen():
                score += 1
                pipes.remove(pipe)

        for pipe in pipes:
            if pipe.x <= bird.x + BIRD_WIDTH // 2 <= pipe.x + PIPE_WIDTH:
                if bird.y < pipe.top_height or bird.y > SCREEN_HEIGHT - pipe.bottom_height:
                    game_active = False

        # Spawn new pipes
        if pipes[-1].x <= SCREEN_WIDTH - PIPE_SPACING:
            pipes.append(Pipe(SCREEN_WIDTH))

    # Draw
    screen.blit(background_image, (0, 0))  # Draw the background first

    for pipe in pipes:
        pipe.draw()

    bird.draw()

    if not game_active:
        font = pygame.font.Font(None, 36)
        if score == 0:
            text_surface = font.render("Press Space to Begin", True, BLACK)
        else:
            text_surface = font.render(f"Try Again! Score: {score}. Press Space to Play Again", True, BLACK)

        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

    if game_active:
        # Draw score
        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)
