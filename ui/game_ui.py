import pygame

class GameUI:
    def __init__(self, game):
        self.game = game
        self.screen = game.surface
        pygame.display.set_caption("Jogo da Memória")
        self.font = pygame.font.SysFont("Arial", 24)
        
    def draw(self):
        self.screen.fill((30, 30, 30))
        self.game.draw()
        pygame.display.flip()

    