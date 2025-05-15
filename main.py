import pygame
import sys
from grid import Grid
from explorer import Explorer

# Initialize pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lost Explorer in Desert")

# Clock for fps control
clock = pygame.time.Clock()

def main():
    grid = Grid(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
    explorer_start = grid.explorer_pos
    explorer = Explorer(grid, explorer_start[0], explorer_start[1], TILE_SIZE)

    # Find path to goal
    path = grid.find_path(grid.explorer_pos, grid.goal_pos)
    explorer.set_path(path)

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update explorer position
        explorer.update(dt)

        # Draw everything
        screen.fill(BLACK)
        grid.draw(screen)
        explorer.draw(screen)


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
