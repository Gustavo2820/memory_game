import asyncio
import websockets
from protocol import *
import os
import time

async def main(uri):
    async with websockets.connect(uri) as ws:
        print("Conectado ao servidor.")
        print("Digite comandos: JOIN nome | REVEAL x,y | QUIT")
        last_flips = []  # (x, y, palavra)
        scores = {}      # nome: pontos
        current_turn = None
        board_str = None
        jogadores = set()
        waiting_for_update = False
        async def send_input():
            while True:
                try:
                    cmd = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
                    if cmd.strip().upper() == "BOARD":
                        print("Comando BOARD desabilitado. O tabuleiro será mostrado automaticamente a cada rodada.")
                    else:
                        await ws.send(cmd.strip() + "\n")
                except Exception:
                    break
        async def recv_msgs():
            nonlocal last_flips, scores, current_turn, board_str, jogadores, waiting_for_update
            while True:
                msg = await ws.recv()
                m = msg.strip()
                if m == "CLEAR":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    # Mostra as duas últimas cartas reveladas
                    if len(last_flips) == 2:
                        print(f"Cartas reveladas:")
                        for (x, y, palavra) in last_flips:
                            print(f"(   {x},{y}) -> {palavra}")
                        print()
                    else:
                        print("Aguardando jogada...")
                    await asyncio.sleep(3)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    # Espera as próximas mensagens antes de exibir
                    waiting_for_update = True
                    board_str = None
                elif m.startswith("FLIP"):
                    try:
                        _, rest = m.split(None, 1)
                        x, y, palavra = rest.split(",", 2)
                        last_flips.append((x, y, palavra))
                        if len(last_flips) > 2:
                            last_flips = last_flips[-2:]
                    except Exception:
                        pass
                elif m.startswith("SCORE"):
                    try:
                        _, nome = m.split()
                        if nome in scores:
                            scores[nome] += 1
                        else:
                            scores[nome] = 1
                        jogadores.add(nome)
                    except Exception:
                        pass
                elif m.startswith("TURN"):
                    try:
                        _, nome = m.split()
                        current_turn = nome
                    except Exception:
                        pass
                elif m.startswith("INFO Estado atual do tabuleiro:"):
                    board_str = m[len("INFO Estado atual do tabuleiro:"):].strip()
                    if waiting_for_update:
                        if board_str:
                            print(board_str)
                        if scores:
                            print("\nPlacar:")
                            for nome, pontos in scores.items():
                                print(f"  {nome}: {pontos}")
                        if current_turn:
                            print(f"\nÉ o turno de: {current_turn}")
                        print()
                        waiting_for_update = False
                        last_flips = []  # Limpa só depois de exibir o tabuleiro
                else:
                    print(f"<- {m}")
        await asyncio.gather(send_input(), recv_msgs())

if __name__ == "__main__":
    import sys
    host = 'localhost'
    port = 8765
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    uri = f"ws://{host}:{port}"
    try:
        asyncio.run(main(uri))
    except KeyboardInterrupt:
        print("\nCliente encerrado.") 