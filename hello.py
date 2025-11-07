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
        self.speed = 4
        self.current_frame = 0
        self.animation_speed = 8
        self.frame_counter = 0
        self.last_direction = 'right'

        self.walk_right_frames = [
            pygame.image.load(f'images/player/walk right/{i}.png') for i in range(1, 7)
        ]
        self.walk_left_frames = [
            pygame.image.load(f'images/player/walk left/{i}.png') for i in range(1, 7)
        ]
        self.chill_frames = [
            pygame.image.load('images/player/chill right/1.png'),
            pygame.image.load('images/player/chill left/1.png')
        ]

        self.direction = 'right'
        self.current_frames = self.walk_right_frames

    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.frame_counter = 0

    def self_moving(self):
        self.update_animation()
        if self.direction == 'right':
            self.x += self.speed
            if self.x >= 1100:
                self.direction = 'left'
                self.current_frames = self.walk_left_frames
        elif self.direction == 'left':
            self.x -= self.speed
            if self.x <= 200:
                self.direction = 'right'
                self.current_frames = self.walk_right_frames

    def moving(self, keys):
        self.update_animation()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 200:
            self.x -= self.speed
            self.current_frames = self.walk_left_frames
            self.last_direction = 'left'
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < 1100:
            self.x += self.speed
            self.current_frames = self.walk_right_frames
            self.last_direction = 'right'
        else:
            if self.last_direction == 'right':
                self.current_frame = 0
            elif self.last_direction == 'left':
                self.current_frame = 1
            self.current_frames = self.chill_frames

    def draw(self, surface):
        surface.blit(self.current_frames[self.current_frame], (self.x, self.y))


player = Player(name='Pete')





running = True
while running:
    keys = pygame.key.get_pressed()
    player.moving(keys)
    screen.blit(bg, (0, 0))
    player.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    clock.tick(60)



