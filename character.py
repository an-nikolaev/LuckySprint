#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from config import CLASSES_FILE, RACES_FILE


class Character:

    def __init__(self, char_class, char_race):
        # текстовое отображение
        self.char_class = char_class
        self.char_race = char_race

        # внутреннее обозначение
        self.int_class = ""
        self.int_race = ""

        # initial char mods
        self.communication = 0
        self.reputation = 0
        self.skill = 0
        self.knowledge = 0
        self.responsibility = 0
        self.connections = 0

        self.skills = [self.communication, self.reputation, self.skill, self.knowledge,
                       self.responsibility, self.connections]

        self.map_class_race_to_internal()
        self.set_class_mods()
        self.set_race_mods()
        self.set_random_mods()

    def map_class_race_to_internal(self):
        with open(CLASSES_FILE, encoding="utf-8") as jfile:
            classes_json = json.loads(jfile.read())
        with open(RACES_FILE, encoding="utf-8") as jfile:
            races_json = json.loads(jfile.read())
        for item in races_json:
            if races_json[item]["external_name"] == self.char_race:
                self.int_race = item
        for item in classes_json:
            if classes_json[item]["external_name"] == self.char_class:
                self.int_class = item
        if self.int_class == "" or self.int_race == "":
            print("RACE or CLASS stated is unknown. Race, class stated: {}, {}".format(self.char_race, self.char_class))

    def modify_chars(self, json_data, key):
        self.communication += json_data[key]["mods"][0]
        self.reputation += json_data[key]["mods"][1]
        self.skill += json_data[key]["mods"][2]
        self.knowledge += json_data[key]["mods"][3]
        self.responsibility += json_data[key]["mods"][4]
        self.connections += json_data[key]["mods"][5]

    def simple_modify_chars(self, mod_list):
        self.communication += mod_list[0]
        self.reputation += mod_list[1]
        self.skill += mod_list[2]
        self.knowledge += mod_list[3]
        self.responsibility += mod_list[4]
        self.connections += mod_list[5]

    def set_class_mods(self):
        with open(CLASSES_FILE, encoding="utf-8") as jfile:
            classes_json = json.loads(jfile.read())
        self.modify_chars(classes_json, self.int_class)

    def set_race_mods(self):
        with open(RACES_FILE, encoding="utf-8") as jfile:
            races_json = json.loads(jfile.read())
        self.modify_chars(races_json, self.int_race)

    def set_random_mods(self):
        random_mods = [0, 0, 0, 0, 0, 0]
        while sum(random_mods) < 3:
            index = random.randint(0, 5)
            if random_mods[index] == 0:
                random_mods[index] = 1
        self.simple_modify_chars(random_mods)

    def get_character_mods(self):
        return [self.communication, self.reputation, self.skill, self.knowledge, self.responsibility, self.connections]

    def get_char_description(self):
        description = {
            "class": self.char_class,
            "race": self.char_race,
            "communication": self.communication,
            "reputation": self.reputation,
            "skill": self.skill,
            "knowledge": self.knowledge,
            "responsibility": self.responsibility,
            "connections": self.connections
        }
        # print(json.dumps(description))
        return description