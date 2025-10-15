import asyncio
import websockets
import pygame
import tkinter as tk
from tkinter import simpledialog
import sys
from game_logic.network_game import NetworkGame
from protocol import *

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

class NetworkGameClient:
    def __init__(self, screen):
        self.screen = screen
        self.network_game = None
        self.running = True
        self.current_state = "CONNECTING"  # CONNECTING, PLAYING, DISCONNECTED
        self.host = 'localhost'
        self.port = 8765
        self.player_name = ""
        
    async def connect_to_server(self, host, port, player_name):
        """Conecta ao servidor e inicia o jogo"""
        self.host = host
        self.port = port
        self.player_name = player_name
        
        log_info(f"Tentando conectar ao servidor em {host}:{port}...")
        log_info(f"Nome do jogador: {player_name}")
        
        # Cria a instância do NetworkGame
        self.network_game = NetworkGame(self.screen, host, port)
        
        # Conecta ao servidor
        if await self.network_game.connect(player_name):
            log_success("Conectado ao servidor com sucesso!")
            self.current_state = "PLAYING"
            return True
        else:
            log_error("Falha ao conectar ao servidor")
            self.current_state = "DISCONNECTED"
            return False
    
    async def run(self):
        """Loop principal do cliente"""
        # Inicia o processamento de mensagens
        if self.network_game:
            asyncio.create_task(self.network_game.process_messages())
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_state == "PLAYING" and self.network_game:
                        self.network_game.handle_click(event.pos)
            
            # Desenha o jogo
            if self.network_game:
                self.network_game.draw()
            
            pygame.display.flip()
            await asyncio.sleep(0.016)  # ~60 FPS
        
        # Desconecta do servidor
        if self.network_game:
            await self.network_game.disconnect()

def get_connection_info():
    """Solicita informações de conexão do usuário"""
    root = tk.Tk()
    root.withdraw()
    
    # Solicita IP do servidor
    host = simpledialog.askstring("IP do Servidor", "Digite o IP do servidor:", initialvalue="localhost")
    if not host:
        return None, None, None
    
    # Solicita porta do servidor
    port_str = simpledialog.askstring("Porta do Servidor", "Digite a porta do servidor:", initialvalue="8765")
    if not port_str:
        return None, None, None
    
    try:
        port = int(port_str)
    except ValueError:
        return None, None, None
    
    # Solicita nome do jogador
    player_name = simpledialog.askstring("Nome do Jogador", "Digite seu nome:", initialvalue="Jogador1")
    if not player_name:
        return None, None, None
    
    root.destroy()
    return host, port, player_name

async def main():
    """Função principal"""
    pygame.init()
    screen = pygame.display.set_mode((1200, 950))
    pygame.display.set_caption("Jogo da Memória - Cliente GUI")
    
    # Solicita informações de conexão
    host, port, player_name = get_connection_info()
    if not host or not port or not player_name:
        print("Conexão cancelada pelo usuário.")
        pygame.quit()
        return
    
    # Cria e executa o cliente
    client = NetworkGameClient(screen)
    
    try:
        if await client.connect_to_server(host, port, player_name):
            await client.run()
        else:
            print("Falha ao conectar ao servidor.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente encerrado.")
