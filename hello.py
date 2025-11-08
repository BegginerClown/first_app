import pygame

clock = pygame.time.Clock()


pygame.init()
screen = pygame.display.set_mode((1376, 768))#, flags=pygame.NOFRAME)
pygame.display.set_caption("Тамагочи")
icon = pygame.image.load('images/icons/icon.png')
bg = pygame.image.load('images/back/back.png')
pygame.display.set_icon(icon)

class Player():
    def __init__(self, name: str, x=200, y=500):
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
            pygame.image.load(f'images/player/walk right/{i}.png') for i in range(1, 7)
        ]
        self.walk_left_frames = [
            pygame.image.load(f'images/player/walk left/{i}.png') for i in range(1, 7)
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
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.y >= 400:
            self.update_animation(self.back_front_anim_speed)
            self.y -= self.back_front_speed
            self.current_frames = self.walk_back_frames
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y <= 500:
            self.update_animation(self.back_front_anim_speed)
            self.y += self.back_front_speed
            self.current_frames = self.walk_front_frames
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 200:
            self.update_animation(self.animation_speed)
            self.x -= self.walk_speed
            self.current_frames = self.walk_left_frames
            self.last_direction = 'left'
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < 1100:
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

    def draw(self, surface):
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

        offset_x = self.x - (scaled_width - original_width) // 2
        offset_y = self.y - (scaled_height - original_height) // 2
        surface.blit(scaled_sprite, (offset_x, offset_y))


player = Player(name='Pete')





running = True
debug_mode = False
font = pygame.font.SysFont('Arial', 20)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                debug_mode = not debug_mode

    keys = pygame.key.get_pressed()
    player.moving(keys)
    screen.blit(bg, (0, 0))
    if debug_mode:
        text = font.render(f'X: {player.x}, Y: {player.y}', True, (255, 255, 255))
        screen.blit(text, (10, 10))
    player.draw(screen)
    pygame.display.update()

    clock.tick(60)
pygame.quit()



