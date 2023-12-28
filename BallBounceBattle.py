import pygame 
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ trò chơi
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Bounce Battle")

# Màu sắc
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Kích thước thanh chuyền bóng
thanh_chuyen_bong_width = 15
thanh_chuyen_bong_height = 100

# Tọa độ ban đầu của các thanh chuyền bóng
player_x = width - 50 - thanh_chuyen_bong_width
player_y = height // 2 - thanh_chuyen_bong_height // 2
opp_x = 50
opp_y = height // 2 - thanh_chuyen_bong_height // 2

# Vận tốc di chuyển của các thanh chuyền bóng
player_speed = 7
opp_speed = 5

# Vận tốc di chuyển của bóng
ball_speed_x = random.choice([-3, 3])
ball_speed_y = random.choice([-3, 3])

# Tọa độ ban đầu của bóng
ball_x = width // 2
ball_y = height // 2
ball_radius = 10

# Điểm số
player_score = 0
opp_score = 0

# Font chữ
font = pygame.font.SysFont("Arial", 30)

# Chướng ngại vật
obstacles = []

# Thêm chướng ngại vật vào danh sách
def add_obstacle():
    obstacle_width = 10
    obstacle_height = random.randint(50, 100)
    obstacle_x = width // 2 - obstacle_width // 2
    obstacle_y = random.randint(0, height - obstacle_height)
    obstacle_speed = 1
    obstacle_direction = random.choice(['up', 'down', 'left', 'right'])
    obstacles.append({
        'width': obstacle_width,
        'height': obstacle_height,
        'x': obstacle_x,
        'y': obstacle_y,
        'speed': obstacle_speed,
        'direction': obstacle_direction
    })

# Reset lại quả bóng
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = width // 2
    ball_y = height // 2
    ball_speed_x = random.choice([-3, 3])
    ball_speed_y = random.choice([-3, 3])

# Reset lại trò chơi
def reset_game():
    global player_score, opp_score
    player_score = 0
    opp_score = 0
    reset_ball()
    obstacles.clear()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Thông báo xin chào và hướng dẫn
screen.fill(BLACK)
draw_text(screen, "Welcome to My Mini Game!!!", 36, width // 2, height // 2 - 50)
draw_text(screen, "Press ENTER to start game...", 24, width // 2, height // 2 + 100)
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

# Thêm các chướng ngại vật ban đầu
for i in range(10):
    add_obstacle()

# Vòng lặp trò chơi
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    # Di chuyển các thanh chuyền bóng
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - thanh_chuyen_bong_height:
        player_y += player_speed
    if opp_y + thanh_chuyen_bong_height // 2 < ball_y:
        opp_y += opp_speed
    if opp_y + thanh_chuyen_bong_height // 2 > ball_y:
        opp_y -= opp_speed

    # Di chuyển bóng
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Kiểm tra va chạm với thành trên và dưới
    if ball_y <= 0 or ball_y >= height - ball_radius:
        ball_speed_y *= -1

    # Kiểm tra va chạm với thanh chuyền bóng
    if (player_x <= ball_x <= player_x + thanh_chuyen_bong_width and
            player_y + thanh_chuyen_bong_height >= ball_y >= player_y) or \
            (opp_x <= ball_x <= opp_x + thanh_chuyen_bong_width and
             opp_y + thanh_chuyen_bong_height >= ball_y >= opp_y):
        ball_speed_x *= -1

    # Kiểm tra va chạm với chướng ngại vật
    for obstacle in obstacles:
        if (obstacle['x'] <= ball_x <= obstacle['x'] + obstacle['width'] and
                obstacle['y'] + obstacle['height'] >= ball_y >= obstacle['y']) or \
                (obstacle['x'] + obstacle['width'] >= ball_x >= obstacle['x'] and
                 obstacle['y'] + obstacle['height'] >= ball_y >= obstacle['y']):
            ball_speed_x *= -1
            ball_speed_y *= -1

    # Kiểm tra bóng chạm biên trái và biên phải
    if ball_x <= 0:
        player_score += 1
        reset_ball()
    elif ball_x >= width - ball_radius:
        opp_score += 1
        reset_ball()

    # Kiểm tra thua cuộc
    if player_score == 1 or opp_score == 5:
        game_over = True

    # Di chuyển các chướng ngại vật
    for obstacle in obstacles:
        if obstacle['direction'] == 'up':
            obstacle['y'] -= obstacle['speed']
            if obstacle['y'] <= 0:
                obstacle['direction'] = random.choice(['down', 'left', 'right'])

        elif obstacle['direction'] == 'down':
            obstacle['y'] += obstacle['speed']
            if obstacle['y'] + obstacle['height'] >= height:
                obstacle['direction'] = random.choice(['up', 'left', 'right'])

        elif obstacle['direction'] == 'left':
            obstacle['x'] -= obstacle['speed']
            if obstacle['x'] <= 0:
                obstacle['direction'] = random.choice(['up', 'down', 'right'])

        elif obstacle['direction'] == 'right':
            obstacle['x'] += obstacle['speed']
            if obstacle['x'] + obstacle['width'] >= width:
                obstacle['direction'] = random.choice(['up', 'down', 'left'])

    # Vẽ trạng thái trò chơi
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, thanh_chuyen_bong_width, thanh_chuyen_bong_height))
    pygame.draw.rect(screen, RED, (opp_x, opp_y, thanh_chuyen_bong_width, thanh_chuyen_bong_height))
    pygame.draw.circle(screen, GREEN, (ball_x, ball_y), ball_radius)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))

    # Vẽ điểm số
    player_text = font.render("Player: " + str(opp_score), True, RED)
    opp_text = font.render("Opponent: " + str(player_score), True, BLUE)
    screen.blit(player_text, (10, 10))
    screen.blit(opp_text, (width - opp_text.get_width() - 10, 10))

    # Thêm chướng ngại vật mới
    current_time = pygame.time.get_ticks()
    if current_time % 1000 == 0:
        add_obstacle()

    # Hiển thị thông báo điểm số khi kết thúc trò chơi
    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "Game Over! Your Score: {}".format(player_score), 36, width // 2, height // 2 - 50)
        draw_text(screen, "Press [X] exit to game...", 24, width // 2, height // 2 + 100)
        
    pygame.display.flip()
    clock.tick(120)

# Kết thúc Pygame
pygame.quit()