import pygame
import random
from bilder import *
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

    """
    for i in range(5):
        vegg(i*40, 0, 60, "y")
        create_door(18 + i*40, 60, 6, "x")

        vegg(i*40, 90, 60, "y")
        create_door(18 + i*40, 90, 6, "x")
    """
    vegg(0, (MAZE_HEIGHT-25)//2, MAZE_WIDTH, "x")
    vegg(0, (MAZE_HEIGHT+25)//2, MAZE_WIDTH, "x")

    vegg(0, (MAZE_HEIGHT-25)//4, 25, "x")
    vegg(25, 0, (MAZE_HEIGHT-25)//2, "y")
    create_door(25, (MAZE_HEIGHT-25)//8-2, 4, "y")
    create_door(25, (MAZE_HEIGHT+25)//4-2, 4, "y")
    create_door(26, (MAZE_HEIGHT-25)//2, 9, "x")
    create_door(26, (MAZE_HEIGHT+25)//2, 9, "x")

    vegg(35, 0, (MAZE_HEIGHT-25)//2, "y")
    vegg(35, (MAZE_HEIGHT-25)//4-5, MAZE_WIDTH-35, "x")
    vegg(35, (MAZE_HEIGHT-25)//4+5, MAZE_WIDTH-35, "x")
    create_door(35, (MAZE_HEIGHT-25)//4-5, 10, "y")

    vegg(MAZE_WIDTH//4, (MAZE_HEIGHT+25)//2, (MAZE_HEIGHT-25)//2+1, "y")
    create_door(MAZE_WIDTH//4, MAZE_HEIGHT-((MAZE_HEIGHT - 25)//4) - 5, 10, "y")



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
    """
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL_COLOR, 
                    (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, RED, 
                    (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE))

    """
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                screen.blit(wall_texture, 
                            (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, RED, 
                    (x * CELL_SIZE - camera_x, y * CELL_SIZE - camera_y, CELL_SIZE, CELL_SIZE))

