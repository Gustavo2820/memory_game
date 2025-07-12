from ui.game_ui import GameUI
from ui.menu import Menu
from game_logic.game import Game
import pygame
import subprocess
import sys
import tkinter as tk
from tkinter import simpledialog

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
                elif result == "PLAY_NETWORK_TERMINAL":
                    pygame.quit()
                    print("Iniciando cliente de terminal...")
                    if sys.platform.startswith('win'):
                        # (pode adaptar para Windows se quiser)
                        subprocess.run(["start", "cmd", "/k", "python", "client.py"], shell=True)
                    else:
                        # Prompt para IP e porta usando tkinter
                        root = tk.Tk()
                        root.withdraw()
                        ip = simpledialog.askstring("IP do Servidor", "Digite o IP do servidor:", initialvalue="localhost")
                        port = simpledialog.askstring("Porta do Servidor", "Digite a porta do servidor:", initialvalue="8765")
                        root.destroy()
                        if not ip or not port:
                            print("Cancelado pelo usuário.")
                            sys.exit(0)
                        # Tenta abrir em diferentes terminais e manter aberto após execução
                        for term in [
                            ["gnome-terminal", "--", "bash", "-c", f"python3 client.py {ip} {port}; exec bash"],
                            ["konsole", "-e", f"bash -c 'python3 client.py {ip} {port}; exec bash'"],
                            ["xfce4-terminal", "-e", f"bash -c 'python3 client.py {ip} {port}; exec bash'"],
                            ["xterm", "-e", f"bash -c 'python3 client.py {ip} {port}; exec bash'"]
                        ]:
                            try:
                                subprocess.run(term, check=True)
                                break
                            except FileNotFoundError:
                                continue
                        else:
                            print("Nenhum terminal suportado encontrado. Execute 'python3 client.py' manualmente.")
                    sys.exit(0)
                elif result == "NETWORK_GUI_SOON":
                    print("Modo GUI em rede estará disponível em breve!")
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
