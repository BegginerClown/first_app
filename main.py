import pygame
from player_core.player import Player
from DB.DB import DB

db = DB('DB/save.db')
#db.create_tables()

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1376, 768))
pygame.display.set_caption("Тамагочи")
icon = pygame.image.load('images/icons/icon.png')
bg = pygame.image.load('images/back/back.png')
bg_left = pygame.image.load('images/back/back_left.png').convert_alpha()
bg_right = pygame.image.load('images/back/back_right.png').convert_alpha()
pygame.display.set_icon(icon)
bg_sound = pygame.mixer.Sound('sounds/back_mus.mp3')
bg_sound.set_volume(0.2)

# --- Переменные для меню ---
game_state = "MENU"
selected_player_name = None
font = pygame.font.SysFont('Arial', 20)
menu_buttons = []
input_text = ""
input_active = False

def load_players():
    global menu_buttons
    all_players = db.get_all_players()
    menu_buttons = []
    for name in all_players:
        menu_buttons.append({"text": name, "action": "load", "name": name})
    menu_buttons.append({"text": "Новый игрок", "action": "new"})

load_players()

def draw_menu():
    # Немного прозрачного фона поверх текущего
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Чёрный с 70% непрозрачностью
    screen.blit(overlay, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i, button in enumerate(menu_buttons):
        # Проверяем, наведена ли мышь
        button_rect = pygame.Rect(50, 50 + i * 50, 300, 40)
        if button_rect.collidepoint(mouse_x, mouse_y):
            color = (100, 100, 200)  # Светло-синий при наведении
        else:
            color = (50, 50, 150)   # Тёмно-синий

        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        text = font.render(button["text"], True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 10, button_rect.y + 10))

    if input_active:
        input_rect = pygame.Rect(50, 50 + len(menu_buttons) * 50, 300, 40)
        pygame.draw.rect(screen, (100, 100, 100), input_rect, border_radius=10)
        input_text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(input_text_surface, (input_rect.x + 10, input_rect.y + 10))

    pygame.display.update()

def handle_menu_events(event):
    global game_state, selected_player_name, input_text, input_active
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, button in enumerate(menu_buttons):
            button_rect = pygame.Rect(50, 50 + i * 50, 300, 40)
            if button_rect.collidepoint(mouse_x, mouse_y):
                if button["action"] == "load":
                    selected_player_name = button["name"]
                    game_state = "PLAYING"
                elif button["action"] == "new":
                    input_active = True
    elif event.type == pygame.KEYDOWN and input_active:
        if event.key == pygame.K_RETURN:
            selected_player_name = input_text
            game_state = "PLAYING"
            input_active = False
        elif event.key == pygame.K_BACKSPACE:
            input_text = input_text[:-1]
        else:
            input_text += event.unicode

# --- Основной цикл ---
running = True
player = None  # Инициализируем позже

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "MENU":
            handle_menu_events(event)

    if game_state == "MENU":
        draw_menu()
    elif game_state == "PLAYING":
        if player is None:
            player = Player(name=selected_player_name)
            bg_sound.play()

        # --- Твой текущий игровой цикл ---
        player.update_stats()
        stats = [
            f'Hunger: {int(player.hunger)}',
            f'Happiness: {int(player.happiness)}',
            f'Energy: {int(player.energy)}'
        ]
        keys = pygame.key.get_pressed()
        player.moving(keys)
        screen.blit(bg, (0, 0))
        bar_width = 150
        bar_height = 20
        bar_x = 10
        bar_start_y = 30

        for i, (stat_name, stat_value, color) in enumerate([
            ("Hunger", player.hunger, (0, 255, 0)),
            ("Happiness", player.happiness, (255, 255, 0)),
            ("Energy", player.energy, (255, 0, 0))
        ]):
            pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_start_y + i * 30, bar_width, bar_height), 2)
            fill_width = int((stat_value / 100) * bar_width)
            pygame.draw.rect(screen, color, (bar_x + 1, bar_start_y + i * 30 + 1, fill_width, bar_height - 2))
            text = font.render(f'{stat_name}', True, (255, 255, 255))
            screen.blit(text, (bar_x + bar_width + 5, bar_start_y + i * 30))

        player.draw(screen, screen.get_width())
        screen.blit(bg_left, (0, 510))
        screen.blit(bg_right, (1136, 612))
        pygame.display.update()

    clock.tick(60)

if player:
    player.save_data()
pygame.quit()