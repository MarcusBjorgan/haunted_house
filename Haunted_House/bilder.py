import pygame
from constants import*

bg_image = pygame.image.load("Haunted_House/Assets/bg.png").convert_alpha()

wall_texture = pygame.image.load("Haunted_House/Assets/parquet.png").convert_alpha()

wall_texture = pygame.transform.scale(wall_texture, (CELL_SIZE, CELL_SIZE))

