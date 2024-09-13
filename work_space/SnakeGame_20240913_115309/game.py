import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_SIZE, FPS
from utils import draw_grid, display_score

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (0, -SNAKE_SIZE)

    def move(self):
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        # Increase the length of the snake only if it eats food
        self.length += 1

    def get_head_position(self):
        return self.positions[0]

    def get_body(self):
        return self.positions

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.respawn()

    def respawn(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, 
                        random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)
        # Ensure food does not appear on the snake
        while self.position in Snake().get_body():
            self.position = (random.randint(0, (SCREEN_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE, 
                             random.randint(0, (SCREEN_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = (0, -SNAKE_SIZE)
                    elif event.key == pygame.K_DOWN:
                        self.snake.direction = (0, SNAKE_SIZE)
                    elif event.key == pygame.K_LEFT:
                        self.snake.direction = (-SNAKE_SIZE, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.direction = (SNAKE_SIZE, 0)

            self.snake.move()
            if self.check_collisions():
                self.game_over()
                running = False
            self.render()
            self.clock.tick(FPS)

    def check_collisions(self):
        head = self.snake.get_head_position()
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        if head in self.snake.get_body()[1:]:
            return True
        if head == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 1
        return False

    def render(self):
        self.screen.fill((0, 0, 0))
        draw_grid(self.screen)
        for pos in self.snake.get_body():
            pygame.draw.rect(self.screen, (0, 255, 0), (pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food.position[0], self.food.position[1], SNAKE_SIZE, SNAKE_SIZE))
        display_score(self.screen, self.score)
        pygame.display.update()

    def game_over(self):
        # Display Game Over message
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing