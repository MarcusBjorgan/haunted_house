import pygame
import math
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from maze import*
from karl import*
from monsters import*
from bilder import *

bg_image = pygame.transform.scale(bg_image, (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))  

def main():

    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Maze Game")
    
    clock = pygame.time.Clock()
    maze = create_maze()
    player = Player()
    npc = NPC() 
    running = True
    won = False
    
    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT)) 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(bg_image, (0, 0))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player.move(0, -2, maze)
        if keys[pygame.K_DOWN]:
            player.move(0, 2, maze)
        if keys[pygame.K_LEFT]:
            player.move(-2, 0, maze)
        if keys[pygame.K_RIGHT]:
            player.move(2, 0, maze) 

        npc.move_towards_player(player, maze)

        # Check if the NPC and player are at the same position
        distance = math.sqrt((player.x - npc.x) ** 2 + (player.y - npc.y) ** 2)
        if distance < NPC_HITBOX_RADIUS:
            running = False
        

        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))

        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))


        virtual_screen.blit(bg_image, (-camera_x, -camera_y))
        draw_maze(virtual_screen, maze, camera_x, camera_y)
        player.draw(virtual_screen, camera_x, camera_y)
        npc.draw(virtual_screen, camera_x, camera_y)


        scaled_surface = pygame.transform.scale(virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)
 
        if maze[player.y][player.x] == 2:
            won = True
            running = False

        pygame.display.flip()
        clock.tick(30)
        
    screen.fill(WHITE)
    if won:
        time_text = font.render('You won!', True, BLACK)
    else:
        time_text = font.render('Game Over...', True, BLACK)
    
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
if __name__ == "__main__":
    main()
