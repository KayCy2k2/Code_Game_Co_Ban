import pygame
import random

class MazeGame:
    def __init__(self):
        # Khai báo kích thước màn hình
        self.WIDTH, self.HEIGHT = 800, 600

        # Khởi tạo màn hình
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Decoding the maze")

        # Màu sắc
        self.WHITE = (0, 0, 0)
        self.BLACK = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # Kích thước cell trong mê cung
        self.CELL_SIZE = 20

        # Số lượng cell trên mỗi hàng và cột
        self.NUM_COLS = self.WIDTH // (self.CELL_SIZE - 1)
        self.NUM_ROWS = self.HEIGHT // (self.CELL_SIZE - 1)

        # Ma trận lưu trạng thái của các cell
        self.grid = [[0] * self.NUM_COLS for _ in range(self.NUM_ROWS)]

        # Thời gian cập nhật mê cung (trong millisecond)
        self.UPDATE_TIME = 5000

        # Vị trí người chơi ban đầu
        self.player_pos = [self.NUM_ROWS // 2, self.NUM_COLS // 2]
        
        # Vị trí các ghost ban đầu
        self.ghost_pos = []
        for _ in range(5):
            row = random.randint(0, self.NUM_ROWS - 1)
            col = random.randint(0, self.NUM_COLS - 1)
            self.ghost_pos.append([row, col])

        # Đếm thời gian đã trôi qua (trong millisecond)
        self.elapsed_time = 0

        # Khởi tạo mê cung ban đầu
        self.create_maze(0, 0)

    # Hàm vẽ mê cung và người chơi
    def draw_maze(self):
        # Xóa màn hình
        self.screen.fill(self.WHITE)

        # Vẽ các cell đã được kết nối
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE

                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, self.BLACK, (x, y, self.CELL_SIZE, self.CELL_SIZE))

        # Vẽ người chơi
        player_x = self.player_pos[1] * self.CELL_SIZE
        player_y = self.player_pos[0] * self.CELL_SIZE
        pygame.draw.rect(self.screen, self.RED, (player_x, player_y, self.CELL_SIZE, self.CELL_SIZE))
        
        # Vẽ ghost
        for ghost in self.ghost_pos:
            ghost_x = ghost[1] * self.CELL_SIZE
            ghost_y = ghost[0] * self.CELL_SIZE
            pygame.draw.rect(self.screen, self.BLUE, (ghost_x, ghost_y, self.CELL_SIZE, self.CELL_SIZE))

        # Cập nhật màn hình
        pygame.display.flip()

    # Hàm kiểm tra xem một cell có hợp lệ hay không
    def is_valid_cell(self, row, col):
        return row >= 0 and row < self.NUM_ROWS and col >= 0 and col < self.NUM_COLS and self.grid[row][col] == 0

    # Hàm kiểm tra xem một cell đã được ghé thăm hay chưa
    def is_visited(self, row, col):
        return self.grid[row][col] == 1

    # Hàm tạo mê cung bằng thuật toán Recursive Backtracking
    def create_maze(self, row, col):
        self.grid[row][col] = 1

        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for direction in directions:
            next_row = row + direction[0] 
            next_col = col + direction[1] 

            if self.is_valid_cell(next_row, next_col) and not self.is_visited(next_row, next_col):
                self.grid[next_row][next_col] = 1
                self.grid[row + direction[0] // 2][col + direction[1] // 2] = 1
                self.create_maze(next_row, next_col)

    def draw_text(self, text, size, x, y):
        self.GREEN = (0, 255, 0)
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, self.GREEN)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Phương thức chạy trò chơi
    def run_game(self):
        # Hiển thị thông báo xin chào và hướng dẫn
        self.screen.fill(self.BLACK)
        self.draw_text("Welcome to My Mini Game!!!", 36, self.WIDTH // 2, self.HEIGHT // 2 - 50)
        self.draw_text("Press ENTER to start game...", 18, self.WIDTH // 2, self.HEIGHT // 2 + 100)
        pygame.display.flip()

        start = False
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start = True
                        break  # Thêm break để thoát khỏi vòng lặp
                    elif event.key == pygame.K_SPACE:
                        pygame.quit()
                
        # Vòng lặp chính
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # Kiểm tra sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Di chuyển lên
                        new_row = self.player_pos[0] - 1
                        new_col = self.player_pos[1]
                        if self.is_valid_cell(new_row, new_col):
                            self.player_pos = [new_row, new_col]
                    elif event.key == pygame.K_DOWN:
                        # Di chuyển xuống
                        new_row = self.player_pos[0] + 1
                        new_col = self.player_pos[1]
                        if self.is_valid_cell(new_row, new_col):
                            self.player_pos = [new_row, new_col]
                    elif event.key == pygame.K_LEFT:
                        # Di chuyển sang trái
                        new_row = self.player_pos[0]
                        new_col = self.player_pos[1] - 1
                        if self.is_valid_cell(new_row, new_col):
                            self.player_pos = [new_row, new_col]
                    elif event.key == pygame.K_RIGHT:
                        # Di chuyển sang phải
                        new_row = self.player_pos[0]
                        new_col = self.player_pos[1] + 1
                        if self.is_valid_cell(new_row, new_col):
                            self.player_pos = [new_row, new_col]

            # Di chuyển ghost
            for i in range(len(self.ghost_pos)):
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                random.shuffle(directions)
                for direction in directions:
                    next_row = self.ghost_pos[i][0] + direction[0]
                    next_col = self.ghost_pos[i][1] + direction[1]
                    if self.is_valid_cell(next_row, next_col):
                        self.ghost_pos[i] = [next_row, next_col]
                        break

            # Cập nhật mê cung mới nếu đã trôi qua UPDATE_TIME
            self.elapsed_time += clock.tick()
            if self.elapsed_time >= self.UPDATE_TIME:
                self.grid = [[0] * self.NUM_COLS for _ in range(self.NUM_ROWS)]
                self.create_maze(0, 0)
                self.elapsed_time = 0

            # Kiểm tra xem người chơi đã chạm biên màn hình hay chưa
            if self.player_pos[0] == 0 or self.player_pos[0] == self.NUM_ROWS - 2 or self.player_pos[1] == 0 or self.player_pos[1] == self.NUM_COLS - 3:
                running = False                    

            # Kiểm tra va chạm giữa người chơi và ghost
            if self.player_pos in self.ghost_pos:
                running = False
                        
            # Vẽ mê cung và người chơi
            self.draw_maze()

        self.screen.fill(self.BLACK)
        self.draw_text("Game Over!", 40, self.WIDTH // 2, self.HEIGHT // 2 - 50)
        self.draw_text("Press ESC to quit...", 18, self.WIDTH // 2, self.HEIGHT // 2 + 50)
        pygame.display.flip()

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        break  # Thêm break để thoát khỏi vòng lặp

            clock.tick(90)

if __name__ == "__main__":
    game = MazeGame()
    game.run_game()
