import pygame
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from maze import*
from karl import*
from timer import*
from bilder import *

bg_image = pygame.image.load("Assets/bg.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))  

def main():
    """
    bg_image = pygame.image.load("Assets/bg.png").convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    """

    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Maze Game")
    
    clock = pygame.time.Clock()
    maze = create_maze()
    player = Player()
    #countdown_time = 120  # Countdown time in seconds (2 minutes)
    #timer = Timer(countdown_time)
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
        

        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))

        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))


        virtual_screen.blit(bg_image, (-camera_x, -camera_y))
        draw_maze(virtual_screen, maze, camera_x, camera_y)
        player.draw(virtual_screen, camera_x, camera_y)


        scaled_surface = pygame.transform.scale(virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(30)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, maze)
        """


        """
        # screen.fill(WHITE)
        draw_maze(screen, maze)
        player.draw(screen)
        #timer.draw(screen)
        """
        if maze[player.y][player.x] == 2:
            won = True
            running = False
        #if timer.is_time_up():
            #running = False

        pygame.display.flip()
        clock.tick(30)
        
    screen.fill(WHITE)
    if won:
        time_text = font.render('You won!', True, BLACK)
    else:
        time_text = font.render('Time is up!', True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
if __name__ == "__main__":
    main()
