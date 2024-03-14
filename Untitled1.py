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
        self.health = 1000 #máu

    def check_collision(self):
        if pygame.sprite.spritecollide(self, bosses, False) or pygame.sprite.spritecollide(self, boss_bullets, True):
            # Kiểm tra va chạm với đạn boss
                # Giảm lượng máu khi bị bắn trúng
                self.health -= 10
                
                # Kiểm tra game over
                if self.health <= 0:
                    return True
        return False

    def update(self):
        keys = pygame.key.get_pressed()
        offset = {K_UP: (0, -self.speed), K_DOWN: (0, self.speed), K_LEFT: (-self.speed, 0), K_RIGHT: (self.speed, 0)}
        for key, move in offset.items():
            if keys[key]:
                self.rect.move_ip(*move)
                self.direction = {K_UP: "up", K_DOWN: "down", K_LEFT: "left", K_RIGHT: "right"}[key]
        
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        # Use dictionary mapping for direction-specific bullet creation
        bullet_offsets = {"up": (0, -1),"down": (0, 1),"left": (-1, 0),"right": (1, 0)}
        if self.direction in bullet_offsets:
            dx, dy = bullet_offsets[self.direction]
            bullet = Bullet(self.rect.centerx + dx, self.rect.centery + dy, dx, dy)
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

class Boss(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Boss, self).__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 10))
        self.speed = 3
        self.shoot_distance = 500
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.player = player
        self.is_idle = True
        self.alive = True  # Thêm biến trạng thái alive và khởi tạo là True
        self.min_distance = 30  # Ví dụ: khoảng cách tối thiểu là 100px

    def update(self):
        if self.is_idle:  # Nếu boss đang trong trạng thái đứng im
            if pygame.time.get_ticks() - self.last_shot > 2000:  # Đợi trong 1 giây
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
        epsilon = 0.001
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.rect.x += (dx / (distance + epsilon)) * self.speed
            self.rect.y += (dy / (distance + epsilon)) * self.speed
        
        for other_boss in bosses:
            if other_boss != self:
                dx = other_boss.rect.centerx - self.rect.centerx
                dy = other_boss.rect.centery - self.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < self.min_distance:
                    # Di chuyển theo hướng ngược lại boss khác
                    self.rect.x += (-dx / (distance + epsilon)) * self.speed
                    self.rect.y += (-dy / (distance + epsilon)) * self.speed
                    break

    def check_player_distance(self):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            epsilon = 0.001
            if distance <= self.shoot_distance:
                bullet = Bullet(self.rect.centerx, self.rect.centery, dx / (distance + epsilon), dy / (distance + epsilon))
                boss_bullets.add(bullet)
                self.last_shot = pygame.time.get_ticks()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, player):
    # Tính toán vị trí và kích thước thanh máu
    bar_width = 200
    bar_height = 10
    x = 550
    y = 5

    # Vẽ thanh nền
    pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height))

    # Vẽ thanh máu
    health_width = int(bar_width * (player.health / 1000))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, health_width, bar_height))

    # Hiển thị % thanh máu
    text = f"{player.health}%"
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + bar_width + 10, y))

def draw_boss_count(surface, num_bosses_dead, total_bosses):
    # Vị trí và kích thước text
    x = 2
    y = 2
    font = pygame.font.SysFont(None, 24)

    # Hiển thị số lượng boss đã chết
    text = f"Boss die: {num_bosses_dead}"
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

    # Hiển thị số lượng boss còn lại
    text = f"Boss alive: {total_bosses - num_bosses_dead}"
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y + 20))

pygame.init()

WIDTH, HEIGHT = 1200, 800
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

boss_bullets = pygame.sprite.Group()  # Tạo nhóm cho các viên đạn của boss

bosses = pygame.sprite.Group()
for _ in range(30):  # Thêm 3 boss
    boss = Boss(player)
    bosses.add(boss)

all_sprites = pygame.sprite.Group()
all_sprites.add(player, *bosses, boss_bullets)  # Thêm nhóm đạn của boss vào all_sprites

num_bosses_dead = 0
total_bosses = 30

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
                num_bosses_dead += 1
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
    # Hiển thị thanh máu
    draw_health_bar(screen, player)
    # Hiển thị thông tin boss
    draw_boss_count(screen, num_bosses_dead, total_bosses)


    # Kiểm tra xem tất cả boss đã bị tiêu diệt hay chưa
    if not bosses:
        # Hiển thị thông báo chiến thắng
        screen.fill((0, 0, 0))
        draw_text(screen, "You Win!", 48, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)  # Đợi 2 giây trước khi đóng cửa sổ
        running = False
    elif player.check_collision():
        running = False
        screen.fill((0, 0, 0))
        draw_text(screen, "Game Over!", 48, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)  # Đợi 2 giây trước khi đóng cửa sổ
        
    pygame.display.flip()
    clock.tick(90)

pygame.quit()