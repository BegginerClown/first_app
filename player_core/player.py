import pygame
from map.can_move import IsCanMove
from DB.DB import DB
db = DB('DB/save.db')
#db.create_tables()

can_move = IsCanMove()
class Player():
    def __init__(self, name: str):
        data = db.get_player_data(name)
        self.hunger = int(data['hunger'])
        self.happiness = int(data['happiness'])
        self.energy = int(data['energy'])
        self.name = name
        self.x = int(data['pos_x'])
        self.y = int(data['pos_y'])
        self.walk_speed = 4
        self.back_front_speed = 1
        self.current_frame = 0
        self.animation_speed = 8
        self.back_front_anim_speed = 12
        self.frame_counter = 0
        self.last_direction = 'right'
        self.hunger_modif = 0.5
        self.happiness_modif = 0.1
        self.energy_modif = 1

        self.walk_right_frames = [
            pygame.image.load(f'images/player/walk right/{i}.png') for i in range(1, 7)
            #pygame.image.load(f'images/player/knight/walk right/{i}.png') for i in range(1, 9)
        ]
        self.walk_left_frames = [
            pygame.image.load(f'images/player/walk left/{i}.png') for i in range(1, 7)
            #pygame.image.load(f'images/player/knight/walk left/{i}.png') for i in range(1, 9)
        ]
        self.walk_back_frames = [
            pygame.image.load(f'images/player/walk back/{i}.png') for i in range(1, 3)
        ]
        self.walk_front_frames = [
            pygame.image.load(f'images/player/walk front/{i}.png') for i in range(1, 3)
        ]
        self.sit_right = [
            pygame.image.load(f'images/player/sit right/{i}.png') for i in range(1, 8)
        ]
        self.sit_left = [
            pygame.image.load(f'images/player/sit left/{i}.png') for i in range(1, 8)
        ]
        self.chill_frames = [
            pygame.image.load('images/player/chill right/1.png'),
            pygame.image.load('images/player/chill left/1.png')
        ]

        self.direction = 'right'
        self.current_frames = self.walk_right_frames
        self.idle_start_time = pygame.time.get_ticks()
        self.last_input_time = pygame.time.get_ticks()#для автошага
        self.idle_duration = 5000
        self.idle_duration2 = 6000#для автошага
        self.is_sitting = False
        self.is_getting_up = False

    def update_stats(self):
        self.hunger = max(0, self.hunger - 0.01 * self.hunger_modif)
        self.happiness = max(0, self.happiness - 0.005 * self.happiness_modif)
        self.energy = max(0, self.energy - 0.003 * self.energy_modif)

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
        is_moving = any([
            keys[pygame.K_UP], keys[pygame.K_w],
            keys[pygame.K_DOWN], keys[pygame.K_s],
            keys[pygame.K_LEFT], keys[pygame.K_a],
            keys[pygame.K_RIGHT], keys[pygame.K_d]
        ])

        if is_moving:
            self.last_input_time = pygame.time.get_ticks()#для автошага
            if self.is_sitting and not self.is_getting_up:
                self.is_getting_up = True
                self.is_sitting = False
                self.idle_start_time = pygame.time.get_ticks()

        if self.is_getting_up:
            if self.current_frame > 0:
                self.current_frame -= 1
            else:
                self.is_getting_up = False

        elif self.is_sitting:
            if self.last_direction == 'right':
                self.current_frames = self.sit_right
            elif self.last_direction == 'left':
                self.current_frames = self.sit_left
            if self.current_frame < len(self.current_frames) - 1:
                self.update_animation(self.animation_speed)
            else:
                self.current_frame = len(self.current_frames) - 1

        else:
            if not self.is_getting_up:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y >= 414 and can_move.can_move_x(self.x,
                                                                                                     self.y - self.walk_speed):
                    self.update_animation(self.back_front_anim_speed)
                    self.y -= self.back_front_speed
                    self.current_frames = self.walk_back_frames

                elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y <= 550:
                    self.update_animation(self.back_front_anim_speed)
                    self.y += self.back_front_speed
                    self.current_frames = self.walk_front_frames

                elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 148 and can_move.can_move_x(
                        self.x - self.walk_speed, self.y):
                    self.update_animation(self.animation_speed)
                    self.x -= self.walk_speed
                    self.current_frames = self.walk_left_frames
                    self.last_direction = 'left'

                elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < 1200 and can_move.can_move_x(
                        self.x + self.walk_speed, self.y):
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

        if self.current_frames != old_frames and not self.is_getting_up:
            self.current_frame = 0

        if not is_moving:
            current_time = pygame.time.get_ticks()
            # для автошага
            '''if current_time - self.last_input_time > self.idle_duration2 and self.is_sitting and not self.is_getting_up:
                self.is_getting_up = True
                self.is_sitting = False'''
            '''if current_time - self.last_input_time > self.idle_duration2:
                self.self_moving()'''
            if current_time - self.idle_start_time > self.idle_duration and not self.is_sitting and not self.is_getting_up:
                self.is_sitting = True

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

    def save_data(self):
        db.set_player_data(
            pos_x=self.x,
            pos_y=self.y,
            hunger=int(self.hunger),
            happiness=int(self.happiness),
            energy=int(self.energy),
            name=self.name
        )
