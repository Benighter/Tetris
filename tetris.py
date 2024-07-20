import pygame
import random
import sys

pygame.init()

# Set up the game window
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = HEIGHT
TOP_LEFT_X = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2
TOP_LEFT_Y = HEIGHT - GRID_HEIGHT * GRID_SIZE - 50

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetromino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [0, 0, 1]],  # J shape
    [[1, 1, 1], [1, 0, 0]]  # L shape
]

COLORS = [CYAN, YELLOW, PURPLE, RED, GREEN, BLUE, ORANGE]

# Tetromino class
class Tetromino:
    def __init__(self, x, y, shape, color=None):
        self.x = x
        self.y = y
        self.shape = shape
        if color:
            self.color = color
        else:
            self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        # Create a new rotated shape
        rotated_shape = list(zip(*reversed(self.shape)))
        # Convert tuples to lists
        rotated_shape = [list(row) for row in rotated_shape]
        
        # Save the current shape
        original_shape = self.shape
        self.shape = rotated_shape

        if not is_valid_position(self):
            # If the rotation is not valid, revert to the original shape
            self.shape = original_shape

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_blocks(self):
        blocks = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    x = self.x + j
                    y = self.y + i
                    blocks.append((x, y))
        return blocks

    def draw(self, surface, offset_x=0, offset_y=0):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    x = self.x + j
                    y = self.y + i
                    draw_block(surface, x, y, self.color, offset_x, offset_y)

# Game grid
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Create a new Tetromino
def create_tetromino():
    shape = random.choice(SHAPES)
    return Tetromino(GRID_WIDTH // 2 - len(shape[0]) // 2, 0, shape)

# Draw a block on the game grid
def draw_block(surface, x, y, color, offset_x=0, offset_y=0):
    pygame.draw.rect(surface, color, (TOP_LEFT_X + x * GRID_SIZE + offset_x, TOP_LEFT_Y + y * GRID_SIZE + offset_y, GRID_SIZE - 1, GRID_SIZE - 1))
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X + x * GRID_SIZE + offset_x, TOP_LEFT_Y + y * GRID_SIZE + offset_y, GRID_SIZE - 1, GRID_SIZE - 1), 1)

# Draw the game grid
def draw_grid(surface):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            draw_block(surface, j, i, grid[i][j])

    # Draw grid lines
    for i in range(GRID_WIDTH + 1):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + i * GRID_SIZE, TOP_LEFT_Y),
                         (TOP_LEFT_X + i * GRID_SIZE, TOP_LEFT_Y + GRID_HEIGHT * GRID_SIZE))
    for j in range(GRID_HEIGHT + 1):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + j * GRID_SIZE),
                         (TOP_LEFT_X + GRID_WIDTH * GRID_SIZE, TOP_LEFT_Y + j * GRID_SIZE))

# Check if a position is valid on the game grid
def is_valid_position(tetromino):
    for x, y in tetromino.get_blocks():
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and grid[y][x] != BLACK):
            return False
    return True

# Place a Tetromino on the game grid
def place_tetromino(tetromino):
    for x, y in tetromino.get_blocks():
        if y >= 0:
            grid[y][x] = tetromino.color

# Clear complete lines and move the grid down
def clear_lines():
    full_rows = [i for i in range(GRID_HEIGHT) if all(color != BLACK for color in grid[i])]
    num_cleared = len(full_rows)
    
    for row in reversed(full_rows):
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)
    
    return num_cleared

# Check if the game is over
def is_game_over():
    return any(color != BLACK for color in grid[0])

# Restart the game
def restart_game():
    global grid, score, level, lines_cleared, fall_speed

    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    level = 1
    lines_cleared = 0
    fall_speed = 0.5

# Update the high score
def update_high_score():
    global score, high_score

    if score > high_score:
        high_score = score

# Draw the next block
def draw_next_block(surface, next_shape):
    font = pygame.font.Font(None, 30)
    text = font.render("Next:", True, WHITE)
    surface.blit(text, (WIDTH + 20, 20))

    # Calculate the center position for the next shape
    center_x = WIDTH + SIDEBAR_WIDTH // 2
    center_y = 100

    # Calculate the size of the shape
    shape_height = len(next_shape)
    shape_width = len(next_shape[0])

    # Calculate the offset to center the shape
    offset_x = center_x - (shape_width * GRID_SIZE) // 2
    offset_y = center_y - (shape_height * GRID_SIZE) // 2

    # Draw the shape
    next_color = COLORS[SHAPES.index(next_shape)]
    for i, row in enumerate(next_shape):
        for j, cell in enumerate(row):
            if cell:
                x = offset_x + j * GRID_SIZE
                y = offset_y + i * GRID_SIZE
                pygame.draw.rect(surface, next_color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))
                pygame.draw.rect(surface, WHITE, (x, y, GRID_SIZE - 1, GRID_SIZE - 1), 1)

# Draw the sidebar
def draw_sidebar(surface, score, high_score, level):
    pygame.draw.rect(surface, BLACK, (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
    
    font = pygame.font.Font(None, 30)
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH + 20, 150))
    
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    surface.blit(high_score_text, (WIDTH + 20, 190))
    
    level_text = font.render(f"Level: {level}", True, WHITE)
    surface.blit(level_text, (WIDTH + 20, 230))

# Show the main menu
def show_menu(win):
    menu_font = pygame.font.Font(None, 48)
    title_font = pygame.font.Font(None, 72)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.fill(BLACK)

        title_text = title_font.render("TETRIS", True, WHITE)
        start_text = menu_font.render("Press SPACE to Start", True, WHITE)
        quit_text = menu_font.render("Press Q to Quit", True, WHITE)

        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))

        win.blit(title_text, title_rect)
        win.blit(start_text, start_rect)
        win.blit(quit_text, quit_rect)

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Main game loop
def main():
    global score, high_score, level, lines_cleared, fall_speed

    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    score = 0
    high_score = 0
    level = 1
    lines_cleared = 0
    fall_speed = 0.5

    tetromino = create_tetromino()
    next_shape = random.choice(SHAPES)

    fall_time = 0
    fall_speed = 0.5
    
    game_over = False

    while True:
        show_menu(win)
        restart_game()
        game_over = False

        while not game_over:
            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                tetromino.move(0, 1)
                if not is_valid_position(tetromino):
                    tetromino.move(0, -1)
                    place_tetromino(tetromino)
                    lines_cleared += clear_lines()
                    score += lines_cleared * 100 * level
                    level = lines_cleared // 10 + 1
                    fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                    
                    if is_game_over():
                        game_over = True
                        update_high_score()
                    else:
                        tetromino = Tetromino(GRID_WIDTH // 2 - len(next_shape[0]) // 2, 0, next_shape, COLORS[SHAPES.index(next_shape)])
                        next_shape = random.choice(SHAPES)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetromino.move(-1, 0)
                        if not is_valid_position(tetromino):
                            tetromino.move(1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetromino.move(1, 0)
                        if not is_valid_position(tetromino):
                            tetromino.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetromino.move(0, 1)
                        if not is_valid_position(tetromino):
                            tetromino.move(0, -1)
                    elif event.key == pygame.K_UP:
                        tetromino.rotate()
                    elif event.key == pygame.K_SPACE:
                        while is_valid_position(tetromino):
                            tetromino.move(0, 1)
                        tetromino.move(0, -1)
                        place_tetromino(tetromino)
                        lines_cleared += clear_lines()
                        score += lines_cleared * 100 * level
                        level = lines_cleared // 10 + 1
                        fall_speed = max(0.1, 0.5 - (level - 1) * 0.05)
                        
                        if is_game_over():
                            game_over = True
                            update_high_score()
                        else:
                            tetromino = Tetromino(GRID_WIDTH // 2 - len(next_shape[0]) // 2, 0, next_shape, COLORS[SHAPES.index(next_shape)])
                            next_shape = random.choice(SHAPES)

            win.fill(BLACK)
            draw_grid(win)
            tetromino.draw(win)
            draw_next_block(win, next_shape)
            draw_sidebar(win, score, high_score, level)

            # Draw ghost piece
            ghost = Tetromino(tetromino.x, tetromino.y, tetromino.shape, WHITE)
            while is_valid_position(ghost):
                ghost.move(0, 1)
            ghost.move(0, -1)
            ghost.draw(win)

            pygame.display.update()

        # Game over screen
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        win.blit(game_over_text, game_over_rect)

        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        win.blit(final_score_text, final_score_rect)

        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        win.blit(restart_text, restart_rect)

        quit_text = font.render("Press Q to Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 150))
        win.blit(quit_text, quit_rect)

        pygame.display.update()

        # Wait for user input to restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()