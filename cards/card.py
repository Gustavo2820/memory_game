import pygame

# Classe de carta
class Card:
    # Construtor
    def __init__(self, word, x, y, width=120, height=120):
        self.word = word
        self.rect = pygame.Rect(x, y, width, height)
        self.revealed = False
        self.matched = False
        self.highlight = False
        self.width = width
        self.height = height

    # Vira a carta
    def flip(self):
        self.revealed = not self.revealed

    # Desenhar
    def draw(self, surface):
        # Desenha o fundo da carta
        if self.matched:
            color = (100, 200, 100)  # Verde claro para cartas acertadas
        elif self.revealed:
            color = (150, 150, 200)  # Azul claro para cartas viradas (reveladas)
        else:
            color = (100, 100, 100)  # Cinza escuro para cartas normais
            
        pygame.draw.rect(surface, color, self.rect)
        
        # Desenha a borda
        border_color = (0, 255, 0) if self.matched else (0, 0, 0)
        pygame.draw.rect(surface, border_color, self.rect, 3)

        if self.revealed:
            # Desenha o texto centralizado
            font = pygame.font.Font(None, 32)
            text = font.render(self.word, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        else:
            # Desenha um símbolo de interrogação quando a carta está virada
            font = pygame.font.Font(None, 48)
            text = font.render("?", True, (200, 200, 200))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    # Testa se o mouse ta na carta
    def is_clicked(self, pos):
        self.highlight = self.rect.collidepoint(pos)
        return self.highlight  