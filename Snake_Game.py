import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🐍 Snake Game by Shreyas")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Fonts and Clock
FONT = pygame.font.SysFont('Arial', 25)
CLOCK = pygame.time.Clock()

# Block and Speed will be set later based on difficulty
BLOCK_SIZE = 10
SPEED = 15

# High score file
HIGH_SCORE_FILE = "highscore.txt"


# Snake class
class Snake:
    def __init__(self):
        self.body = [[300, 200]]
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[-1][:]
        if self.direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            head[1] += BLOCK_SIZE
        elif self.direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            head[0] += BLOCK_SIZE
        self.body.append(head)
        self.body.pop(0)

    def grow(self):
        self.body.insert(0, self.body[0])

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(WINDOW, GREEN, [*segment, BLOCK_SIZE, BLOCK_SIZE])

    def collided_with_self(self):
        return self.body[-1] in self.body[:-1]

    def get_head(self):
        return self.body[-1]


# Food class
class Food:
    def __init__(self, snake_body, obstacles):
        self.position = self.random_position(snake_body, obstacles)

    def random_position(self, snake_body, obstacles):
        while True:
            x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            if [x, y] not in snake_body and [x, y] not in obstacles:
                return [x, y]

    def draw(self):
        pygame.draw.rect(WINDOW, RED, [*self.position, BLOCK_SIZE, BLOCK_SIZE])


# Obstacles class
class Obstacles:
    def __init__(self, count):
        self.count = count
        self.blocks = self.generate_obstacles()

    def generate_obstacles(self):
        blocks = []
        for _ in range(self.count):
            x = round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            y = round(random.randrange(0, WINDOW_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            blocks.append([x, y])
        return blocks

    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(WINDOW, GRAY, [*block, BLOCK_SIZE, BLOCK_SIZE])


# Draw score and high score
def draw_score(score, high_score):
    score_text = FONT.render(f"Score: {score}  High Score: {high_score}", True, BLACK)
    WINDOW.blit(score_text, [10, 10])


# Game Over screen
def game_over_screen(score, high_score):
    WINDOW.fill(WHITE)
    message1 = FONT.render(f"Game Over! Your Score: {score}", True, RED)
    message2 = FONT.render(f"High Score: {high_score}", True, BLACK)
    message3 = FONT.render("Press C to Play Again or Q to Quit", True, BLACK)
    WINDOW.blit(message1, [WINDOW_WIDTH // 6, WINDOW_HEIGHT // 4])
    WINDOW.blit(message2, [WINDOW_WIDTH // 6, WINDOW_HEIGHT // 3])
    WINDOW.blit(message3, [WINDOW_WIDTH // 6, WINDOW_HEIGHT // 2])
    pygame.display.update()
    update_high_score(score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    main()


# Read and Update High Score
def get_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, 'r') as file:
        return int(file.read())


def update_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, 'w') as file:
            file.write(str(score))


# Difficulty selection
def select_difficulty():
    global SPEED
    WINDOW.fill(WHITE)
    msg1 = FONT.render("Select Difficulty: E - Easy, M - Medium, H - Hard", True, BLACK)
    WINDOW.blit(msg1, [WINDOW_WIDTH // 8, WINDOW_HEIGHT // 3])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    SPEED = 10
                    return 3  # obstacle count
                elif event.key == pygame.K_m:
                    SPEED = 15
                    return 7
                elif event.key == pygame.K_h:
                    SPEED = 20
                    return 12


# Game loop
def main():
    obstacle_count = select_difficulty()
    snake = Snake()
    obstacles = Obstacles(obstacle_count)
    food = Food(snake.body, obstacles.blocks)
    score = 0
    high_score = get_high_score()

    running = True
    while running:
        CLOCK.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'

        snake.move()
        head = snake.get_head()

        # Check wall collision
        if head[0] < 0 or head[0] >= WINDOW_WIDTH or head[1] < 0 or head[1] >= WINDOW_HEIGHT:
            game_over_screen(score, high_score)

        # Check self collision
        if snake.collided_with_self():
            game_over_screen(score, high_score)

        # Check obstacle collision
        if head in obstacles.blocks:
            game_over_screen(score, high_score)

        # Check food collision
        if head == food.position:
            snake.grow()
            score += 1
            food = Food(snake.body, obstacles.blocks)

        # Drawing
        WINDOW.fill(WHITE)
        snake.draw()
        food.draw()
        obstacles.draw()
        draw_score(score, get_high_score())
        pygame.display.update()

    pygame.quit()


# Start the game
main()
