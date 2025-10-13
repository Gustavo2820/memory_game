# Jogo da Memória - GUI em Rede

Este documento explica como usar a nova funcionalidade de GUI em rede do Jogo da Memória.

## Funcionalidades Implementadas

O jogo agora suporta todas as combinações de interface:

- ✅ **GUI Local** - Jogo local com interface gráfica
- ✅ **GUI em Rede** - Jogo em rede com interface gráfica (NOVO!)
- ✅ **Terminal em Rede** - Jogo em rede via terminal
- ✅ **Terminal com Terminal** - Jogo local via terminal

## Como Usar

### 1. Iniciar o Servidor

```bash
python server.py [host] [port] [tema]
```

Exemplos:
```bash
# Servidor padrão (localhost:8765, tema Rock)
python server.py

# Servidor personalizado
python server.py 192.168.1.100 9000 Games
```

### 2. Conectar com GUI

#### Opção A: Pelo Menu Principal
1. Execute `python main.py`
2. Escolha "Jogar em Rede"
3. Escolha "GUI"
4. Digite as informações de conexão quando solicitado

#### Opção B: Diretamente
```bash
python client_gui.py
```

### 3. Conectar com Terminal (como antes)
```bash
python client.py [host] [port]
```

## Arquivos Modificados/Criados

### Novos Arquivos
- `client_gui.py` - Cliente GUI para rede
- `game_logic/network_game.py` - Lógica do jogo em rede com GUI
- `test_network_gui.py` - Script de teste
- `NETWORK_GUI_README.md` - Este arquivo

### Arquivos Modificados
- `main.py` - Adicionada opção "GUI" no menu de rede
- `ui/menu.py` - Atualizado menu de rede

## Protocolo de Rede

O jogo usa o protocolo AnzolNet v1.0 existente, mantendo total compatibilidade:

- **JOIN nome** - Entrar no jogo
- **REVEAL x,y** - Revelar carta na posição (x,y)
- **QUIT** - Sair do jogo

### Mensagens do Servidor
- **START** - Jogo iniciado
- **TURN nome** - É o turno do jogador
- **FLIP x,y,palavra** - Carta revelada
- **MATCH x1,y1 x2,y2** - Par encontrado
- **MISS x1,y1 x2,y2** - Par errado
- **SCORE nome** - Pontuação atualizada
- **WIN nome** - Jogador venceu
- **ERROR motivo** - Erro ocorreu

## Compatibilidade

- ✅ Mantém toda funcionalidade existente
- ✅ Servidor funciona com GUI e Terminal simultaneamente
- ✅ Clientes podem misturar GUI e Terminal
- ✅ Protocolo inalterado
- ✅ Temas funcionam em todos os modos

## Exemplo de Uso Completo

1. **Terminal 1** (Servidor):
   ```bash
   python server.py localhost 8765 Games
   ```

2. **Terminal 2** (Cliente GUI):
   ```bash
   python client_gui.py
   # Digite: localhost, 8765, Jogador1
   ```

3. **Terminal 3** (Cliente Terminal):
   ```bash
   python client.py localhost 8765
   # Digite: JOIN Jogador2
   ```

4. **Jogar!** - Ambos os clientes podem jogar juntos, um com GUI e outro com terminal.

## Solução de Problemas

### Erro de Conexão
- Verifique se o servidor está rodando
- Confirme o IP e porta corretos
- Verifique se não há firewall bloqueando

### GUI não Responde
- Verifique se o servidor está ativo
- Confirme se o nome do jogador é único
- Verifique os logs do servidor

### Cartas não Aparecem
- Aguarde o segundo jogador conectar
- Verifique se o jogo foi iniciado (mensagem "START")
- Confirme se o tema está correto

## Desenvolvimento

Para modificar ou estender a funcionalidade:

1. **NetworkGame** (`game_logic/network_game.py`) - Lógica principal do jogo em rede
2. **NetworkGameClient** (`client_gui.py`) - Interface do cliente GUI
3. **Menu** (`ui/menu.py`) - Opções do menu principal

A implementação mantém a separação de responsabilidades e é facilmente extensível.
