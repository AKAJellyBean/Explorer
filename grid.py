import os
import random
import pygame
import heapq

from pathfinder import heuristic


class Grid:

    def __init__(self, screen_width, screen_height, tile_size):
        self.cols = screen_width // tile_size
        self.rows = screen_height // tile_size
        self.tile_size = tile_size

        self.bg_tile = pygame.image.load("assets/bg.png")
        self.bg_tile = pygame.transform.scale(self.bg_tile, (tile_size, tile_size))

        self.lake_positions = [(5, 5), (10, 8)]
        self.lake = pygame.image.load("assets/lake.png")
        self.lake = pygame.transform.scale(self.lake, (tile_size, tile_size))

        self.sheltor = pygame.image.load("assets/sheltor.png")
        self.sheltor = pygame.transform.scale(self.sheltor, (tile_size, tile_size))

        # Load decoration images
        self.decor_images = []
        decoration_path = "assets/decor"
        for filename in os.listdir(decoration_path):
            img = pygame.image.load(os.path.join(decoration_path, filename))
            img = pygame.transform.scale(img, (tile_size, tile_size))
            self.decor_images.append(img)

        self.decor_pos = {}
        self.lake_pos = set()
        self.sheltor_pos = set()
        self.goal_pos = None  # (col, row)
        self.explorer_pos = None  # (col, row)

        self.place_decorations(40)
        self.place_sheltors(2)
        self.place_lakes(3)
        self.place_goal()
        self.place_explorer()

    def find_nearest_lake(self, pos):
        x, y = pos
        nearest = None
        min_dist = float('inf')
        for lake in self.lake_positions:
            dist = abs(lake[0] - x) + abs(lake[1] - y)  # Manhattan distance
            if dist < min_dist:
                min_dist = dist
                nearest = lake
        return nearest


    def place_decorations(self, count):
        placed = 0
        while placed < count:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)
            key = (col, row)
            if key not in self.decor_pos and key not in self.lake_pos and key not in self.sheltor_pos:
                self.decor_pos[key] = random.choice(self.decor_images)
                placed += 1

    def place_lakes(self, count):
        placed = 0
        while placed < count:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)
            key = (col, row)
            if key not in self.lake_pos and key not in self.decor_pos and key not in self.sheltor_pos:
                self.lake_pos.add(key)
                placed += 1

    def place_sheltors(self, count):
        placed = 0
        while placed < count:
            col = random.randint(0, self.cols - 1)
            row = random.randint(0, self.rows - 1)
            key = (col, row)
            if key not in self.sheltor_pos and key not in self.lake_pos and key not in self.decor_pos:
                self.sheltor_pos.add(key)
                placed += 1

    def place_goal(self):
        possible_positions = []
        for x in range(self.cols):
            possible_positions.append((x, 0))  # top row
            possible_positions.append((x, self.rows - 1))  # bottom row
        for y in range(1, self.rows - 1):
            possible_positions.append((0, y))  # left col
            possible_positions.append((self.cols - 1, y))  # right col

        random.shuffle(possible_positions)
        for pos in possible_positions:
            if pos not in self.lake_pos and pos not in self.decor_pos and pos not in self.sheltor_pos:
                self.goal_pos = pos
                break

    def place_explorer(self):
        free_positions = []
        for x in range(self.cols):
            for y in range(self.rows):
                pos = (x, y)
                if pos not in self.lake_pos and pos not in self.decor_pos and pos not in self.sheltor_pos and pos != self.goal_pos:
                    free_positions.append(pos)

        if free_positions:
            self.explorer_pos = random.choice(free_positions)
        else:
            self.explorer_pos = None

    def draw(self, surface):
        for x in range(self.cols):
            for y in range(self.rows):
                surface.blit(self.bg_tile, (x * self.tile_size, y * self.tile_size))

                if (x, y) in self.decor_pos:
                    surface.blit(self.decor_pos[(x, y)], (x * self.tile_size, y * self.tile_size))

                if (x, y) in self.lake_pos:
                    surface.blit(self.lake, (x * self.tile_size, y * self.tile_size))

                if (x, y) in self.sheltor_pos:
                    surface.blit(self.sheltor, (x * self.tile_size, y * self.tile_size))

        # Draw goal as red rectangle
        if self.goal_pos:
            goal_rect = pygame.Rect(
                self.goal_pos[0] * self.tile_size + 5,
                self.goal_pos[1] * self.tile_size + 5,
                self.tile_size - 10,
                self.tile_size - 10
            )
            pygame.draw.rect(surface, (255, 0, 0), goal_rect)

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def is_walkable(self, pos):
        x, y = pos
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return False
        if pos in self.lake_pos or pos in self.sheltor_pos or pos in self.decor_pos:
            return False
        return True

    def find_path(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current_priority, current = heapq.heappop(frontier)

            if current == goal:
                break

            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1),
            ]

            for next_pos in neighbors:
                if not self.is_walkable(next_pos):
                    continue
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        # Reconstruct path
        path = []
        cur = goal
        while cur != start:
            if cur in came_from:
                path.append(cur)
                cur = came_from[cur]
            else:
                # No path found
                return []
        path.reverse()
        return path
