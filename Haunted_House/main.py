import pygame
import math
from constants import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from maze import *
from karl import *
from monsters import *
from bilder import *
from sound import *

bg_image = pygame.transform.scale(bg_image, (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))  

def draw_light_effect(screen, player, camera_x, camera_y):
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  

    light_radius = 120
    light_center_x = player.x * CELL_SIZE - camera_x + CELL_SIZE // 2
    light_center_y = player.y * CELL_SIZE - camera_y + CELL_SIZE // 2

    darkness.fill((0, 0, 0, 0))

    pygame.draw.rect(darkness, (0, 0, 0, 250), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    for i in range(light_radius, 0, -10):  
        alpha = max(0, 255 - (light_radius - i) * 2)  
        pygame.draw.circle(darkness, (0, 0, 0, alpha), (light_center_x, light_center_y), i)

    screen.blit(darkness, (0, 0))

def main():
    clock = pygame.time.Clock()
    clock.tick(FPS)
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Maze Game")

    maze, key_position = create_maze()
    player = Player()
    npc_1 = NPC(MAZE_WIDTH-20, MAZE_HEIGHT-20)
    npc_2 = NPC(20, MAZE_HEIGHT-40)
    has_key = False
    running = True
    won = False
    time_count = 1

    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    pygame.mixer.music.play(-1)

    player_move_delay = 4

    while running: 
        keys = pygame.key.get_pressed()
        if time_count == 60:
            time_count = 0
        else:
            time_count += 1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if time_count % player_move_delay == 0:
            if keys[pygame.K_UP]:
                player.move(0, -1, maze)
            if keys[pygame.K_DOWN]:
                player.move(0, 1, maze)
            if keys[pygame.K_LEFT]:
                player.move(-1, 0, maze)
            if keys[pygame.K_RIGHT]:
                player.move(1, 0, maze)

        npc_1.move_towards_player(player, maze, 8)
        npc_2.move_towards_player(player, maze, 10)

        if key_position:
            key_x, key_y = key_position
            distance = math.sqrt((player.x - key_x) ** 2 + (player.y - key_y) ** 2)

            if distance <= KEY_PICKUP_RADIUS:
                has_key = True
                key_position = None  

        distance1 = math.sqrt((player.x - npc_1.x) ** 2 + (player.y - npc_1.y) ** 2)
        distance2 = math.sqrt((player.x - npc_2.x) ** 2 + (player.y - npc_2.y) ** 2)
        if distance1 < NPC_HITBOX_RADIUS or distance2 < NPC_HITBOX_RADIUS:
            running = False

        if 18 < distance1 < 20 or 18 < distance2 < 20:
            eye_sound.play()

        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))

        scaled_surface = pygame.transform.scale(virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        virtual_screen.blit(bg_image, (-camera_x, -camera_y))
        draw_maze(virtual_screen, maze, camera_x, camera_y)
        player.draw(virtual_screen, camera_x, camera_y)
        npc_1.draw(virtual_screen, camera_x, camera_y)
        npc_2.draw(virtual_screen, camera_x, camera_y)

        if key_position:
            pygame.draw.circle(
                virtual_screen, (255, 215, 0),  
                (key_position[0] * CELL_SIZE - camera_x + CELL_SIZE // 2,
                 key_position[1] * CELL_SIZE - camera_y + CELL_SIZE // 2),
                CELL_SIZE // 2
            )

        if maze[player.y][player.x] == 2:
            if has_key:
                won = True
                running = False
            else:
                print("You need the key to escape!") 

        if time_count%60 != 0:
            draw_light_effect(virtual_screen, player, camera_x, camera_y)

        pygame.display.flip()

    screen.fill(WHITE)
    if won:
        message = font.render('You won!', True, BLACK)
    else:
        message = font.render('Game Over...', True, BLACK)

    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
