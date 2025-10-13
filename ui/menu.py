import pygame
from themes.theme_manager import ThemeManager

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.theme_manager = ThemeManager()
        self.selected_option = 0
        self.selected_theme = 0
        self.in_theme_selection = False
        self.in_network_menu = False
        self.selected_network = 0
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Cores
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 100, 200)
        self.GREEN = (0, 255, 0)
        
        # Opções do menu
        self.options = ["Jogar Local", "Jogar em Rede", "Escolher Tema", "Sair"]
        self.network_options = ["Terminal", "GUI", "Voltar"]
        self.themes = self.theme_manager.get_available_themes()
        
        # Retângulos para interação com o mouse
        self.option_rects = []
        self.theme_rects = []
        self.network_rects = []
        self.back_rect = None

    def draw(self):
        self.surface.fill((30, 30, 30))
        
        # Título
        title = self.font.render("Jogo da Memória", True, self.YELLOW)
        title_rect = title.get_rect(center=(600, 100))
        self.surface.blit(title, title_rect)

        if self.in_network_menu:
            self.network_rects = []
            for i, option in enumerate(self.network_options):
                text = self.font.render(option, True, self.WHITE)
                rect = text.get_rect(center=(600, 250 + i * 60))
                self.network_rects.append(rect)
                if i == self.selected_network:
                    pygame.draw.rect(self.surface, self.BLUE, rect.inflate(20, 10))
                    text = self.font.render(option, True, self.YELLOW)
                self.surface.blit(text, rect)
        elif not self.in_theme_selection:
            # Desenha as opções do menu principal
            self.option_rects = []
            for i, option in enumerate(self.options):
                text = self.font.render(option, True, self.WHITE)
                rect = text.get_rect(center=(600, 250 + i * 60))
                self.option_rects.append(rect)
                if i == self.selected_option:
                    pygame.draw.rect(self.surface, self.BLUE, rect.inflate(20, 10))
                    text = self.font.render(option, True, self.YELLOW)
                self.surface.blit(text, rect)
        else:
            # Desenha a seleção de temas
            theme_title = self.font.render("Escolha um Tema", True, self.YELLOW)
            theme_title_rect = theme_title.get_rect(center=(600, 200))
            self.surface.blit(theme_title, theme_title_rect)
            self.theme_rects = []
            for i, theme in enumerate(self.themes):
                text = self.font.render(theme, True, self.WHITE)
                rect = text.get_rect(center=(600, 300 + i * 60))
                self.theme_rects.append(rect)
                if i == self.selected_theme:
                    pygame.draw.rect(self.surface, self.BLUE, rect.inflate(20, 10))
                    text = self.font.render(theme, True, self.YELLOW)
                self.surface.blit(text, rect)
            back_text = self.small_font.render("Voltar (ESC)", True, self.WHITE)
            self.back_rect = back_text.get_rect(center=(600, 500))
            pygame.draw.rect(self.surface, self.BLUE, self.back_rect.inflate(20, 10))
            self.surface.blit(back_text, self.back_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.in_network_menu:
                for i, rect in enumerate(self.network_rects):
                    if rect.collidepoint(pos):
                        if self.network_options[i].startswith("Terminal"):
                            return "PLAY_NETWORK_TERMINAL"
                        elif self.network_options[i].startswith("GUI"):
                            return "PLAY_NETWORK_GUI"
                        elif self.network_options[i] == "Voltar":
                            self.in_network_menu = False
            elif not self.in_theme_selection:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        if self.options[i] == "Escolher Tema":
                            self.in_theme_selection = True
                            self.selected_theme = 0
                        elif self.options[i] == "Sair":
                            return "QUIT"
                        elif self.options[i] == "Jogar Local":
                            return "PLAY_LOCAL"
                        elif self.options[i] == "Jogar em Rede":
                            self.in_network_menu = True
                            self.selected_network = 0
            else:
                for i, rect in enumerate(self.theme_rects):
                    if rect.collidepoint(pos):
                        self.theme_manager.set_theme(self.themes[i])
                        self.in_theme_selection = False
                        return "THEME_CHANGED"
                if self.back_rect and self.back_rect.collidepoint(pos):
                    self.in_theme_selection = False
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if self.in_network_menu:
                for i, rect in enumerate(self.network_rects):
                    if rect.collidepoint(pos):
                        self.selected_network = i
            elif not self.in_theme_selection:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        self.selected_option = i
            else:
                for i, rect in enumerate(self.theme_rects):
                    if rect.collidepoint(pos):
                        self.selected_theme = i
        elif event.type == pygame.KEYDOWN:
            if self.in_network_menu:
                if event.key == pygame.K_UP:
                    self.selected_network = (self.selected_network - 1) % len(self.network_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_network = (self.selected_network + 1) % len(self.network_options)
                elif event.key == pygame.K_RETURN:
                    if self.network_options[self.selected_network].startswith("Terminal"):
                        return "PLAY_NETWORK_TERMINAL"
                    elif self.network_options[self.selected_network].startswith("GUI"):
                        return "PLAY_NETWORK_GUI"
                    elif self.network_options[self.selected_network] == "Voltar":
                        self.in_network_menu = False
            elif not self.in_theme_selection:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected_option] == "Escolher Tema":
                        self.in_theme_selection = True
                        self.selected_theme = 0
                    elif self.options[self.selected_option] == "Sair":
                        return "QUIT"
                    elif self.options[self.selected_option] == "Jogar Local":
                        return "PLAY_LOCAL"
                    elif self.options[self.selected_option] == "Jogar em Rede":
                        self.in_network_menu = True
                        self.selected_network = 0
            else:
                if event.key == pygame.K_UP:
                    self.selected_theme = (self.selected_theme - 1) % len(self.themes)
                elif event.key == pygame.K_DOWN:
                    self.selected_theme = (self.selected_theme + 1) % len(self.themes)
                elif event.key == pygame.K_RETURN:
                    self.theme_manager.set_theme(self.themes[self.selected_theme])
                    self.in_theme_selection = False
                    return "THEME_CHANGED"
                elif event.key == pygame.K_ESCAPE:
                    self.in_theme_selection = False
            if event.key == pygame.K_ESCAPE and self.in_network_menu:
                self.in_network_menu = False
        return None

    def get_current_theme(self):
        return self.theme_manager.current_theme 