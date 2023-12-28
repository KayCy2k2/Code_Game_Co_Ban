import pygame
import random
import math

# Định nghĩa các màu sắc
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Định nghĩa kích thước màn hình
WIDTH = 800
HEIGHT = 600

# Định nghĩa tốc độ khung hình (FPS)
FPS = 90

# Khởi tạo pygame và cửa sổ game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

clock = pygame.time.Clock()

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed = 5 # tăng/giảm tốc độ pacman di chuyển
        self.direction = "right"
        self.paused = False

    def update(self):
        if not self.paused:
            if self.direction == "right":
                self.rect.x += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed

            # Kiểm tra va chạm với biên màn hình
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

    def change_direction(self, direction):
        self.direction = direction

    def toggle_pause(self):
        self.paused = not self.paused

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ghost(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
        self.speed = 3 # tăng/giảm tốc độ ghost di chuyển
        self.target = target

    def update(self):
        target_x = self.target.rect.centerx
        target_y = self.target.rect.centery

        if not self.target.paused:
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > 40: # hack khoảng cách giữa ghost và pacman
                if self.rect.x < target_x:
                    self.rect.x += self.speed
                elif self.rect.x > target_x:
                    self.rect.x -= self.speed

                if self.rect.y < target_y:
                    self.rect.y += self.speed
                elif self.rect.y > target_y:
                    self.rect.y -= self.speed

        self.check_collision()

    def check_collision(self):
        for ghost in ghosts:
            if ghost != self and pygame.sprite.collide_rect(self, ghost):
                self.avoid_collision()
                break

    def avoid_collision(self):
        directions = ["right", "left", "up", "down"]

        for direction in directions:
            if direction == "right":
                self.rect.x += self.speed
            elif direction == "left":
                self.rect.x -= self.speed
            elif direction == "up":
                self.rect.y -= self.speed
            elif direction == "down":
                self.rect.y += self.speed

            # Kiểm tra va chạm với biên màn hình
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

            if not pygame.sprite.spritecollide(self, ghosts, False):
                break

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

pacman = None  # Biến pacman được khởi tạo trước vì nó sẽ được sử dụng ở nhiều hàm

def create_sprites():
    global pacman  # Sử dụng biến toàn cục pacman

    all_sprites = pygame.sprite.Group()
    dots = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    pacman = Pacman()
    all_sprites.add(pacman)

    for _ in range(100): # thêm/bớt số lượng dot
        dot = Dot(random.randrange(0, WIDTH - 10), random.randrange(0, HEIGHT - 10))
        dots.add(dot)
        all_sprites.add(dot)

    for _ in range(3): # thêm/bớt số lượng ghost
        ghost = Ghost(pacman)
        ghosts.add(ghost)
        all_sprites.add(ghost)

    return all_sprites, dots, ghosts

def reset_game():
    global score, game_over, all_sprites, dots, ghosts

    game_over = False
    score = 0

    all_sprites.empty()
    dots.empty()
    ghosts.empty()

    all_sprites, dots, ghosts = create_sprites()

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

# Tạo các sprite
all_sprites, dots, ghosts = create_sprites()

score = 0 # Khởi tạo điểm số khi bắt đầu

# Khởi tạo game
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.change_direction("left")
            elif event.key == pygame.K_RIGHT:
                pacman.change_direction("right")
            elif event.key == pygame.K_UP:
                pacman.change_direction("up")
            elif event.key == pygame.K_DOWN:
                pacman.change_direction("down")
            elif event.key == pygame.K_p:
                pacman.toggle_pause()
            elif event.key == pygame.K_SPACE and game_over:  # Thêm xử lý cho phím Space
                reset_game()

    if not pacman.paused and not game_over:
        all_sprites.update()

        collisions = pygame.sprite.spritecollide(pacman, dots, True)
        score += len(collisions)

        if len(dots) == 0:
            game_over = True

        ghost_collisions = pygame.sprite.spritecollide(pacman, ghosts, False)
        if ghost_collisions:
            game_over = True

    screen.fill(BLACK)
    all_sprites.draw(screen)

    draw_text(screen, "Score: {}".format(score), 30, WIDTH // 2, 10)

    # Hiển thị thông báo điểm số khi kết thúc trò chơi
    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "Game Over! Your Score: {}".format(score), 36, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, "Press SPACE to play again...", 24, WIDTH // 2, HEIGHT // 2 + 100)
    pygame.display.flip()

pygame.quit()