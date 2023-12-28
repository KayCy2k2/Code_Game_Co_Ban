import pygame
import random

# Khởi tạo các hằng số
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
CENTIPEDE_SPEED = 2
BULLET_SPEED = 8

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Lớp con cho đối tượng người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# Lớp con cho đối tượng giun đất (centipede)
class Centipede(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey(pygame.Color("BLACK"))  # Đặt màu nền trong suốt
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = CENTIPEDE_SPEED

        points = [(0, 0), (12, 25), (25, 0)]  # Tọa độ các điểm để vẽ tam giác
        pygame.draw.polygon(self.image, pygame.Color("RED"), points)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

# Lớp con cho đối tượng đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.set_colorkey(pygame.Color("BLACK"))  # Đặt màu nền trong suốt
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed_y = -BULLET_SPEED
        self.radius = 6

        pygame.draw.circle(self.image, pygame.Color("WHITE"), (self.radius, self.radius), self.radius)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Khởi tạo font chữ
font_name = pygame.font.match_font("arial")

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Khởi tạo Pygame và cửa sổ trò chơi
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600

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

all_sprites = pygame.sprite.Group()
centipedes = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(10):
    centipede = Centipede()
    all_sprites.add(centipede)
    centipedes.add(centipede)

running = True
game_over = False
score = 0

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.centery)
                all_sprites.add(bullet)
                bullets.add(bullet)

            if event.key == pygame.K_ESCAPE:
                if game_over:
                    running = False

            if event.key == pygame.K_RETURN:
                if game_over:
                    # Reset game
                    all_sprites.empty()
                    centipedes.empty()
                    bullets.empty()

                    player = Player()
                    all_sprites.add(player)

                    for _ in range(10):
                        centipede = Centipede()
                        all_sprites.add(centipede)
                        centipedes.add(centipede)

                    score = 0
                    game_over = False

    all_sprites.update()

    # Kiểm tra va chạm giữa người chơi và giun đất
    hits = pygame.sprite.spritecollide(player, centipedes, False)
    if hits:
        game_over = True

    # Kiểm tra va chạm giữa đạn và giun đất
    bullet_hits = pygame.sprite.groupcollide(bullets, centipedes, True, True)
    for hit in bullet_hits:
        centipede = Centipede()
        all_sprites.add(centipede)
        centipedes.add(centipede)
        score += 5

    screen.fill(BLACK)
    all_sprites.draw(screen)

    draw_text(screen, "Score: {}".format(score), 30, WIDTH // 2, 10)

    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "Game Over! Score : {}".format(score), 36, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, "Press ENTER to start game...", 24, WIDTH // 2, HEIGHT // 2 + 100)
        draw_text(screen, "Press ESC to exit game...", 24, WIDTH // 2, HEIGHT // 2 + 130)
        pygame.display.flip()
        #pygame.time.wait(2000)  # Đợi 2 giây trước khi reset
    else:
        pygame.display.flip()

pygame.quit()


