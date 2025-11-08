import pygame
from map.can_move import IsCanMove
can_move = IsCanMove()
class Player():
    def __init__(self, name: str, x=200, y=500):
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        self.name = name
        self.x = x
        self.y = y
        self.walk_speed = 4
        self.back_front_speed = 2
        self.current_frame = 0
        self.animation_speed = 8
        self.back_front_anim_speed = 12
        self.frame_counter = 0
        self.last_direction = 'right'

        self.walk_right_frames = [
            #pygame.image.load(f'images/player/walk right/{i}.png') for i in range(1, 7)
            pygame.image.load(f'images/player/knight/walk right/{i}.png') for i in range(1, 9)
        ]
        self.walk_left_frames = [
            #pygame.image.load(f'images/player/walk left/{i}.png') for i in range(1, 7)
            pygame.image.load(f'images/player/knight/walk left/{i}.png') for i in range(1, 9)
        ]
        self.walk_back_frames = [
            pygame.image.load(f'images/player/walk back/{i}.png') for i in range(1, 3)
        ]
        self.walk_front_frames = [
            pygame.image.load(f'images/player/walk front/{i}.png') for i in range(1, 3)
        ]
        self.chill_frames = [
            pygame.image.load('images/player/chill right/1.png'),
            pygame.image.load('images/player/chill left/1.png')
        ]

        self.direction = 'right'
        self.current_frames = self.walk_right_frames

    def update_stats(self):
        self.hunger = max(0, self.hunger - 0.01)
        self.happiness = max(0, self.happiness - 0.005)
        self.energy = max(0, self.energy - 0.003)

    def update_animation(self, anim_speed):
        self.frame_counter += 1
        if self.frame_counter >= anim_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.frame_counter = 0

    def self_moving(self):
        self.update_animation(self.animation_speed)
        if self.direction == 'right':
            self.x += self.walk_speed
            if self.x >= 1100:
                self.direction = 'left'
                self.current_frames = self.walk_left_frames

        elif self.direction == 'left':
            self.x -= self.walk_speed
            if self.x <= 200:
                self.direction = 'right'
                self.current_frames = self.walk_right_frames

    def moving(self, keys):
        old_frames = self.current_frames

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y >= 414 and can_move.can_move_x(self.x, self.y - self.walk_speed):
            self.update_animation(self.back_front_anim_speed)
            self.y -= self.back_front_speed
            self.current_frames = self.walk_back_frames

        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y <= 550:
            self.update_animation(self.back_front_anim_speed)
            self.y += self.back_front_speed
            self.current_frames = self.walk_front_frames

        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 148 and can_move.can_move_x(self.x - self.walk_speed, self.y):
            self.update_animation(self.animation_speed)
            self.x -= self.walk_speed
            self.current_frames = self.walk_left_frames
            self.last_direction = 'left'

        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < 1200 and can_move.can_move_x(self.x + self.walk_speed, self.y):
            self.update_animation(self.animation_speed)
            self.x += self.walk_speed
            self.current_frames = self.walk_right_frames
            self.last_direction = 'right'

        else:
            if self.last_direction == 'right':
                self.current_frame = 0
            elif self.last_direction == 'left':
                self.current_frame = 1
            self.current_frames = self.chill_frames

        if self.current_frames != old_frames:
            self.current_frame = 0

    def draw(self, surface, screen_width):
        current_sprite = self.current_frames[self.current_frame]
        original_width = current_sprite.get_width()
        original_height = current_sprite.get_height()

        scale_factor = max(0.5, 1.0 - (500 - self.y) / 500)
        scaled_sprite = pygame.transform.scale(
            current_sprite,
            (int(current_sprite.get_width() * scale_factor),
             int(current_sprite.get_height() * scale_factor))
        )

        scaled_width = scaled_sprite.get_width()
        scaled_height = scaled_sprite.get_height()
        offset_y = self.y - (scaled_height - original_height) // 2

        center_x = screen_width // 2
        offset_x = self.x - (scaled_width - original_width) // 2

        perspective_factor = (500 - self.y) /500
        perspective_factor = min(1.0, perspective_factor * 3.0)
        distance_from_center = abs(offset_x - center_x)
        max_distance = center_x
        adjusted_perspective = perspective_factor * (1 - distance_from_center / max_distance)
        offset_x = offset_x * (1 - adjusted_perspective) + center_x * adjusted_perspective

        surface.blit(scaled_sprite, (offset_x, offset_y))