from constants import *
import pygame
import heapq  # Brukes for A*-algoritmen 

class NPC:
    def __init__(self):
        self.x = MAZE_WIDTH - 20  # Starter NPC-en på motsatt side av spilleren
        self.y = MAZE_HEIGHT - 20
        self.diameter = CELL_SIZE
        self.path = []  # Liste som lagrer veien NPC-en skal følge
        self.frame_counter = 0  # Teller hvor mange frames som har gått

    def find_path(self, player, maze):
        """Bruker A* algoritme for å finne den korteste veien til spilleren, inkludert diagonale bevegelser."""
        start = (int(self.x), int(self.y))  # Start (NPC)
        goal = (int(player.x), int(player.y))  # Mål (spilleren)

        open_set = []
        heapq.heappush(open_set, (0, start[0], start[1], []))
        visited = set()

        while open_set:
            cost, x, y, path = heapq.heappop(open_set)

            if (x, y) in visited:
                continue
            visited.add((x, y))

            if (x, y) == goal:
                self.path = path
                return

            # Mulige retninger
            neighbors = [
                (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),  # Vanlige bevegelser (høyre, venstre, ned, opp)
                (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)  # Diagonal bevegelse
            ]

            for nx, ny in neighbors:
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] != 1 and (nx, ny) not in visited:
                    new_cost = cost + (1.4 if abs(nx - x) == 1 and abs(ny - y) == 1 else 1)  # Diagonal bevegelse koster litt mer
                    heapq.heappush(open_set, (new_cost, nx, ny, path + [(nx, ny)]))

    def move_towards_player(self, player, maze):
        """Beveger NPC-en mot spilleren basert på A*-stien."""
        self.frame_counter += 1

        if self.frame_counter % 10 == 0 or not self.path:
            self.find_path(player, maze)  # Oppdaterer stien hver 10. frame

        if self.path and len(self.path) > 1:
            steps_to_move = min(1, len(self.path))
            for _ in range(steps_to_move):
                next_x, next_y = self.path.pop(0)
                self.x, self.y = next_x, next_y  # Oppdaterer NPC-posisjonen

    def draw(self, screen, camera_x, camera_y):
        """Tegner NPC-en på skjermen."""
        pygame.draw.circle(
            screen,
            GRAY,
            (int(self.x * CELL_SIZE - camera_x + self.diameter), 
             int(self.y * CELL_SIZE - camera_y + self.diameter)),
            self.diameter
        )
