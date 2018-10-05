import json

from config import CLASSES_FILE, RACES_FILE


class Character:

    def __init__(self, char_class, char_race):
        # текстовое отображение
        self.char_class = char_class
        self.char_race = char_race

        self.int_class = ""
        self.int_race = ""

        # initial char mods
        self.communication = 0
        self.reputation = 0
        self.skill = 0
        self.knowledge = 0
        self.responsibility = 0
        self.connections = 0

    def map_class_race_to_internal(self):
        with open(CLASSES_FILE) as jfile:
            classes_json = json.loads(jfile.read())
        with open(RACES_FILE) as jfile:
            races_json = json.loads(jfile.read())
        for item in races_json:
            if races_json[item]["external_name"] == self.char_race:
                self.int_race = item
            else:
                print("UNKNOWN RACE!!!!")
        for item in races_json:
            if classes_json[item]["external_name"] == self.char_class:
                self.int_class = item
            else:
                print("UNKNOWN CLASS!!!!")

    def modify_chars(self, json_data, key):
        self.communication += json_data[key]["mods"][0]
        self.reputation += json_data[key]["mods"][1]
        self.skill += json_data[key]["mods"][2]
        self.knowledge += json_data[key]["mods"][3]
        self.responsibility += json_data[key]["mods"][4]
        self.connections += json_data[key]["mods"][5]

    def set_class_mods(self):
        with open(CLASSES_FILE) as jfile:
            classes_json = json.loads(jfile.read())
        self.modify_chars(classes_json, self.int_class)

    def set_race_mods(self):
        with open(RACES_FILE) as jfile:
            races_json = json.loads(jfile.read())
        self.modify_chars(races_json, self.int_race)

    def get_character_mods(self):
        return [self.communication, self.reputation, self.skill, self.knowledge, self.responsibility, self.connections]

    def get_char_description(self):
        description = {
        }
        return description