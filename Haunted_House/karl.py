from constants import *
import pygame

class Player:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.diameter = CELL_SIZE

    def move(self, dx, dy, maze):
        new_x = self.x + dx 
        new_y = self.y + dy 

        if 0 <= new_x < MAZE_WIDTH - self.diameter/4 and 0 <= new_y < MAZE_HEIGHT - self.diameter/4 and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.circle(
            screen,
            GREEN,
            (self.x * CELL_SIZE - camera_x + self.diameter, self.y * CELL_SIZE - camera_y + self.diameter),
            self.diameter
        )