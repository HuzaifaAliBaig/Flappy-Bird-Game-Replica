import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 288, 512

# Load assets
BG_IMAGE = pygame.image.load("background.png")
BIRD_IMAGE = pygame.image.load("bird.png")
PIPE_IMAGE = pygame.image.load("pipe.png")
GAME_FONT = pygame.font.Font(None, 32)

def create_pipe():
    pipe_height = random.randint(100, 400)
    bottom_pipe = PIPE_IMAGE.get_rect(midtop=(SCREEN_WIDTH + 100, pipe_height))
    top_pipe = PIPE_IMAGE.get_rect(midbottom=(SCREEN_WIDTH + 100, pipe_height - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for bottom_pipe, top_pipe in pipes:
        bottom_pipe.centerx -= 2
        top_pipe.centerx -= 2
    return pipes

def draw_pipes(pipes, screen):
    for bottom_pipe, top_pipe in pipes:
        if bottom_pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(PIPE_IMAGE, bottom_pipe)
        else:
            flipped_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)
            screen.blit(flipped_pipe, top_pipe)

def collision(bird_rect, pipes):
    for p in pipes:
        if bird_rect.colliderect(p[0]) or bird_rect.colliderect(p[1]):
            print("Collision detected!")
            return True
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT:
        print("Out of bounds!")
        return True
    return False

# def main():
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Flappy Bird")
#     pygame.display.set_icon(BIRD_IMAGE)
#     clock = pygame.time.Clock()
#
#     bird_rect = BIRD_IMAGE.get_rect(center=(50, SCREEN_HEIGHT // 2))
#     pipes = [create_pipe()]
#
#     gravity = 0.25
#     bird_movement = 0
#     score = 0
#
#     while True:
#         screen.blit(BG_IMAGE, (0, 0))
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     bird_movement = 0
#                     bird_movement -= 7
#
#         bird_movement += gravity
#         bird_rect.centery += bird_movement
#         screen.blit(BIRD_IMAGE, bird_rect)
#
#         pipes = move_pipes(pipes)
#         draw_pipes(pipes, screen)
#
#         if collision(bird_rect, pipes):
#             break
#
#         if pipes[0].centerx < -50:
#             pipes.pop(0)
#             pipes.append(create_pipe())
#             score += 1
#
#         score_text = GAME_FONT.render(f"Score: {score}", True, (255, 255, 255))
#         screen.blit(score_text, (10, 10))
#
#         pygame.display.update()
#         clock.tick(60)
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    pygame.display.set_icon(BIRD_IMAGE)
    clock = pygame.time.Clock()

    bird_rect = BIRD_IMAGE.get_rect(center=(10, SCREEN_HEIGHT // 2))
    pipes = []

    gravity = 0.25
    bird_movement = 0
    score = 0
    game_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                if game_active and event.key == pygame.K_SPACE:
                    bird_movement = 0
                    bird_movement -= 7

        screen.blit(BG_IMAGE, (0, 0))

        if game_active:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            if bird_rect.top <= 0:
                bird_rect.top = 0
            if bird_rect.bottom >= SCREEN_HEIGHT:
                bird_rect.bottom = SCREEN_HEIGHT
            screen.blit(BIRD_IMAGE, bird_rect)

            pipes = move_pipes(pipes)
            draw_pipes(pipes, screen)

            if collision(bird_rect, pipes):
                game_active = False

            if pipes and pipes[0].centerx < -50:
                pipes.pop(0)
                pipes.append(create_pipe())
                score += 1

            score_text = GAME_FONT.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
        else:
            start_text = GAME_FONT.render("Press Enter to Start", True, (255, 255, 255))
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
