import pygame
from player_core.player import Player


clock = pygame.time.Clock()


pygame.init()
screen = pygame.display.set_mode((1376, 768))#, flags=pygame.NOFRAME)
pygame.display.set_caption("Тамагочи")
icon = pygame.image.load('images/icons/icon.png')
bg = pygame.image.load('images/back/back.png')
bg_left = pygame.image.load('images/back/back_left.png').convert_alpha()
bg_right = pygame.image.load('images/back/back_right.png').convert_alpha()
pygame.display.set_icon(icon)
bg_sound = pygame.mixer.Sound('sounds/back_mus.mp3')
bg_sound.set_volume(0.2)
bg_sound.play()

player = Player(name='Pete')


running = True
debug_mode = False
font = pygame.font.SysFont('Arial', 20)
while running:
    player.update_stats()
    stats = [
        f'Hunger: {int(player.hunger)}',
        f'Happiness: {int(player.happiness)}',
        f'Energy: {int(player.energy)}'
    ]
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
        for i, stat in enumerate(stats):
            t_stat = font.render(stat, True, (255, 255, 255))
            screen.blit(t_stat, (10, 30 + i * 20))
    player.draw(screen, screen.get_width())
    screen.blit(bg_left, (0, 510))
    screen.blit(bg_right, (1136, 612))
    pygame.display.update()

    clock.tick(60)
pygame.quit()



