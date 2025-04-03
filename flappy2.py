import pygame
import sys
import random

# Game variables
floor_x_position = 0
bg_x_position = 0
gravity = 0.1
bird_y_movement = 0
game_active = False
game_over = False
game_paused = False
score = 0
high_score = 0

# Load bird assets
bird_upflap = pygame.image.load('assets/bluebird-upflap.png')
bird_midflap = pygame.image.load('assets/bluebird-midflap.png')
bird_downflap = pygame.image.load('assets/bluebird-downflap.png')
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(78, 256))

# Functions
def draw_bg():
    if (score // 10) % 2 == 1:
        screen.blit(bg_surface_night, (bg_x_position, 0))
        screen.blit(bg_surface_night, (bg_x_position + 288, 0))
    else:
        screen.blit(bg_surface_day, (bg_x_position, 0))
        screen.blit(bg_surface_day, (bg_x_position + 288, 0))

def floor_varathu():
    screen.blit(floor_surface, (floor_x_position, 450))
    screen.blit(floor_surface, (floor_x_position + 288, 450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(400, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(400, random_pipe_pos - 200))  # Increase gap 
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2  # Maintain consistent pipe speed
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        hit_sound.play()
        return False
    return True

def update_score(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx == bird_rect.centerx:
            score += 1
            point_sound.play()
    return pipes

def display_score(game_state):
    if game_state == 'main_game':
        score_surface = font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = font.render(f'Score: {score}', True, WHITE)
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = font.render(f'High Score: {high_score}', True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)

def animate_bird():
    global bird_surface, bird_rect, bird_index
    bird_index = (bird_index + 1) % len(bird_frames)
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center=(78, bird_rect.centery))

def start_screen():
    screen.blit(welcome_surface, welcome_rect)

def game_over_screen():
    screen.blit(game_over_surface, game_over_rect)
    display_score('game_over')

def pause_screen():
    screen.blit(pause_surface, pause_rect)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

# Load assets
bg_surface_day = pygame.image.load('assets/background-day.png')
bg_surface_night = pygame.image.load('assets/background-night.png')
floor_surface = pygame.image.load('assets/base.png')
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)  # Increase time interval
ANIMATESURF = pygame.USEREVENT + 1
pygame.time.set_timer(ANIMATESURF, 400)  # Timer to change bird flapping

# Load sounds
flap_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')

# Load welcome and game over message
welcome_surface = pygame.image.load('assets/message.png')
welcome_rect = welcome_surface.get_rect(center=(144, 256))
game_over_surface = pygame.image.load('assets/gameover.png')
game_over_rect = game_over_surface.get_rect(center=(144, 256))

# Create pause surface
font = pygame.font.Font(None, 48)
pause_surface = font.render("Paused", True, (255, 255, 255))
pause_rect = pause_surface.get_rect(center=(144, 256))

pipe_height = [i for i in range(200, 401, 50)]  # Updated to a smaller range of heights

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
while True:
    keys = pygame.key.get_pressed()  # Check the state of all keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Start the game by pressing SPACE
                if not game_active and not game_over:
                    game_active = True
                    flap_sound.play()
                    pygame.time.set_timer(SPAWNPIPE, 2000)  # Increase time interval to 2000 ms
                elif game_active:
                    bird_y_movement = 0
                    bird_y_movement -= 3  # Slower upward movement
                    flap_sound.play()
                elif game_over:
                    game_over = False
                    game_active = False
                    bird_rect.center = (78, 256)
                    bird_y_movement = 0
                    pipe_list.clear()
                    score = 0  # Reset score
            if event.key == pygame.K_p:  # Pause and play button
                if game_active and not game_paused:
                    game_paused = True
                    pygame.time.set_timer(SPAWNPIPE, 0)
                elif game_paused:
                    game_paused = False
                    pygame.time.set_timer(SPAWNPIPE, 2000)  # Increase time interval to 2000 ms

        if event.type == SPAWNPIPE and game_active and not game_paused:
            pipe_list.extend(create_pipe())
            point_sound.play()

        if event.type == ANIMATESURF:
            animate_bird()

    if game_active and not game_paused:
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:  # Check if space or up arrow key is pressed
            bird_y_movement = 0
            bird_y_movement -= 1  # Slower upward movement
            flap_sound.play()

        if keys[pygame.K_DOWN]:  # Check if down arrow key is pressed
            bird_y_movement += 0.05  # increase downward movement

        floor_x_position -= 1
        bg_x_position -= 1

        draw_bg()

        pipe_list = move_pipes(pipe_list)
        pipe_list = update_score(pipe_list)
        draw_pipes(pipe_list)

        bird_y_movement += gravity
        bird_rect.centery += bird_y_movement
        screen.blit(bird_surface, bird_rect)

        if not check_collision(pipe_list):
            game_active = False
            game_over = True
            if score > high_score:
                high_score = score  # Update high score

        floor_varathu()
        if floor_x_position <= -288:
            floor_x_position = 0
        if bg_x_position <= -288:
            bg_x_position = 0
        
        display_score('main_game')
    elif game_paused:
        draw_bg()
        floor_varathu()
        pause_screen()
    else:
        # Display start screen if the game has not started yet
        if game_over:
            draw_bg()
            floor_varathu()
            game_over_screen()
        else:
            draw_bg()
            floor_varathu()
            start_screen()

    # Draw pause and play buttons
    pygame.draw.rect(screen, WHITE, pygame.Rect(10, 10, 50, 30))
    pygame.draw.rect(screen, WHITE, pygame.Rect(70, 10, 50, 30))
    
    font = pygame.font.Font(None, 24)
    pause_text = font.render("Pause", True, BLACK)
    play_text = font.render("Play", True, BLACK)

    screen.blit(pause_text, (20, 15))
    screen.blit(play_text, (80, 15))

    pygame.display.update()
    clock.tick(60)
