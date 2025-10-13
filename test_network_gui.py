#!/usr/bin/env python3
"""
Script de teste para o cliente GUI em rede
Este script demonstra como usar o cliente GUI para conectar ao servidor
"""

import asyncio
import pygame
import sys
from client_gui import NetworkGameClient, get_connection_info

async def test_client():
    """Testa o cliente GUI"""
    print("=== Teste do Cliente GUI em Rede ===")
    print("Este script irá abrir uma janela para testar o cliente GUI")
    print("Certifique-se de que o servidor está rodando antes de continuar")
    print()
    
    # Solicita informações de conexão
    host, port, player_name = get_connection_info()
    if not host or not port or not player_name:
        print("Teste cancelado pelo usuário.")
        return
    
    print(f"Conectando ao servidor {host}:{port} como {player_name}...")
    
    # Inicializa pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 950))
    pygame.display.set_caption("Teste - Jogo da Memória - Cliente GUI")
    
    # Cria e executa o cliente
    client = NetworkGameClient(screen)
    
    try:
        if await client.connect_to_server(host, port, player_name):
            print("Conectado com sucesso! Iniciando jogo...")
            await client.run()
        else:
            print("Falha ao conectar ao servidor.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        pygame.quit()
        print("Teste finalizado.")

if __name__ == "__main__":
    try:
        asyncio.run(test_client())
    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
