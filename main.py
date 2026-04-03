import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sounds
laser_sound = pygame.mixer.Sound('shooter/assets/Bonus/sfx_laser1.ogg')
zap_sound = pygame.mixer.Sound('shooter/assets/Bonus/sfx_zap.ogg')
shield_up_sound = pygame.mixer.Sound('shooter/assets/Bonus/sfx_shieldUp.ogg')
lose_sound = pygame.mixer.Sound('shooter/assets/Bonus/sfx_lose.ogg')

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# High score
HIGH_SCORE_FILE = 'high_score.txt'

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

high_score = load_high_score()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Shooter Game")
clock = pygame.time.Clock()

# Create background
background = pygame.image.load('shooter/assets/Backgrounds/darkPurple.png').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('shooter/assets/PNG/playerShip1_blue.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.health = 100
        self.last_shot = 0
        self.shoot_cooldown = 300  # ms
        self.multishot = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown:
            self.last_shot = now
            bullets = [Bullet(self.rect.centerx, self.rect.top)]
            if self.multishot:
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top + 5))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top + 5))
            return bullets
        return []

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('shooter/assets/PNG/Lasers/laserBlue01.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (5, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        if type == 'health':
            self.image = pygame.image.load('shooter/assets/PNG/Power-ups/powerupBlue.png').convert_alpha()
        elif type == 'speed':
            self.image = pygame.image.load('shooter/assets/PNG/Power-ups/powerupGreen.png').convert_alpha()
        elif type == 'multishot':
            self.image = pygame.image.load('shooter/assets/PNG/Power-ups/powerupRed.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed, color, size, health=1):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # Default shape, but subclasses will override
        pygame.draw.circle(self.image, color, (size[0]//2, size[1]//2), size[0]//2)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed
        self.health = health

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class FastEnemy(Enemy):
    def __init__(self):
        super().__init__(5, RED, (30, 30))
        self.image = pygame.image.load('shooter/assets/PNG/Enemies/enemyBlack1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

class SlowEnemy(Enemy):
    def __init__(self):
        super().__init__(1, ORANGE, (50, 50), 2)
        self.image = pygame.image.load('shooter/assets/PNG/Enemies/enemyBlack2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

class TankEnemy(Enemy):
    def __init__(self):
        super().__init__(1, GRAY, (60, 60), 3)
        self.image = pygame.image.load('shooter/assets/PNG/Enemies/enemyBlack3.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game variables
score = 0
level = 1
spawn_rate = 1  # percentage, reduced
max_enemies = 8  # limit enemies on screen
game_over = False

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Update
        all_sprites.update()

        # Continuous shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet_list = player.shoot()
            for bullet in bullet_list:
                all_sprites.add(bullet)
                bullets.add(bullet)
            if bullet_list:
                laser_sound.play()

        # Spawn enemies
        if random.randint(0, 100) < spawn_rate and len(enemies) < max_enemies:
            enemy_type = random.choice([FastEnemy, SlowEnemy, TankEnemy])
            enemy = enemy_type()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10 * level
                    zap_sound.play()
                    if random.random() < 0.3:
                        powerup_type = random.choice(['health', 'speed', 'multishot'])
                        powerup = PowerUp(enemy.rect.centerx, enemy.rect.centery, powerup_type)
                        all_sprites.add(powerup)
                        powerups.add(powerup)

        player_hits = pygame.sprite.spritecollide(player, enemies, False)
        if player_hits:
            player.health -= 10
            for hit in player_hits:
                hit.kill()
            if player.health <= 0:
                game_over = True
                lose_sound.play()

        # Powerup collisions
        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'health':
                player.health = min(100, player.health + 20)
                shield_up_sound.play()
            elif powerup.type == 'speed':
                player.speed = min(10, player.speed + 1)
                shield_up_sound.play()
            elif powerup.type == 'multishot':
                player.multishot = True
                shield_up_sound.play()

        # Level up
        if score > (level ** 2) * 100:
            level += 1
            spawn_rate = min(5, spawn_rate + 0.5)  # slower increase
            max_enemies = min(15, max_enemies + 2)  # increase max enemies
            # Clear enemies for fresh start
            for enemy in enemies:
                enemy.kill()
            for powerup in powerups:
                powerup.kill()

    else:
        # Game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    all_sprites.empty()
                    bullets.empty()
                    enemies.empty()
                    powerups.empty()
                    player = Player()
                    all_sprites.add(player)
                    score = 0
                    level = 1
                    spawn_rate = 1
                    max_enemies = 8
                    game_over = False
                elif event.key == pygame.K_q:
                    running = False

    # Draw
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # Draw UI
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 10))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 50))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 90))

    if game_over:
        font_large = pygame.font.Font(None, 74)
        game_over_text = font_large.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        restart_text = font.render("Press R to Restart, Q to Quit", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

    pygame.display.flip()

# Save high score
if score > high_score:
    save_high_score(score)

pygame.quit()
sys.exit()