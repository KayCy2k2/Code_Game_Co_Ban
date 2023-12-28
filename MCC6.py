import pygame
import random

# Khai báo kích thước màn hình
WIDTH, HEIGHT = 800, 600

# Khởi tạo màn hình
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mê cung")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Kích thước cell trong mê cung
CELL_SIZE = 20

# Số lượng cell trên mỗi hàng và cột
NUM_COLS = WIDTH // CELL_SIZE
NUM_ROWS = HEIGHT // CELL_SIZE

# Ma trận lưu trạng thái của các cell
grid = [[0] * NUM_COLS for _ in range(NUM_ROWS)]

# Thời gian cập nhật mê cung (trong millisecond)
UPDATE_TIME = 9000000

# Vị trí người chơi ban đầu
player_pos = [NUM_ROWS // 2, NUM_COLS // 2]

# Vẽ mê cung
def draw_maze(player_pos):
    # Xóa màn hình
    screen.fill(WHITE)

    # Vẽ các cell đã được kết nối
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if grid[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

    # Vẽ người chơi
    player_x = player_pos[1] * CELL_SIZE
    player_y = player_pos[0] * CELL_SIZE
    pygame.draw.rect(screen, RED, (player_x, player_y, CELL_SIZE, CELL_SIZE))

    # Cập nhật màn hình
    pygame.display.flip()

# Hàm kiểm tra xem một cell có hợp lệ hay không
def is_valid_cell(row, col):
    return row >= 0 and row < NUM_ROWS and col >= 0 and col < NUM_COLS and grid[row][col] == 0

# Hàm kiểm tra xem một cell đã được ghé thăm hay chưa
def is_visited(row, col):
    return grid[row][col] == 1

# Hàm kiểm tra xem một cell có hàng xóm chưa được ghé thăm hay không
def has_unvisited_neighbor(row, col):
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    for direction in directions:
        next_row = row + direction[0]
        next_col = col + direction[1]

        if is_valid_cell(next_row, next_col) and not is_visited(next_row, next_col):
            return True

    return False

# Hàm tạo mê cung bằng thuật toán Recursive Backtracking
def create_maze(row, col):
    grid[row][col] = 1

    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    random.shuffle(directions)

    for direction in directions:
        next_row = row + direction[0]
        next_col = col + direction[1]

        if is_valid_cell(next_row, next_col) and not is_visited(next_row, next_col):
            grid[next_row][next_col] = 1
            grid[row + direction[0] // 2][col + direction[1] // 2] = 1
            create_maze(next_row, next_col)

    return

# Thực hiện tạo mê cung ban đầu
grid = [[0] * NUM_COLS for _ in range(NUM_ROWS)]

# Loại bỏ vị trí ban đầu của người chơi khỏi danh sách các cell có thể di chuyển
player_start_row, player_start_col = player_pos
grid[player_start_row][player_start_col] = 1

create_maze(0, 0)

# Đếm thời gian đã trôi qua (trong millisecond)
elapsed_time = 0

# Vòng lặp chính
running = True
while running:
    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Di chuyển lên
                new_row = player_pos[0] - 1
                new_col = player_pos[1]
                if is_valid_cell(new_row, new_col):
                    player_pos = [new_row, new_col]
            elif event.key == pygame.K_DOWN:
                # Di chuyển xuống
                new_row = player_pos[0] + 1
                new_col = player_pos[1]
                if is_valid_cell(new_row, new_col):
                    player_pos = [new_row, new_col]
            elif event.key == pygame.K_LEFT:
                # Di chuyển sang trái
                new_row = player_pos[0]
                new_col = player_pos[1] - 1
                if is_valid_cell(new_row, new_col):
                    player_pos = [new_row, new_col]
            elif event.key == pygame.K_RIGHT:
                # Di chuyển sang phải
                new_row = player_pos[0]
                new_col = player_pos[1] + 1
                if is_valid_cell(new_row, new_col):
                    player_pos = [new_row, new_col]

    # Cập nhật mê cung mới nếu đã trôi qua UPDATE_TIME
    elapsed_time += pygame.time.get_ticks()
    if elapsed_time >= UPDATE_TIME:
        grid = [[0] * NUM_COLS for _ in range(NUM_ROWS)]
        create_maze(0, 0)
        elapsed_time = 0

    # Kiểm tra xem người chơi đã chạm biên màn hình hay chưa
    if player_pos[0] == 0 or player_pos[0] == NUM_ROWS - 1 or player_pos[1] == 0 or player_pos[1] == NUM_COLS - 1:
        running = False

    # Vẽ mê cung và người chơi
    draw_maze(player_pos)

# Đóng cửa sổ Pygame
pygame.quit()