
"""
import pygame
from constants import*

class Timer:
    def __init__(self, countdown_time):
        self.font = pygame.font.SysFont(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.countdown_time = countdown_time  # Time in seconds
    def get_time(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.countdown_time - elapsed_time // 1000
        if remaining_time < 0:
            remaining_time = 0
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        return f"Time: {minutes:02}:{seconds:02}"
    def draw(self, screen):
        time_text = self.font.render(self.get_time(), True, BLACK)
        screen.blit(time_text, (10, 600))
    def is_time_up(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.countdown_time - elapsed_time // 1000
        return remaining_time <= 0

"""