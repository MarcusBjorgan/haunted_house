import pygame
import random
from constants import *

def create_maze():
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

    def vegg(x_start, y_start, length, x_or_y):
        if x_or_y == "x":
            for i in range(length):
                maze[y_start][x_start+i] = 1
        else:
            for i in range(length):
                maze[y_start+i][x_start] = 1
    
    def create_door(x, y, length, orientation):
        for i in range(length):
            if orientation == "x":
                maze[y][x + i] = 0
            else:
                maze[y + i][x] = 0
    
    vegg(0, 60, MAZE_WIDTH, "x")
    vegg(0, 90, MAZE_WIDTH, "x")

    for i in range(5):
        vegg(i*40, 0, 60, "y")
        create_door(18 + i*40, 60, 6, "x")

        vegg(i*40, 90, 60, "y")
        create_door(18 + i*40, 90, 6, "x")

    # Set endpoint
    maze[MAZE_HEIGHT - 10][MAZE_WIDTH - 10] = 2

    # **Plasser nøkkel på et tilfeldig sted (ikke en vegg)**
    while True:
        key_x = random.randint(1, MAZE_WIDTH - 2)
        key_y = random.randint(1, MAZE_HEIGHT - 2)
        if maze[key_y][key_x] == 0:  # Sjekk at det ikke er en vegg
            maze[key_y][key_x] = 3  # 3 = nøkkel
            break


    return maze, (key_x, key_y)

def draw_maze(screen, maze, camera_x, camera_y):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL_COLOR, 
                    (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, RED, 
                    (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE))
