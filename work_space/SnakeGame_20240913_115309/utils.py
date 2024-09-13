import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, 20):
        pygame.draw.line(surface, (200, 200, 200), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 20):
        pygame.draw.line(surface, (200, 200, 200), (0, y), (SCREEN_WIDTH, y))

def display_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(text, (10, 10))