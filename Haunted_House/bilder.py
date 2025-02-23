import pygame
from constants import*

bg_image = pygame.image.load("Assets/bg.png").convert_alpha()

bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
