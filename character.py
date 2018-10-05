

class Character:

    def __init__(self, char_class, char_race):
        self.char_class = char_class
        self.char_race = char_race

        # initial char mods
        self.communcation = 0
        self.reputation = 0
        self.skill = 0
        self.knowledge = 0
        self.responsibility = 0
        self.connections = 0

    def get_class_mods(self):
        pass

    def get_race_mods(self):
        pass

    def get_random_mods(self, class_mods, race_mods):
        pass

    def get_character_mods(self):
        pass

    def print_char(self):
        pass