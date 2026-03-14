import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time-Twister Arena")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player setup
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 100]
player_speed = 5

# Enemy setup
enemy_size = 40
red_enemy_list = []  # Standard enemies
green_enemy_list = []  # Special enemies
red_enemy_speed = 3
green_enemy_speed = 2
RED_ENEMY_SPAWN_TIME = 30  # Frames between red enemy spawns
GREEN_ENEMY_SPAWN_TIME = 120  # Frames between green enemy spawns
red_enemy_timer = 0
green_enemy_timer = 0

# Bullet setup
bullet_list = []
bullet_size = 10
bullet_speed = 10

# Time manipulation states
time_slowed = False
time_reversed = False

# Score
score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Helper functions
def draw_player(position):
    pygame.draw.rect(screen, BLUE, (position[0], position[1], player_size, player_size))

def spawn_red_enemy():
    x_pos = random.randint(0, WIDTH - enemy_size)
    y_pos = random.randint(-100, -enemy_size)  # Spawn above the screen
    red_enemy_list.append([x_pos, y_pos])

def spawn_green_enemy():
    x_pos = random.randint(0, WIDTH - enemy_size)
    y_pos = random.randint(-100, -enemy_size)  # Spawn above the screen
    green_enemy_list.append([x_pos, y_pos])

def draw_red_enemies():
    for enemy in red_enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

def draw_green_enemies():
    for enemy in green_enemy_list:
        pygame.draw.rect(screen, GREEN, (enemy[0], enemy[1], enemy_size, enemy_size))

def update_red_enemies():
    for enemy in red_enemy_list:
        enemy[1] += red_enemy_speed
    # Remove enemies that move off the screen
    red_enemy_list[:] = [enemy for enemy in red_enemy_list if enemy[1] < HEIGHT]

def update_green_enemies():
    for enemy in green_enemy_list:
        enemy[1] += green_enemy_speed
    # Remove enemies that move off the screen
    green_enemy_list[:] = [enemy for enemy in green_enemy_list if enemy[1] < HEIGHT]

def draw_bullets():
    for bullet in bullet_list:
        pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_size, bullet_size))

def update_bullets():
    for bullet in bullet_list:
        bullet[1] -= bullet_speed
    # Remove bullets that leave the screen
    bullet_list[:] = [bullet for bullet in bullet_list if bullet[1] > 0]

def check_bullet_collision():
    global red_enemy_list, green_enemy_list, bullet_list, score
    for bullet in bullet_list[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)

        # Check collision with red enemies
        for enemy in red_enemy_list[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullet_list.remove(bullet)
                red_enemy_list.remove(enemy)
                score += 1  # Red enemy worth 1 point
                break

        # Check collision with green enemies
        for enemy in green_enemy_list[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullet_list.remove(bullet)
                green_enemy_list.remove(enemy)
                score += 2  # Green enemy worth 2 points
                break

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Fire bullet
                bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]]
                bullet_list.append(bullet_pos)

    # Player movement (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos[0] > 0:  # Move left
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size:  # Move right
        player_pos[0] += player_speed
    if keys[pygame.K_w] and player_pos[1] > 0:  # Move up
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size:  # Move down
        player_pos[1] += player_speed

    # Time manipulation keys
    if keys[pygame.K_f]:  # Slow down time
        time_slowed = True
    else:
        time_slowed = False

    if keys[pygame.K_r]:  # Reverse time (placeholder functionality)
        time_reversed = True
    else:
        time_reversed = False

    # Enemy spawning
    if red_enemy_timer == 0:
        spawn_red_enemy()
        red_enemy_timer = RED_ENEMY_SPAWN_TIME
    else:
        red_enemy_timer -= 1

    if green_enemy_timer == 0:
        spawn_green_enemy()
        green_enemy_timer = GREEN_ENEMY_SPAWN_TIME
    else:
        green_enemy_timer -= 1

    # Update game elements
    update_red_enemies()
    update_green_enemies()
    update_bullets()
    check_bullet_collision()

    # Check collisions (player vs. any enemy)
    if any(
        pygame.Rect(player_pos[0], player_pos[1], player_size, player_size).colliderect(
            pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        )
        for enemy in red_enemy_list + green_enemy_list
    ):
        running = False  # End the game if the player collides with an enemy

    # Drawing elements
    draw_player(player_pos)
    draw_red_enemies()
    draw_green_enemies()
    draw_bullets()

    # Display time manipulation status
    status_text = f"Time Slowed: {time_slowed} | Time Reversed: {time_reversed}"
    text_surface = font.render(status_text, True, WHITE)
    screen.blit(text_surface, (10, 10))

    # Display score
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, WHITE)
    screen.blit(score_surface, (10, 40))

    # Update screen and manage FPS
    pygame.display.flip()
    clock.tick(FPS if not time_slowed else FPS // 2)  # Slow down time effect

# Quit pygame
pygame.quit()
sys.exit()
