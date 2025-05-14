# Jogo da Memória

Um jogo da memória desenvolvido em Python com interface gráfica usando Pygame. O jogo permite escolher entre diferentes temas e jogar localmente com dois jogadores.

## Autores

- Gustavo Oliveira Longuinho
- Cauan Luca Navarro Araújo Oliveira
- Gabriel Henrique Policarpo Santos

## Requisitos

- Python 3.x
- Pygame 2.x

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

## Ferramentas Utilizadas

- **Python**: Linguagem de programação principal
- **Pygame**: Biblioteca para desenvolvimento de jogos
- **Git**: Controle de versão
- **VS Code**: Ambiente de desenvolvimento

## Estrutura do Projeto

```
memory_game/
├── main.py              # Arquivo principal
├── board/              # Lógica do tabuleiro
│   └── board.py
├── cards/              # Implementação das cartas
│   └── card.py
├── game_logic/         # Lógica do jogo
│   └── game.py
├── themes/             # Gerenciamento de temas
│   └── theme_manager.py
├── ui/                 # Interface do usuário
│   ├── game_ui.py
│   └── menu.py
└── README.md
```