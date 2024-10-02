import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))

# Background image (optional)
# background = pygame.image.load('background.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load('icon.png')  # Optional game icon
# pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for _ in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

# Bullet

# Ready - Bullet is hidden
# Fire - Bullet is moving
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font(None, 32)
text_x = 10
text_y = 10

# Game Over Text
game_over_font = pygame.font.Font(None, 64)

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, idx):
    screen.blit(enemy_img[idx], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.hypot(enemy_x - bullet_x, enemy_y - bullet_y)
    return distance < 27

# Main Game Loop
running = True
while running:

    # Fill the screen with black color
    screen.fill((0, 0, 0))
    # Draw background image (optional)
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        # Keyup events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Update player position
    player_x += player_x_change
    player_x = max(0, min(player_x, 736))  # Keep player within screen bounds

    # Update enemy positions
    for i in range(num_of_enemies):

        # Game Over condition
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # Move enemies off-screen
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        # Collision detection
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            # Reset enemy position
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Draw player and score
    player(player_x, player_y)
    show_score(text_x, text_y)

    # Update the display
    pygame.display.update()
