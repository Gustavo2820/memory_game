import asyncio
import websockets
import pygame
from protocol import *
from board.board import Board
from themes.theme_manager import ThemeManager

# Cores ANSI para terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

def log_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")

def log_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")

def log_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")

def log_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")

class NetworkGame:
    def __init__(self, surface, host='localhost', port=8765):
        self.surface = surface
        self.host = host
        self.port = port
        self.websocket = None
        self.player_name = None
        self.connected = False
        self.game_started = False
        self.current_turn = None
        self.scores = {}
        self.board = None
        self.revealed_cards = set()
        self.pairs = []
        self.waiting_for_update = False
        self.message = ""
        self.message_time = 0
        self.game_over = False
        self.winner = None
        self.theme_manager = ThemeManager()
        self.board_width = 8
        self.board_height = 6
        self.message_queue = asyncio.Queue()
        self.running = True
        
    async def connect(self, player_name):
        """Conecta ao servidor e envia comando JOIN"""
        try:
            uri = f"ws://{self.host}:{self.port}"
            log_info(f"Conectando ao servidor {uri}...")
            self.websocket = await websockets.connect(uri)
            self.connected = True
            self.player_name = player_name
            
            # Inicia a tarefa de recebimento de mensagens
            asyncio.create_task(self.receive_messages())
            
            # Envia comando JOIN
            await self.websocket.send(format_join(player_name))
            log_success(f"Conectado ao servidor como '{player_name}'")
            return True
        except websockets.exceptions.ConnectionRefused:
            log_error("Falha na conexão: servidor recusou ou firewall bloqueando a porta.")
            return False
        except websockets.exceptions.InvalidURI:
            log_error("Falha na conexão: IP incorreto ou formato de URI inválido.")
            return False
        except websockets.exceptions.WebSocketException as e:
            log_error(f"Falha na conexão: {e}")
            return False
        except Exception as e:
            log_error(f"Erro inesperado ao conectar: {e}")
            return False
    
    async def receive_messages(self):
        """Recebe mensagens do servidor e as coloca na fila"""
        try:
            async for message in self.websocket:
                await self.message_queue.put(message)
        except websockets.exceptions.ConnectionClosed:
            log_warning("Conexão com servidor foi fechada")
        except Exception as e:
            log_error(f"Erro ao receber mensagens: {e}")
        finally:
            self.connected = False
    
    async def process_messages(self):
        """Processa mensagens da fila"""
        while self.running and self.connected:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=0.1)
                self.handle_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")
                break
    
    async def disconnect(self):
        """Desconecta do servidor"""
        self.running = False
        if self.websocket and self.connected:
            try:
                log_info("Desconectando do servidor...")
                await self.websocket.send(format_quit())
                await self.websocket.close()
                log_success("Desconectado do servidor com sucesso")
            except Exception as e:
                log_warning(f"Erro ao desconectar: {e}")
            finally:
                self.connected = False
    
    async def send_reveal(self, x, y):
        """Envia comando REVEAL para o servidor"""
        if self.connected and self.websocket:
            try:
                await self.websocket.send(format_reveal(x, y))
                return True
            except Exception as e:
                print(f"Erro ao enviar REVEAL: {e}")
                return False
        return False
    
    def handle_message(self, message):
        """Processa mensagens recebidas do servidor"""
        message = message.strip()
        
        if message.startswith("INFO"):
            # Processa informações do servidor
            info = message[5:].strip()
            if "Tema do jogo:" in info:
                theme = info.split("Tema do jogo:")[1].strip()
                self.theme_manager.set_theme(theme)
            elif "Tabuleiro:" in info:
                # Extrai dimensões do tabuleiro
                parts = info.split("x")
                if len(parts) == 2:
                    self.board_height = int(parts[0].split()[-1])
                    self.board_width = int(parts[1].split()[0])
            elif "É o turno de" in info:
                self.current_turn = info.split("É o turno de")[1].strip()
            elif "Bem-vindo" in info:
                self.message = info
                self.message_time = pygame.time.get_ticks() + 3000
            elif "Par encontrado" in info:
                self.message = info
                self.message_time = pygame.time.get_ticks() + 2000
            elif "Não foi par" in info:
                self.message = info
                self.message_time = pygame.time.get_ticks() + 2000
            elif "Fim de jogo" in info:
                self.game_over = True
                self.winner = info.split("!")[1].strip() if "!" in info else "Desconhecido"
                self.message = info
                self.message_time = pygame.time.get_ticks() + 5000
                
        elif message == "START":
            self.game_started = True
            self.message = "Jogo iniciado! Aguarde o segundo jogador..."
            self.message_time = pygame.time.get_ticks() + 3000
            # Cria o tabuleiro quando o jogo começar
            self.board = Board(self.board_width, self.board_height)
            self.board.theme_manager = self.theme_manager
            self.board.cards = self.board.create_board()
            
        elif message.startswith("TURN"):
            self.current_turn = message.split()[1]
            
        elif message.startswith("FLIP"):
            # Processa carta revelada
            parts = message.split()
            if len(parts) >= 2:
                coords = parts[1].split(",")
                if len(coords) == 3:
                    x, y, word = int(coords[0]), int(coords[1]), coords[2]
                    self.pairs.append((x-1, y-1, word))  # Converte para 0-based
                    
        elif message.startswith("MATCH"):
            # Processa par encontrado
            parts = message.split()
            if len(parts) >= 3:
                coords1 = parts[1].split(",")
                coords2 = parts[2].split(",")
                if len(coords1) == 2 and len(coords2) == 2:
                    x1, y1 = int(coords1[0])-1, int(coords1[1])-1
                    x2, y2 = int(coords2[0])-1, int(coords2[1])-1
                    self.revealed_cards.add((x1, y1))
                    self.revealed_cards.add((x2, y2))
                    self.pairs = []
                    
        elif message.startswith("MISS"):
            # Processa par errado
            self.pairs = []
            
        elif message.startswith("SCORE"):
            # Processa pontuação
            player = message.split()[1]
            if player in self.scores:
                self.scores[player] += 1
            else:
                self.scores[player] = 1
                
        elif message.startswith("WIN"):
            # Processa vitória
            self.winner = message.split()[1]
            self.game_over = True
            
        elif message == "CLEAR":
            self.waiting_for_update = True
            
        elif message.startswith("ERROR"):
            error_msg = message[6:]
            self.message = f"Erro: {error_msg}"
            self.message_time = pygame.time.get_ticks() + 3000
    
    def update_board_state(self):
        """Atualiza o estado das cartas baseado nas mensagens do servidor"""
        if not self.board:
            return
        
        # Atualiza estado das cartas baseado no que foi revelado
        for i, card in enumerate(self.board.cards):
            row = i // self.board_width
            col = i % self.board_width
            
            # Verifica se a carta foi revelada permanentemente
            if (row, col) in self.revealed_cards:
                card.revealed = True
                card.matched = True
            else:
                # Verifica se está nas cartas temporariamente reveladas
                card.revealed = False
                card.matched = False
                for x, y, word in self.pairs:
                    if x == row and y == col:
                        card.revealed = True
                        break
    
    def handle_click(self, pos):
        """Processa clique do mouse"""
        if not self.game_started or self.game_over or not self.connected:
            return
            
        if self.current_turn != self.player_name:
            self.message = "Não é seu turno!"
            self.message_time = pygame.time.get_ticks() + 2000
            return
            
        if not self.board:
            return
            
        # Verifica se clicou em uma carta
        for i, card in enumerate(self.board.cards):
            if card.is_clicked(pos) and not card.revealed and not card.matched:
                row = i // self.board_width
                col = i % self.board_width
                
                # Adiciona o comando REVEAL à fila de envio
                asyncio.create_task(self.send_reveal(row + 1, col + 1))
                break
    
    def draw(self):
        """Desenha o jogo"""
        self.surface.fill((30, 30, 30))
        
        if not self.connected:
            # Mostra mensagem de conexão
            font = pygame.font.Font(None, 48)
            text = font.render("Conectando...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600, 300))
            self.surface.blit(text, text_rect)
            return
            
        if not self.game_started:
            # Mostra mensagem de espera
            font = pygame.font.Font(None, 36)
            text = font.render("Aguardando segundo jogador...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600, 300))
            self.surface.blit(text, text_rect)
            return
            
        # Atualiza o estado do tabuleiro
        self.update_board_state()
        
        if self.board:
            self.board.draw(self.surface)
        
        # Desenha informações do jogo
        self.draw_game_info()
    
    def draw_game_info(self):
        """Desenha informações do jogo (placar, turno, mensagens)"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Desenha o placar
        if self.scores:
            score_text = " | ".join([f"{player}: {score}" for player, score in self.scores.items()])
            text = font.render(score_text, True, (255, 255, 255))
            self.surface.blit(text, (10, 10))
        
        # Desenha o jogador atual
        if self.current_turn:
            player_text = f"Turno: {self.current_turn}"
            player_surface = font.render(player_text, True, (255, 255, 0))
            self.surface.blit(player_surface, (10, 50))
        
        # Desenha mensagem temporária
        if pygame.time.get_ticks() < self.message_time and self.message:
            message_surface = font.render(self.message, True, (0, 255, 0))
            text_rect = message_surface.get_rect(center=(600, 50))
            self.surface.blit(message_surface, text_rect)
        
        # Se o jogo acabou, mostra o vencedor
        if self.game_over:
            winner_text = f"Fim de Jogo! {self.winner} venceu!"
            winner_surface = font.render(winner_text, True, (255, 255, 0))
            text_rect = winner_surface.get_rect(center=(600, 400))
            self.surface.blit(winner_surface, text_rect)
            
            # Botão para voltar ao menu
            back_button = pygame.Rect(500, 450, 200, 50)
            pygame.draw.rect(self.surface, (0, 100, 200), back_button)
            pygame.draw.rect(self.surface, (0, 255, 0), back_button, 2)
            
            back_text = "Voltar ao Menu"
            back_surface = font.render(back_text, True, (255, 255, 255))
            text_rect = back_surface.get_rect(center=back_button.center)
            self.surface.blit(back_surface, text_rect)
