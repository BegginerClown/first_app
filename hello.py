import pygame
from player_core.player import Player

clock = pygame.time.Clock()


pygame.init()
screen = pygame.display.set_mode((1376, 768))#, flags=pygame.NOFRAME)
pygame.display.set_caption("Тамагочи")
icon = pygame.image.load('images/icons/icon.png')
bg = pygame.image.load('images/back/back.png')
pygame.display.set_icon(icon)

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
    player.draw(screen, screen.get_width())
    pygame.display.update()

    clock.tick(60)
pygame.quit()



