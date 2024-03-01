import pygame
from pygame.locals import *
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 7
        self.direction = "up"  # Hướng ban đầu là "up"

    def check_collision(self):
        if pygame.sprite.spritecollide(self, bosses, False) or pygame.sprite.spritecollide(self, boss_bullets, True):
            return True
        return False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
            self.direction = "up"
        if keys[K_DOWN]:
            self.rect.y += self.speed
            self.direction = "down"
        if keys[K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"

        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        if self.direction == "up":
            bullet = Bullet(self.rect.centerx, self.rect.top, 0, -1)
        elif self.direction == "down":
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 0, 1)
        elif self.direction == "left":
            bullet = Bullet(self.rect.left, self.rect.centery, -1, 0)
        elif self.direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 1, 0)
        
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.dx = dx  # Hướng di chuyển theo trục x
        self.dy = dy  # Hướng di chuyển theo trục y

    def update(self):
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy
        
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

boss_bullets = pygame.sprite.Group()  # Tạo nhóm cho các viên đạn của boss

class Boss(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Boss, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10))
        self.speed = 1
        self.shoot_distance = 250
        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks()
        self.player = player
        self.is_idle = True
        self.alive = True  # Thêm biến trạng thái alive và khởi tạo là True

    def update(self):
        if self.is_idle:  # Nếu boss đang trong trạng thái đứng im
            if pygame.time.get_ticks() - self.last_shot > 1000:  # Đợi trong 1 giây
                self.is_idle = False  # Chuyển sang trạng thái truy đuổi
                self.last_shot = pygame.time.get_ticks()  # Cập nhật thời điểm bắn đạn cuối cùng
        else:
            self.move_towards_player()
            self.check_player_distance()
        self.rect.clamp_ip(screen.get_rect())
        
        # Cập nhật trạng thái "alive" khi boss bị tiêu diệt
        if not self.alive:
            self.kill()  # Xóa boss khỏi nhóm sprites

    def move_towards_player(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed

    def check_player_distance(self):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= self.shoot_distance:
                bullet = Bullet(self.rect.centerx, self.rect.centery, dx / distance, dy / distance)
                boss_bullets.add(bullet)
                self.last_shot = pygame.time.get_ticks()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle")
clock = pygame.time.Clock()

# Định nghĩa các màu sắc
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

player = Player()
players = pygame.sprite.Group()
players.add(player)
bullets = pygame.sprite.Group()

bosses = pygame.sprite.Group()
for _ in range(10):  # Thêm 3 boss
    boss = Boss(player)
    bosses.add(boss)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, *bosses, boss_bullets)  # Thêm nhóm đạn của boss vào all_sprites

# Thông báo xin chào và hướng dẫn
screen.fill(BLACK)
draw_text(screen, "Welcome to My Mini Game!!!", 36, WIDTH // 2, HEIGHT // 2 - 50)
draw_text(screen, "Press ENTER to start game...", 24, WIDTH // 2, HEIGHT // 2 + 100)
pygame.display.flip()

start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = True
                break  # Thêm break để thoát khỏi vòng lặp
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.shoot()

    all_sprites.update()
    bullets.update()
    boss_bullets.update()

    for bullet in pygame.sprite.groupcollide(bullets, bosses, True, False):
        for boss in bosses:
            if boss.rect.colliderect(bullet.rect) and boss.alive:  # Kiểm tra va chạm và trạng thái sống của boss
                boss.alive = False  # Đánh dấu boss đã chết
                break

    screen.fill((0, 0, 0))
    # Vẽ player, boss và đạn của boss
    for sprite in all_sprites:
        if isinstance(sprite, Boss) and not sprite.alive: # Chỉ vẽ boss còn sống  
            continue
        screen.blit(sprite.image, sprite.rect)
        
    # Vẽ đạn của người chơi và đạn của boss
    bullets.draw(screen)
    boss_bullets.draw(screen)

    if player.check_collision():
        running = False
        screen.fill((0, 0, 0))
        draw_text(screen, "Game Over", 48, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)  # Đợi 2 giây trước khi đóng cửa sổ
        
    pygame.display.flip()
    clock.tick(90)

pygame.quit()
