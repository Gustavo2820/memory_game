import pygame
from board.board import Board

class Game:
    def __init__(self, surface):
        self.board = Board()
        self.surface = surface
        self.score = {1: 0, 2: 0}
        self.flipped_cards = []
        self.waiting_time = 0
        self.game_over = False
        self.winner = None
        self.message = ""
        self.message_time = 0
        self.waiting = False

    def check_pair(self):
        card1, card2 = self.flipped_cards
        if self.board.check_pair(card1, card2):
            self.score[self.board.current_player] += 1
            card1.matched = card2.matched = True
            self.message = f"Par encontrado! +1 ponto para o Jogador {self.board.current_player}"
            if self.check_game_over():
                self.game_over = True
                self.winner = 1 if self.score[1] > self.score[2] else 2
        else:
            self.waiting = True
            self.waiting_time = pygame.time.get_ticks() + 1000
            self.message = "Par errado! Próximo jogador"
            self.board.next_turn()
        self.message_time = pygame.time.get_ticks() + 2000
        self.flipped_cards.clear()

    def handle_event(self, event):
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()
        
        # Atualiza o estado de espera
        if self.waiting and current_time > self.waiting_time:
            self.waiting = False
            for card in self.board.cards:
                if card.revealed and not card.matched:
                    card.flip()

        if event.type == pygame.MOUSEBUTTONDOWN and not self.waiting:
            pos = pygame.mouse.get_pos()
            for card in self.board.cards:
                if card.is_clicked(pos) and not card.revealed and not card.matched:
                    card.flip()
                    self.flipped_cards.append(card)
                    if len(self.flipped_cards) == 2:
                        self.check_pair()

    def update(self):
        pass

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        current_player = self.board.get_current_player()
        
        # Desenha o placar
        score_text = f"Jogador 1: {self.score[1]}  Jogador 2: {self.score[2]}"
        text = font.render(score_text, True, (255, 255, 255))
        self.surface.blit(text, (10, 10))
        
        # Desenha o jogador atual
        player_text = f"Jogador Atual: {current_player}"
        player_surface = font.render(player_text, True, (255, 255, 0))
        self.surface.blit(player_surface, (10, 50))

        # Desenha mensagem temporária
        if pygame.time.get_ticks() < self.message_time and self.message:
            message_surface = font.render(self.message, True, (0, 255, 0))
            text_rect = message_surface.get_rect(center=(600, 50))
            self.surface.blit(message_surface, text_rect)

        # Desenha indicador de espera
        if self.waiting:
            wait_text = "Aguarde..."
            wait_surface = font.render(wait_text, True, (255, 0, 0))
            text_rect = wait_surface.get_rect(center=(600, 80))
            self.surface.blit(wait_surface, text_rect)

        # Se o jogo acabou, mostra o vencedor
        if self.game_over:
            winner_text = f"Fim de Jogo! Jogador {self.winner} venceu!"
            winner_surface = font.render(winner_text, True, (0, 255, 0))
            text_rect = winner_surface.get_rect(center=(600, 400))
            self.surface.blit(winner_surface, text_rect)

    def draw(self):
        self.board.draw(self.surface)
        self.draw_score()
    
    def check_game_over(self):
        return all(card.matched for card in self.board.cards)
