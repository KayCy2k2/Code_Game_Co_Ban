import pygame

# Định nghĩa các màu sắc
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Định nghĩa kích thước màn hình
WIDTH = 600
HEIGHT = 600

# Khởi tạo pygame và cửa sổ game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro 4.0")

class TicTacToe:
    def __init__(self, width, height, fps, bg_color, line_color, x_color, o_color):
        self.width = width
        self.height = height
        self.fps = fps
        self.bg_color = bg_color
        self.line_color = line_color
        self.x_color = x_color
        self.o_color = o_color
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        self.board = None
        self.player_positions = None
        self.history = None
        self.current_player = None

    def create_board(self, size):
        return [[' ' for _ in range(size)] for _ in range(size)]

    def draw_board(self):
        self.screen.fill(self.bg_color)
        square_size = self.width // len(self.board)
        
        for i in range(1, len(self.board)):
            pygame.draw.line(self.screen, self.line_color, (0, i * square_size), (self.width, i * square_size), 2)
            pygame.draw.line(self.screen, self.line_color, (i * square_size, 0), (i * square_size, self.height), 2)
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                x = col * square_size
                y = row * square_size
                
                if self.board[row][col] == 'X':
                    x_size = square_size - 15
                    x_offset = (square_size - x_size) // 2
                    pygame.draw.line(
                        self.screen,
                        self.x_color,
                        (x + x_offset, y + x_offset),
                        (x + square_size - x_offset, y + square_size - x_offset),
                        2
                    )
                    pygame.draw.line(
                        self.screen,
                        self.x_color,
                        (x + x_offset, y + square_size - x_offset),
                        (x + square_size - x_offset, y + x_offset),
                        2
                    )
                elif self.board[row][col] == 'O':
                    o_radius = (square_size - 10) // 2
                    pygame.draw.circle(
                        self.screen,
                        self.o_color,
                        (x + square_size // 2, y + square_size // 2),
                        o_radius,
                        2
                    )

    def check_win(self):
        rows = len(self.board)
        cols = len(self.board[0])
        target = 5

        for i in range(rows):
            for j in range(cols - target + 1):
                if all(self.board[i][j+k] == 'X' for k in range(target)):
                    return 'X'
                elif all(self.board[i][j+k] == 'O' for k in range(target)):
                    return 'O'

        for i in range(rows - target + 1):
            for j in range(cols):
                if all(self.board[i+k][j] == 'X' for k in range(target)):
                    return 'X'
                elif all(self.board[i+k][j] == 'O' for k in range(target)):
                    return 'O'

        for i in range(rows - target + 1):
            for j in range(cols - target + 1):
                if all(self.board[i+k][j+k] == 'X' for k in range(target)):
                    return 'X'
                elif all(self.board[i+k][j+k] == 'O' for k in range(target)):
                    return 'O'

        for i in range(rows - target + 1):
            for j in range(target - 1, cols):
                if all(self.board[i+k][j-k] == 'X' for k in range(target)):
                    return 'X'
                elif all(self.board[i+k][j-k] == 'O' for k in range(target)):
                    return 'O'
    
        # Kiểm tra cờ hòa
        if all(self.board[i][j] != ' ' for i in range(rows) for j in range(cols)):
            return 'draw'
    
        return None

    def play_game(self, size):
        self.board = self.create_board(size)
        self.player_positions = {'X': (0, 0), 'O': (0, 0)}
        self.history = []
        self.current_player = 'X'
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    row = mouse_pos[1] // (self.height // size)
                    col = mouse_pos[0] // (self.width // size)

                    if self.board[row][col] != ' ':
                        continue

                    self.board[row][col] = self.current_player
                    self.player_positions[self.current_player] = (row, col)
                    self.history.append((row, col))

                    winner = self.check_win()
                    while winner:
                        if winner == 'draw':
                            # Hiển thị thông báo cờ hòa
                            screen.fill(WHITE)
                            draw_text(screen, "Game Over! It's a draw!", 36, WIDTH // 2, HEIGHT // 2 - 50)
                        else:
                            # Hiển thị thông báo người chiến thắng
                            screen.fill(WHITE)
                            draw_text(screen, "Game Over! You {} Win!".format(winner), 36, WIDTH // 2, HEIGHT // 2 - 50)
                        
                        draw_text(screen, "Press ENTER to start a new game...", 24, WIDTH // 2, HEIGHT // 2 + 100)
                        draw_text(screen, "Press SPACE to exit game ...", 24, WIDTH // 2, HEIGHT // 2 + 120)
                        pygame.display.flip()

                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    pygame.quit()
                                    return
                                elif event.key == pygame.K_RETURN:
                                    self.board = self.create_board(size)
                                    self.player_positions = {'X': (0, 0), 'O': (0, 0)}
                                    self.history = []
                                    self.current_player = 'X'
                                    winner = None  # Reset biến winner để bắt đầu trò chơi mới
                                    
                    self.current_player = 'O' if self.current_player == 'X' else 'X'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.board = self.create_board(size)
                        self.player_positions = {'X': (0, 0), 'O': (0, 0)}
                        self.history = []
                        self.current_player = 'X'

                    if event.key == pygame.K_r:
                        if len(self.history) > 0:
                            last_move = self.history[-1]
                            row, col = last_move
                            self.board[row][col] = ' '
                            self.player_positions[self.current_player] = last_move
                            self.history.pop()

                    if event.key == pygame.K_u:
                        if len(self.history) > 1:
                            self.history.pop()
                            last_move = self.history[-1]
                            row, col = last_move
                            self.board[row][col] = ' '
                            self.player_positions[self.current_player] = last_move
                            self.current_player = 'O' if self.current_player == 'X' else 'X'

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.fps)

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    FPS = 90
    BG_COLOR = (255, 255, 255)
    LINE_COLOR = (0, 0, 0)
    X_COLOR = (255, 0, 0)
    O_COLOR = (0, 0, 255)

    size_input = 20 #Nhập kích thước bàn cờ
    try:
        board_size = int(size_input)
        if board_size < 3:
            print("Kích thước bàn cờ phải lớn hơn hoặc bằng 3.")
        else:
            game = TicTacToe(WIDTH, HEIGHT, FPS, BG_COLOR, LINE_COLOR, X_COLOR, O_COLOR)
            game.play_game(board_size)
    except ValueError:
        print("Vui lòng nhập một số nguyên.")
    
    # Thông báo xin chào và hướng dẫn
screen.fill(WHITE)
draw_text(screen, "Welcome to My Mini Game!!!", 36, WIDTH // 2, HEIGHT // 2 - 50)
draw_text(screen, "- Game Two Player -", 30, WIDTH // 2, HEIGHT // 2)
draw_text(screen, "Press ENTER to start game...", 24, WIDTH // 2, HEIGHT // 2 + 100)

pygame.display.flip()

start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = True
                break  # Thêm break để thoát khỏi vòng lặp
 
if __name__ == "__main__":
    main()
