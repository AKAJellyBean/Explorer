import pygame
class AnimatedSprite:
    def __init__(self, image_paths, frame_width, frame_height, frames_per_row, frame_duration=100):
        # image_paths: dict with direction -> file path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames_per_row = frames_per_row
        self.frame_duration = frame_duration

        self.frames = self.load_frames(image_paths)

        self.current_direction = list(image_paths.keys())[0]  # e.g. "walk_Down"
        self.current_frame = 0
        self.animation_timer = 0

    def load_frames(self, image_paths):
        frames = {}
        for direction, path in image_paths.items():
            sprite_sheet = pygame.image.load(path).convert_alpha()
            frames[direction] = []
            for col in range(self.frames_per_row):
                rect = pygame.Rect(
                    col * self.frame_width,
                    0,
                    self.frame_width,
                    self.frame_height
                )
                image = sprite_sheet.subsurface(rect)
                frames[direction].append(image)
        return frames

    def set_direction(self, direction):
        if direction in self.frames and direction != self.current_direction:
            self.current_direction = direction
            self.current_frame = 0
            self.animation_timer = 0

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_direction])

    def draw(self, surface, pos, scale=2):
        frame = self.frames[self.current_direction][self.current_frame]
        if scale != 1.0:
            # Scale frame size by factor
            new_width = int(self.frame_width * scale)
            new_height = int(self.frame_height * scale)
            frame = pygame.transform.scale(frame, (new_width, new_height))
            surface.blit(frame, (pos[0] - new_width // 2, pos[1] - new_height // 2))
        else:
            surface.blit(frame, (pos[0] - self.frame_width // 2, pos[1] - self.frame_height // 2))
