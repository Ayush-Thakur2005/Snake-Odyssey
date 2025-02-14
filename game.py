import pygame
import random

# Initialize Pygame
pygame.init()

# Set up game constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Font for score
font = pygame.font.SysFont("arial", 36)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  # Initial snake
        self.direction = 'RIGHT'
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= CELL_SIZE
        elif self.direction == 'DOWN':
            head_y += CELL_SIZE
        elif self.direction == 'LEFT':
            head_x -= CELL_SIZE
        elif self.direction == 'RIGHT':
            head_x += CELL_SIZE

        new_head = (head_x, head_y)
        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def grow_snake(self):
        self.grow = True

    def collision(self):
        head_x, head_y = self.body[0]
        # Check if snake hits the wall
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        # Check if snake hits itself
        if (head_x, head_y) in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.x = random.randrange(0, WIDTH, CELL_SIZE)
        self.y = random.randrange(0, HEIGHT, CELL_SIZE)
    
    def spawn(self):
        self.x = random.randrange(0, WIDTH, CELL_SIZE)
        self.y = random.randrange(0, HEIGHT, CELL_SIZE)
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, CELL_SIZE, CELL_SIZE))

# Main game loop
def game():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        
        # Handle events
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

        # Move snake
        snake.move()

        # Check for collision
        if snake.collision():
            running = False

        # Check for food collision
        if snake.body[0] == (food.x, food.y):
            score += 1
            snake.grow_snake()
            food.spawn()

        # Draw everything
        snake.draw(screen)
        food.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Control the game speed
        clock.tick(FPS)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game()
