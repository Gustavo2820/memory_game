from ui.game_ui import GameUI
from ui.menu import Menu
from game_logic.game import Game
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 950))
    pygame.display.set_caption("Jogo da Memória")
    
    menu = Menu(screen)
    game = None
    game_ui = None
    current_state = "MENU"  # Estados possíveis: "MENU", "GAME"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_state == "MENU":
                result = menu.handle_event(event)
                if result == "QUIT":
                    running = False
                elif result == "PLAY_LOCAL":
                    game = Game(screen)
                    game.board.set_theme(menu.get_current_theme())
                    game_ui = GameUI(game)
                    current_state = "GAME"
                elif result == "THEME_CHANGED":
                    if game:
                        game.board.set_theme(menu.get_current_theme())
            elif current_state == "GAME":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = "MENU"
                else:
                    game.handle_event(event)

        if current_state == "MENU":
            menu.draw()
        else:
            game_ui.draw()
            
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
