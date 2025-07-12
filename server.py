import asyncio
import websockets
import random
from protocol import *
from themes.theme_manager import ThemeManager

async def handler(websocket):
    await MemoryGameServer.instance.handle_connection(websocket)

class MemoryGameServer:
    instance = None
    def __init__(self, host, port, tema_nome=None):
        MemoryGameServer.instance = self
        self.host = host
        self.port = port
        self.clients = []  # [(websocket, nome)]
        self.turn = 0
        self.scores = {}
        self.names = []
        self.board = []
        self.revealed = set()
        self.pairs = []
        self.log = []
        self.state = 'waiting'  # waiting, playing, finished
        self.theme_manager = ThemeManager()
        if tema_nome and tema_nome in self.theme_manager.get_available_themes():
            self.theme_manager.set_theme(tema_nome)
        self.words = self.theme_manager.get_words()
        self.size = 6 if len(self.words) == 24 else 4  # 6x8 para 24 palavras, 4x4 para 8
        self.width = 8 if len(self.words) == 24 else 4
        self.height = 6 if len(self.words) == 24 else 4

    def make_board(self):
        words = self.words
        all_words = words * 2
        random.shuffle(all_words)
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(all_words.pop())
            board.append(row)
        return board

    def reset_state(self):
        self.log.append("[RESET] Reiniciando estado do servidor para nova partida.")
        self.turn = 0
        self.scores = {}
        self.names = []
        self.board = []
        self.revealed = set()
        self.pairs = []
        self.state = 'waiting'

    def board_state_str(self):
        if not self.board:
            return "Tabuleiro ainda não iniciado."
        lines = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (i, j) in self.revealed:
                    row.append("✔")
                else:
                    row.append("*")
            lines.append(f"{i+1}: " + " | ".join(row))
        header = "    " + "   ".join(str(j+1) for j in range(self.width))
        return header + "\n" + "\n".join(lines)

    async def handle_connection(self, websocket):
        nome = None
        try:
            await websocket.send(f"INFO Tema do jogo: {self.theme_manager.current_theme}")
            await websocket.send(f"INFO Tabuleiro: {self.height}x{self.width} cartas")
            await websocket.send(f"INFO Linhas válidas: 1 a {self.height}, Colunas válidas: 1 a {self.width}")
            async for msg in websocket:
                self.log.append(f"RECV {msg.strip()}")
                cmd, args = parse_message(msg)
                self.log.append(f"[STATE] Estado atual: {self.state}")
                if cmd == 'JOIN' and len(args) == 1 and self.state == 'waiting':
                    nome = args[0]
                    if len(self.clients) >= 2:
                        await websocket.send(format_error("Sala cheia"))
                        self.log.append(f"[ERROR] Sala cheia para {nome}")
                        continue
                    if any(n == nome for _, n in self.clients):
                        await websocket.send(format_error("Nome em uso"))
                        self.log.append(f"[ERROR] Nome em uso: {nome}")
                        continue
                    self.clients.append((websocket, nome))
                    self.scores[nome] = 0
                    self.names.append(nome)
                    await websocket.send(format_start())
                    await websocket.send(f"INFO Bem-vindo, {nome}! Aguarde o segundo jogador...")
                    await websocket.send(f"INFO Linhas válidas: 1 a {self.height}, Colunas válidas: 1 a {self.width}")
                    self.log.append(f"SEND START para {nome}")
                    self.log.append(f"[JOIN] {nome} entrou no jogo.")
                    if len(self.clients) == 2:
                        self.state = 'playing'
                        self.turn = 0
                        self.board = self.make_board()
                        self.revealed = set()
                        self.pairs = []
                        for ws, n in self.clients:
                            await ws.send(format_turn(self.names[self.turn]))
                            await ws.send(f"INFO É o turno de {self.names[self.turn]}")
                        self.log.append(f"[START] Jogo iniciado com jogadores: {self.names}")
                elif cmd == 'REVEAL' and self.state == 'playing':
                    if nome != self.names[self.turn]:
                        await websocket.send(format_error("Nao e seu turno"))
                        await websocket.send(f"INFO Aguarde o outro jogador.")
                        self.log.append(f"[ERROR] Jogador {nome} tentou jogar fora do turno.")
                        continue
                    if len(args) != 1 or ',' not in args[0]:
                        await websocket.send(format_error("Comando malformado"))
                        self.log.append(f"[ERROR] Comando REVEAL malformado por {nome}")
                        continue
                    try:
                        x, y = map(int, args[0].split(','))
                        x -= 1
                        y -= 1
                    except Exception:
                        await websocket.send(format_error("Coordenadas invalidas"))
                        self.log.append(f"[ERROR] Coordenadas invalidas por {nome}")
                        continue
                    if not (0 <= x < self.height and 0 <= y < self.width):
                        await websocket.send(format_error("Coordenadas fora do tabuleiro"))
                        self.log.append(f"[ERROR] Coordenadas fora do tabuleiro por {nome}")
                        continue
                    if (x, y) in self.revealed:
                        await websocket.send(format_error("Carta ja revelada"))
                        self.log.append(f"[ERROR] Carta já revelada por {nome}")
                        continue
                    imagem = self.board[x][y]
                    for ws, n in self.clients:
                        # Envia coordenadas 1-based
                        await ws.send(format_flip(x+1, y+1, imagem))
                    self.pairs.append((x, y, imagem))
                    self.log.append(f"[REVEAL] {nome} revelou ({x},{y}) = {imagem}")
                    if len(self.pairs) == 2:
                        (x1, y1, img1), (x2, y2, img2) = self.pairs
                        if img1 == img2:
                            self.revealed.add((x1, y1))
                            self.revealed.add((x2, y2))
                            self.scores[nome] += 1
                            for ws, n in self.clients:
                                await ws.send(format_match(x1+1, y1+1, x2+1, y2+1))
                                await ws.send(format_score(nome))
                                await ws.send(f"INFO Par encontrado! {nome} ganhou 1 ponto.")
                            self.log.append(f"[MATCH] {nome} encontrou par: {img1}")
                            if len(self.revealed) == self.width * self.height:
                                for ws, n in self.clients:
                                    await ws.send(format_win(nome))
                                    await ws.send(f"INFO Fim de jogo! {nome} venceu!")
                                self.log.append(f"[END] Jogo finalizado. Vencedor: {nome}")
                                self.reset_state()
                                break
                        else:
                            for ws, n in self.clients:
                                await ws.send(format_miss(x1+1, y1+1, x2+1, y2+1))
                                await ws.send(f"INFO Não foi par. Próximo jogador!")
                            self.log.append(f"[MISS] {nome} não encontrou par: {img1} e {img2}")
                            self.turn = (self.turn + 1) % 2
                        self.pairs = []
                        for ws, n in self.clients:
                            await ws.send(format_turn(self.names[self.turn]))
                            await ws.send(f"INFO É o turno de {self.names[self.turn]}")
                            await ws.send("CLEAR\n")
                            await ws.send(f"INFO Estado atual do tabuleiro:\n{self.board_state_str()}")
                            await ws.send(format_turn(self.names[self.turn]))
                elif cmd == 'BOARD':
                    await websocket.send(f"INFO Estado atual do tabuleiro:\n{self.board_state_str()}")
                    self.log.append(f"[BOARD] Estado do tabuleiro enviado para {nome or 'desconhecido'}.")
                elif cmd == 'QUIT':
                    await websocket.send(format_disconnect(nome or "Desconhecido"))
                    await websocket.send(f"INFO Você saiu do jogo.")
                    self.log.append(f"[QUIT] {nome} saiu do jogo.")
                    break
                else:
                    await websocket.send(format_error("Comando invalido ou fora de contexto"))
                    self.log.append(f"[ERROR] Comando invalido ou fora de contexto por {nome}")
        except Exception as e:
            self.log.append(f"ERRO: {e}")
        finally:
            if nome:
                self.log.append(f"{nome} desconectou.")
            else:
                self.log.append(f"Cliente anonimo desconectou.")
            self.clients = [(ws, n) for ws, n in self.clients if ws != websocket]
            if nome in self.names:
                self.names.remove(nome)
            if nome in self.scores:
                del self.scores[nome]
            for ws, n in self.clients:
                await ws.send(format_disconnect(nome or "Desconhecido"))
                await ws.send(f"INFO O jogador {nome or 'Desconhecido'} saiu do jogo.")
            self.log.append(f"[DISCONNECT] {nome or 'Desconhecido'} removido da partida.")

    def print_log(self):
        print("\n--- LOG DA PARTIDA ---")
        for l in self.log:
            print(l)
        print("---------------------\n")

    def run(self):
        print(f"Servidor ouvindo em ws://{self.host}:{self.port}")
        async def main():
            async with websockets.serve(handler, self.host, self.port):
                await asyncio.Future()  # roda para sempre
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
            self.print_log()

if __name__ == "__main__":
    import sys
    host = 'localhost'
    port = 8765
    tema = None
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    if len(sys.argv) > 3:
        tema = sys.argv[3]
    MemoryGameServer(host, port, tema).run() 