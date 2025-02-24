import pygame
import math
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

from maze import *
from karl import *
from monsters import *
from bilder import *

bg_image = pygame.transform.scale(bg_image, (MAZE_WIDTH * CELL_SIZE, MAZE_HEIGHT * CELL_SIZE))  


def draw_light_effect(screen, player, camera_x, camera_y):
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Transparent surface

    # Light properties
    light_radius = 300  # Change this to adjust vision range

    light_center_x = player.x * CELL_SIZE - camera_x + CELL_SIZE // 2
    light_center_y = player.y * CELL_SIZE - camera_y + CELL_SIZE // 2

    #light_center_x = VIRTUAL_WIDTH / 2
    #light_center_y = VIRTUAL_HEIGHT / 2

    #light_center_x = (player.x * CELL_SIZE - camera_x) * (SCREEN_WIDTH / VIRTUAL_WIDTH) + CELL_SIZE // 2
    #light_center_y = (player.y * CELL_SIZE - camera_y) * (SCREEN_HEIGHT / VIRTUAL_HEIGHT) + CELL_SIZE // 2

    darkness.fill((0, 0, 0, 0))

    # Darken entire screen
    pygame.draw.rect(darkness, (0, 0, 0, 250), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create fading light effect
    for i in range(light_radius, 0, -10):  
        alpha = max(0, 255 - (light_radius - i) * 2)  # Creates a fade effect
        pygame.draw.circle(darkness, (0, 0, 0, alpha), (light_center_x, light_center_y), i)

    # Apply the darkness effect **on top of everything**
    screen.blit(darkness, (0, 0))


def main():
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Maze Game")

    clock = pygame.time.Clock()
    maze, key_position = create_maze()
    player = Player()
    npc_1 = NPC(MAZE_WIDTH-20, MAZE_HEIGHT-20)
    npc_2 = NPC(MAZE_WIDTH-20, MAZE_HEIGHT-40)
    has_key = False
    running = True
    won = False

    virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player.move(0, -1, maze)
        if keys[pygame.K_DOWN]:
            player.move(0, 1, maze)
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, maze)

        npc_1.move_towards_player(player, maze, 2)
        npc_2.move_towards_player(player, maze, 3)

        # Check if the player picks up the key
        if key_position:
            key_x, key_y = key_position
            distance = math.sqrt((player.x - key_x) ** 2 + (player.y - key_y) ** 2)

            if distance <= KEY_PICKUP_RADIUS:
                has_key = True
                key_position = None  # Remove key from the map

        # Check if the NPC and player collide (Game Over)
        distance1 = math.sqrt((player.x - npc_1.x) ** 2 + (player.y - npc_1.y) ** 2)
        distance2 = math.sqrt((player.x - npc_2.x) ** 2 + (player.y - npc_2.y) ** 2)
        if distance1 < NPC_HITBOX_RADIUS or distance2 < NPC_HITBOX_RADIUS:
            running = False

        # Camera follows player
        camera_x = max(0, min(player.x * CELL_SIZE - VIRTUAL_WIDTH // 2, MAZE_WIDTH * CELL_SIZE - VIRTUAL_WIDTH))
        camera_y = max(0, min(player.y * CELL_SIZE - VIRTUAL_HEIGHT // 2, MAZE_HEIGHT * CELL_SIZE - VIRTUAL_HEIGHT))

        # Scale virtual screen to fit the main screen
        scaled_surface = pygame.transform.scale(virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        # Draw everything on the virtual screen
        virtual_screen.blit(bg_image, (-camera_x, -camera_y))
        draw_maze(virtual_screen, maze, camera_x, camera_y)
        player.draw(virtual_screen, camera_x, camera_y)
        npc_1.draw(virtual_screen, camera_x, camera_y)
        npc_2.draw(virtual_screen, camera_x, camera_y)

        # Draw the key if it's still there
        if key_position:
            pygame.draw.circle(
                virtual_screen, (255, 215, 0),  # Gold-colored key
                (key_position[0] * CELL_SIZE - camera_x + CELL_SIZE // 2,
                 key_position[1] * CELL_SIZE - camera_y + CELL_SIZE // 2),
                CELL_SIZE // 2
            )

        # Check if player reaches the exit
        if maze[player.y][player.x] == 2:
            if has_key:
                won = True
                running = False
            else:
                print("You need the key to escape!")  # Could be replaced with a GUI message

        # Apply the darkness effect **LAST**
        draw_light_effect(virtual_screen, player, camera_x, camera_y)

        pygame.display.flip()
        clock.tick(30)

    # End screen
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
