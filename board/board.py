import random
from cards.card import Card

class Board:
    # Construtor
    def __init__(self, width=6, height=8):
        self.width = width
        self.height = height
        self.cards = self.create_board()
        self.turns = 0
        self.current_player = 1

    # Função pra definir e embaralhar as cartas
    def create_board(self):
        words = [
            "Metallica",           # 1
            "Iron Maiden",         # 2
            "Black Sabbath",       # 3
            "Slipknot",            # 4
            "Tool",                # 5
            "Nirvana",             # 6
            "Korn",                # 7
            "Pantera",             # 8
            "Deftones",            # 9
            "Megadeth",            #10
            "Radiohead",           #11
            "A7X",                 #12
            "Pink Floyd",          #13
            "Led Zeppelin",        #14
            "Alice In Chains",     #15
            "Gojira",              #16
            "Opeth",               #17
            "Trivium",             #18
            "Queen",               #19
            "Limp Bizkit",         #20
            "Slayer",              #21
            "The Beatles",         #22
            "The Smiths",          #23
            "The Cure"             #24 
        ]

        # Calculando o tamanho e posição das cartas para melhor distribuição
        card_width = 120
        card_height = 120
        margin_x = 50
        margin_y = 100
        cards = []
        
        for i, word in enumerate(words * 2):
            row = i // 8
            col = i % 8
            x = margin_x + col * (card_width + 20)  # 20 pixels de espaçamento entre cartas
            y = margin_y + row * (card_height + 20)
            cards.append(Card(word, x, y, card_width, card_height))
            
        random.shuffle(cards)
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
