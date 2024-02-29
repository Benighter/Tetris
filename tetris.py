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
TOP_LEFT_X = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2
TOP_LEFT_Y = HEIGHT - GRID_HEIGHT * GRID_SIZE - 50

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 1], [0, 0, 1]],  # J shape
    [[1, 1, 1], [1, 0, 0]]  # L shape
]

# Define Tetromino colors
COLORS = [CYAN, YELLOW, PURPLE, RED, GREEN, BLUE, ORANGE]

# Tetromino class
class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = list(zip(*reversed(self.shape)))

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

    def draw(self, surface):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    x = self.x + j
                    y = self.y + i
                    draw_block(surface, x, y, self.color)

# Game grid
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Create a new Tetromino
def create_tetromino():
    x = GRID_WIDTH // 2 - 1
    y = 0
    shape = random.choice(SHAPES)
    return Tetromino(x, y, shape)

# Draw a block on the game grid
def draw_block(surface, x, y, color):
    pygame.draw.rect(surface, color, (TOP_LEFT_X + x * GRID_SIZE, TOP_LEFT_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, BLACK, (TOP_LEFT_X + x * GRID_SIZE, TOP_LEFT_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Draw the game grid
def draw_grid(surface):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            draw_block(surface, j, i, grid[i][j])

# Check if a position is valid on the game grid
def is_valid_position(tetromino):
    for x, y in tetromino.get_blocks():
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x] != BLACK:
            return False
    return True

# Place a Tetromino on the game grid
def place_tetromino(tetromino):
    for x, y in tetromino.get_blocks():
        grid[y][x] = tetromino.color

# Clear complete lines and move the grid down
def clear_lines():
    full_rows = []
    for i in range(GRID_HEIGHT):
        if all(color != BLACK for color in grid[i]):
            full_rows.append(i)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)

# Check if the game is over
def is_game_over():
    return any(color != BLACK for color in grid[0])

# Restart the game
def restart_game():
    global game_over, grid, score

    game_over = False
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0

# Update the high score
def update_high_score():
    global score, high_score

    if score > high_score:
        high_score = score

# Draw the next block
def draw_next_block(surface, next_block):
    x = GRID_WIDTH + 2
    y = 4
    color = COLORS[SHAPES.index(next_block)]
    rotation = 0
    for i in range(len(next_block)):
        for j in range(len(next_block[i])):
            if next_block[i][j]:
                draw_block(surface, x + j, y + i, color)

def show_menu(win):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        win.fill(WHITE)

        # Draw the menu text
        font = pygame.font.Font(None, 36)
        title_text = font.render("Tetris", True, BLACK)
        start_text = font.render("Press SPACE to Start", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        win.blit(title_text, title_rect)
        win.blit(start_text, start_rect)
        win.blit(quit_text, quit_rect)

        # Update the display
        pygame.display.update()

        # Wait for user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def main():
    global game_over, score, high_score

    # Create the game window
    win = pygame.display.set_mode((WIDTH + 200, HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    run = True
    game_over = False

    # Show the main menu
    show_menu(win)

    tetromino = create_tetromino()
    next_block = random.choice(SHAPES)
    score = 0
    high_score = 0
    level = 1

    while run:
        clock.tick(5)  # Adjust the tick value to control the speed of the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
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
                    elif event.key == pygame.K_SPACE:
                        tetromino.rotate()
                        if not is_valid_position(tetromino):
                            tetromino.rotate()

        if not game_over:
            tetromino.move(0, 1)
            if not is_valid_position(tetromino):
                tetromino.move(0, -1)
                place_tetromino(tetromino)
                clear_lines()

                if is_game_over():
                    game_over = True
                    update_high_score()
                    run = False

                tetromino = Tetromino(GRID_WIDTH // 2 - 1, 0, next_block)
                next_block = random.choice(SHAPES)
                score += 10

        # Draw the game window
        win.fill(WHITE)
        pygame.draw.rect(win, BLACK, (TOP_LEFT_X, TOP_LEFT_Y, WIDTH, HEIGHT))
        draw_grid(win)
        tetromino.draw(win)
        draw_next_block(win, next_block)

        # Draw the score and high score
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score), True, BLACK)
        high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
        win.blit(score_text, (WIDTH + 10, 10))
        win.blit(high_score_text, (WIDTH + 10, 50))

        pygame.display.update()

    # After the game ends, show the menu again
    show_menu(win)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
