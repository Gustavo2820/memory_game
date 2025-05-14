class ThemeManager:
    def __init__(self):
        self.themes = {
            "Rock": [
                "Metallica", "Iron Maiden", "Black Sabbath", "Slipknot",
                "Tool", "Nirvana", "Korn", "Pantera", "Deftones", "Megadeth",
                "Radiohead", "A7X", "Pink Floyd", "Led Zeppelin", "Alice In Chains",
                "Gojira", "The Smiths", "The Cure", "Queen", "Limp Bizkit",
                "Rammstein", "Guns N' Roses", "S.O.A.D", "Red Hot"
            ],
            "Anime": [
                "Naruto", "Goku", "Luffy", "Ichigo", "Eren", "Mikasa",
                "Levi", "Edward", "Light", "L", "Gon", "Killua",
                "Saitama", "Gintoki", "Spike", "Vash", "Alucard", "Guts",
                "Monkey D. Dragon", "Vegeta", "Sasuke", "Zoro", "Kakashi", "All Might"
            ],
            "Games": [
                "Zelda", "Super Mario", "God of War", "Halo",
                "TLOU", "Red Dead", "GTA", "Minecraft",
                "Fortnite", "Elden Ring", "Outer Wilds", "Hollow Knight",
                "Counter-Strike", "Persona", "The Witcher", "Fallout",
                "Cyberpunk 2077", "Resident Evil", "Silent Hill", "Dark Souls",
                "Sekiro", "Final Fantasy", "Bloodborne", "DMC"
            ]

        }
        self.current_theme = "Rock"

    def get_words(self):
        return self.themes[self.current_theme]

    def set_theme(self, theme):
        if theme in self.themes:
            self.current_theme = theme
            return True
        return False

    def get_available_themes(self):
        return list(self.themes.keys()) 