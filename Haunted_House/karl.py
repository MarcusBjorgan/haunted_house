from constants import *
import pygame

class Player:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.diameter = CELL_SIZE*4

        self.image = pygame.image.load("Haunted_House/Assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE*4, CELL_SIZE*4))
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx 
        new_y = self.y + dy 

        if (
            0 <= new_x < MAZE_WIDTH - self.diameter//CELL_SIZE + 1 and
            0 <= new_y < MAZE_HEIGHT - self.diameter//CELL_SIZE + 1 and
            maze[int(new_y + self.diameter//CELL_SIZE - 2)][int(new_x + self.diameter//CELL_SIZE - 2)] != 1  
        ):
            self.x = new_x
            self.y = new_y
    

    def draw(self, screen, camera_x, camera_y):
        screen.blit(
            self.image, 
            (int(self.x * CELL_SIZE - camera_x), int(self.y * CELL_SIZE - camera_y))
        )
        """
        pygame.draw.circle(
            screen,
            GREEN,
            (self.x * CELL_SIZE - camera_x + self.diameter, self.y * CELL_SIZE - camera_y + self.diameter),
            self.diameter
        )
        """
