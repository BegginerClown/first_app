import pygame

class WalkableMap:
    def __init__(self, filepath):
        self.map_surface = pygame.image.load(filepath).convert_alpha()
        self.width = self.map_surface.get_width()
        self.heigth = self.map_surface.get_height()

    def is_walkable(self, x, y):
        map_x = int(x)
        map_y = int(y)

        if not (0 <= map_x < self.width and 0 <= map_y < self.heigth):
            return  False

        color = self.map_surface.get_at((map_x, map_y))
        return color == (255, 255, 255, 255)