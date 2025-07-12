# protocol.py - Funções auxiliares para o protocolo AnzolNet v1.0

def parse_message(msg):
    """Recebe uma string, retorna (comando, argumentos)"""
    msg = msg.strip()
    if not msg:
        return None, []
    parts = msg.split()
    cmd = parts[0].upper()
    args = parts[1:]
    return cmd, args


def format_join(nome):
    return f"JOIN {nome}\n"

def format_reveal(x, y):
    return f"REVEAL {x},{y}\n"

def format_quit():
    return "QUIT\n"

def format_start():
    return "START\n"

def format_flip(x, y, imagem):
    return f"FLIP {x},{y},{imagem}\n"

def format_match(x1, y1, x2, y2):
    return f"MATCH {x1},{y1} {x2},{y2}\n"

def format_miss(x1, y1, x2, y2):
    return f"MISS {x1},{y1} {x2},{y2}\n"

def format_turn(nome):
    return f"TURN {nome}\n"

def format_score(nome):
    return f"SCORE {nome}\n"

def format_win(nome):
    return f"WIN {nome}\n"

def format_error(motivo):
    return f"ERROR {motivo}\n"

def format_disconnect(nome):
    return f"DISCONNECT {nome}\n" 