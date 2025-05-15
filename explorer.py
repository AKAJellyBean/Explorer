import pygame
from animated_sprite import AnimatedSprite


class Explorer:

    def __init__(self, grid, x, y, tile_size):
        self.grid = grid
        self.x = x
        self.y = y
        self.tile_size = tile_size

        self.pos_x = x * tile_size + tile_size // 2
        self.pos_y = y * tile_size + tile_size // 2
        self.target_pos = (self.pos_x, self.pos_y)

        self.path = []
        self.speed = 4

        # Load a single static image instead of animated sprite
        self.image = pygame.image.load("assets/images.png").convert_alpha()

        # Load animated sprite
        directions_paths = {
            "walk_Down": "assets/walk_Down.png",
            "walk_Left_Down": "assets/walk_Left_Down.png",
            "walk_Left_Up": "assets/walk_Left_Up.png",
            "walk_Up": "assets/walk_Up.png",
            "walk_Right_up": "assets/walk_Right_up.png",

        }

        self.sprite = AnimatedSprite(directions_paths, 64, 64, 6)



    def set_path(self, path):
        self.path = path
        if path:
            next_tile = path.pop(0)
            self.move_to(next_tile[0], next_tile[1])


    def update(self, dt):
        dx = self.target_pos[0] - self.pos_x
        dy = self.target_pos[1] - self.pos_y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist > 1:
            self.pos_x += self.speed * dx / dist
            self.pos_y += self.speed * dy / dist
        else:
            self.pos_x, self.pos_y = self.target_pos
            if self.path:
                next_tile = self.path.pop(0)
                self.move_to(next_tile[0], next_tile[1])

    def draw(self, surface):
        self.sprite.draw(surface, (int(self.pos_x), int(self.pos_y)), scale=2)

        print(f"pos_x: {self.pos_x}, pos_y: {self.pos_y}, target: {self.target_pos}")

    

    def decide_next_path(self):
        if self.is_thirsty:
            lake = self.grid.find_nearest_lake((self.x, self.y))
            if lake:
                path_to_lake = self.grid.find_path((self.x, self.y), lake)
                self.set_path(path_to_lake)
                self.target_lake = lake
                return
        # If not thirsty or after lake
        path_to_goal = self.grid.find_path((self.x, self.y), self.grid.goal_pos)
        self.set_path(path_to_goal)

    def move_to(self, grid_x, grid_y):
        self.x = grid_x
        self.y = grid_y
        self.target_pos = (grid_x * self.tile_size + self.tile_size // 2,
                           grid_y * self.tile_size + self.tile_size // 2)

    def draw(self, surface):
        self.sprite.draw(surface, (int(self.pos_x), int(self.pos_y)))



    def set_animation_direction(self, dx, dy):
        angle = pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))

        if -30 <= angle <= 30:
            direction = "walk_Right"
        elif 30 < angle <= 75:
            direction = "walk_Right_up"
        elif 75 < angle <= 105:
            direction = "walk_Up"
        elif 105 < angle <= 150:
            direction = "walk_Left_Up"
        elif angle > 150 or angle < -150:
            direction = "walk_Left_Down"
        elif -105 <= angle < -75:
            direction = "walk_Down"
        else:
            direction = "walk_Left_Down"

        self.sprite.set_direction(direction)
