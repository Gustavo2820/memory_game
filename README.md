from ui.game_ui import GameUI
from game_logic.game import Game
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    game = Game(screen)
    ui = GameUI(game)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        ui.draw()

    pygame.quit()

if __name__ == "__main__":
    main()
