import random
from cards.card import Card
from themes.theme_manager import ThemeManager

class Board:
    # Construtor
    def __init__(self, width=8, height=6):
        self.width = width
        self.height = height
        self.theme_manager = ThemeManager()
        self.cards = self.create_board()
        self.turns = 0
        self.current_player = 1

    # Função pra definir e embaralhar as cartas
    def create_board(self):
        words = self.theme_manager.get_words()
        all_words = words * 2  # pares
        random.shuffle(all_words)

        card_width = 120
        card_height = 120
        margin_x = 50
        margin_y = 100

        cards = []
        for i, word in enumerate(all_words):
            row = i // self.width
            col = i % self.width
            x = margin_x + col * (card_width + 20)
            y = margin_y + row * (card_height + 20)
            cards.append(Card(word, x, y, card_width, card_height))

        return cards
    
    # Desenha cada carda no tabuleiro
    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)
    
    # Checa se duas cartas tem a mesma palavra
    def check_pair(self, card1, card2):
        return card1.word == card2.word
    
    # Passa pro próximo turno
    def next_turn(self):
        self.turns += 1
        self.current_player = 2 if self.turns % 2 == 0 else 1

    def get_current_player(self):
        return self.current_player

    def set_theme(self, theme):
        self.theme_manager.set_theme(theme)
        self.cards = self.create_board()
        self.turns = 0
        self.current_player = 1
