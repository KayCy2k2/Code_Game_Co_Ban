import pygame
import random

# Khai báo màu sắc
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
 
# Khởi tạo Pygame và cửa sổ trò chơi
pygame.init()
WIDTH = 800
HEIGHT = 600
Fast = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Khởi tạo font chữ
font_name = pygame.font.match_font("arial")

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

class Snake:
    def __init__(self):
        self.size = 3
        self.segments = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self):
        x, y = self.segments[0]
        if self.direction == "UP":
            y -= 20
        elif self.direction == "DOWN":
            y += 20
        elif self.direction == "LEFT":
            x -= 20
        elif self.direction == "RIGHT":
            x += 20
        self.segments.insert(0, (x, y))
        if len(self.segments) > self.size:
            self.segments.pop()

    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = direction
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = direction
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = direction
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = direction

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 20, 20))

    def check_collision(self):
        head = self.segments[0]
        if (
            head[0] < 0
            or head[0] >= WIDTH
            or head[1] < 0
            or head[1] >= HEIGHT
            or head in self.segments[1:]
        ):
            return True
        return False

    def check_eat_food(self, food):
        head = self.segments[0]
        if head == food.position:
            self.size += 1
            return True
        return False

class Food:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], 20, 20))
 
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
            
# Khởi tạo Rắn và Thức ăn
snake = Snake()
food = Food()
high_score = 0

running = True
game_over = False

while running:
    clock.tick(Fast)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_RETURN:
                game_over = False
                snake = Snake()
                food = Food()
            elif not game_over:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
            elif event.key == pygame.K_SPACE and game_over:
                running = False

    if not game_over:
        snake.move()

        if snake.check_collision():
            game_over = True
            if snake.size > high_score:
                high_score = snake.size

        if snake.check_eat_food(food):
            food = Food()
            
    screen.fill(BLACK)
    snake.draw()
    food.draw()
    
    draw_text(screen, "Score: {}".format(snake.size - 3), 30, WIDTH // 2, 10)

    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "Game Over! Your Score: {}".format(snake.size - 3), 36, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, "Press ENTER to play again...", 24, WIDTH // 2, HEIGHT // 2 + 100)
        draw_text(screen, "Press SPACE to exit game...", 24, WIDTH // 2, HEIGHT // 2 + 130)
    pygame.display.flip()

pygame.quit()