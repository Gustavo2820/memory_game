# Jogo da Memória

Um jogo da memória desenvolvido em Python com interface gráfica usando Pygame e modo online via terminal utilizando WebSockets e o protocolo AnzolNet v1.1. O jogo permite escolher entre diferentes temas e jogar localmente ou em rede.

## Autores

- Gustavo Oliveira Longuinho
- Cauan Luca Navarro Araújo Oliveira
- Gabriel Henrique Policarpo Santos

## Requisitos

- Python 3.x
- Pygame 2.x
- websockets >= 10.0

## Ferramentas Utilizadas
- **Python**: Linguagem de programação principal
- **Pygame**: Biblioteca para desenvolvimento de jogos 2D
- **websockets**: Biblioteca para comunicação WebSocket no modo online
- **Tkinter**: Biblioteca para diálogos de entrada no menu (GUI)
- **Git**: Controle de versão
- **VS Code**: Ambiente de desenvolvimento

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Gustavo2820/memory_game
cd memory_game
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Jogar

### Modo Local (GUI)
1. Execute o jogo:
```bash
python main.py
```
2. No menu inicial:
   - Use o mouse para navegar entre as opções
   - Clique em "Jogar Local" para iniciar uma partida
   - Clique em "Escolher Tema" para selecionar um tema diferente
   - Clique em "Sair" para encerrar o jogo

3. Durante o jogo:
   - Clique nas cartas para revelá-las
   - Encontre os pares de cartas
   - Pressione ESC para voltar ao menu principal
   - O jogo termina quando todos os pares forem encontrados

### Modo Online (Terminal)
1. Inicie o servidor:
```bash
python server.py [IP] [PORTA] [TEMA]
# Exemplo: python server.py 0.0.0.0 8765 Rock
```
2. No menu do jogo, escolha "Jogar em Rede" > "Terminal". Informe o IP e a porta do servidor.
3. O cliente de terminal será aberto. Siga as instruções na tela.

## Temas Disponíveis
- **Rock**: Bandas de rock
- **Anime**: Séries de anime
- **Games**: Jogos populares

## Funcionalidades Implementadas
- Menu inicial interativo com mouse
- Seleção de temas
- Sistema de turnos para dois jogadores
- Placar de pontuação
- Feedback visual das cartas
- Botão de reiniciar após o fim do jogo
- Diferentes temas com palavras específicas
- Interface gráfica responsiva
- **Modo online via terminal** com protocolo customizado
- Escolha de IP e porta ao conectar como cliente
- Comando BOARD automático a cada rodada
- Exibição das cartas reveladas na jogada anterior
- Limpeza automática do terminal a cada rodada
- Log detalhado no servidor
- Reset automático do estado do servidor após cada partida

## Protocolo AnzolNet v1.1
A comunicação entre cliente e servidor ocorre via WebSockets, utilizando mensagens de texto simples, campos separados por espaço e finalizadas com `\n`.

### Comandos do Protocolo AnzolNet v1.1

| Comando                | Origem    | Descrição                                                                 |
|------------------------|-----------|---------------------------------------------------------------------------|
| JOIN nome              | Cliente   | Solicita entrada no jogo, informando o nome do jogador                    |
| START                  | Servidor  | Indica que o jogo começou                                                 |
| REVEAL x,y             | Cliente   | Solicita ao servidor que revele a carta na posição (linha,coluna)         |
| FLIP x,y,palavra       | Servidor  | Informa que a carta na posição (x,y) foi virada, revelando a palavra      |
| MATCH x1,y1 x2,y2      | Servidor  | As duas cartas nas posições indicadas formam um par                       |
| MISS x1,y1 x2,y2       | Servidor  | As duas cartas nas posições indicadas não formam um par                   |
| TURN nome              | Servidor  | Indica de quem é o turno atual                                            |
| SCORE nome             | Servidor  | Incrementa a pontuação do jogador informado                               |
| WIN nome               | Servidor  | Informa quem venceu o jogo                                                |
| ERROR motivo           | Servidor  | Mensagem de erro explicando o motivo                                      |
| DISCONNECT nome        | Servidor  | Indica que o jogador foi desconectado                                     |
| INFO texto             | Servidor  | Mensagem informativa (tema, limites, feedback, etc)                       |
| CLEAR                  | Servidor  | Solicita ao cliente que limpe o terminal e aguarde a próxima rodada       |
| QUIT                   | Cliente   | Encerra a conexão e sai do jogo                                           |

#### Exemplos de uso dos comandos

```
> JOIN Pedro
< START
> REVEAL 2,3
< FLIP 2,3,Iron Maiden
> REVEAL 4,4
< FLIP 4,4,Iron Maiden
< MATCH 2,3 4,4
< SCORE Pedro
< INFO Par encontrado! Pedro ganhou 1 ponto.
< TURN Pedro
< CLEAR
< INFO Estado atual do tabuleiro: ...
> QUIT
< DISCONNECT Pedro
< INFO Você saiu do jogo.
< WIN Pedro
< ERROR Jogada inválida
```

### Fluxo típico de uma rodada online
1. Ambos os jogadores enviam `JOIN nome`.
2. O servidor envia `START` e mensagens `INFO` com tema e limites do tabuleiro.
3. O servidor envia `TURN nome` para indicar de quem é o turno.
4. O jogador da vez envia `REVEAL x,y` duas vezes (para revelar duas cartas).
5. O servidor envia `FLIP x,y,palavra` para cada carta revelada.
6. O servidor envia `MATCH` ou `MISS`, `SCORE`, `INFO` e `TURN` conforme o resultado.
7. O servidor envia `CLEAR` para ambos os clientes, seguido do estado do tabuleiro, placar e turno.
8. O cliente exibe as cartas reveladas, aguarda 3 segundos, limpa o terminal e mostra o tabuleiro, placar e turno.

### Exemplo de interação (cliente)
```
> JOIN Alice
<- START
<- INFO Bem-vindo, Alice! Aguarde o segundo jogador...
<- TURN Alice
<- INFO É o turno de Alice
> REVEAL 1,1
<- FLIP 1,1,Iron Maiden
> REVEAL 2,2
<- FLIP 2,2,Iron Maiden
<- MATCH 1,1 2,2
<- SCORE Alice 1
<- INFO Par encontrado! Alice ganhou 1 ponto.
<- TURN Alice
<- INFO É o turno de Alice
<- CLEAR
Cartas reveladas:
(1,1) -> Iron Maiden
(2,2) -> Iron Maiden

# (após 3 segundos, terminal limpo)
1   2   3   4   5   6   7   8
1: ✔ | * | * | * | * | * | * | *
2: * | ✔ | * | * | * | * | * | *
3: * | * | * | * | * | * | * | *
4: * | * | * | * | * | * | * | *
5: * | * | * | * | * | * | * | *
6: * | * | * | * | * | * | * | *

Placar:
  Alice: 1

É o turno de: Alice
```


## Estrutura do Projeto
```
memory_game/
├── main.py              # Arquivo principal (GUI e integração)
├── board/              # Lógica do tabuleiro
│   └── board.py
├── cards/              # Implementação das cartas
│   └── card.py
├── game_logic/         # Lógica do jogo local
│   └── game.py
├── themes/             # Gerenciamento de temas
│   └── theme_manager.py
├── ui/                 # Interface do usuário
│   ├── game_ui.py
│   └── menu.py
├── server.py           # Servidor WebSocket (modo terminal)
├── client.py           # Cliente WebSocket (modo terminal)
├── protocol.py         # Funções auxiliares do protocolo AnzolNet
└── README.md
```

## Observações
- O cliente pode ser iniciado em qualquer IP/porta configurados.
- O terminal do cliente é limpo automaticamente a cada rodada para simular a experiência de memória real.
- O log do servidor pode ser visualizado ao encerrar com Ctrl+C.
