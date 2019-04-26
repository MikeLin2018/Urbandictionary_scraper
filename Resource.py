import re
import html

import bs4


class Word:
    def __init__(self, term):
        self.word = term
        self.meanings = []

    def add_meaning(self, meaning):
        self.meanings.append(meaning)

    def report(self):
        meanings_list = []
        for meaning in self.meanings:
            meanings_list.append([self.word, meaning.word_alias, meaning.meaning, meaning.example, meaning.good,
                                  meaning.bad] + meaning.tags)
        return meanings_list


class Meaning:
    def __init__(self):
        self.meaning = ""
        self.word_alias = ""
        self.tags = []
        self.example = ""
        self.good = 0
        self.bad = 0

    def parse(self, definition, term):
        self.parse_alias(definition, term)
        self.parse_meaning(definition)
        self.parse_example(definition)
        self.parse_tags(definition)
        self.parse_rating(definition)

    def parse_alias(self, definition, term):
        possible_alias = definition.find('div', {"class", "def-header"}).find(class_="word").text
        if term != possible_alias:
            self.word_alias = possible_alias

    def parse_meaning(self, definition):
        self.meaning = Helper.get_text_from_tag(definition.find('div', {"class", "meaning"}))

    def parse_example(self, definition):
        self.example = Helper.get_text_from_tag(definition.find('div', {"class", "example"}))

    def parse_tags(self, definition):
        tags_str = Helper.get_text_from_tag(definition.find('div', {"class", "tags"}))
        tags = re.split("#+", tags_str)
        self.tags = list(filter(None, tags))

    def parse_rating(self, definition):
        good = Helper.get_text_from_tag(definition.find('a', {"class", "up"}).find('span', {"class", "count"}))
        bad = Helper.get_text_from_tag(definition.find('a', {"class", "down"}).find('span', {"class", "count"}))
        self.good = int(good)
        self.bad = int(bad)


class Helper:
    @staticmethod
    def get_text_from_tag(tag):
        if tag is None:
            return ""
        contents = tag.contents
        result = ""
        for content in contents:
            if isinstance(content, bs4.element.NavigableString):
                result += " " + content.strip() + " "
            elif isinstance(content, bs4.element.Tag):
                result += " " + content.text.strip() + " "
        # Beautifulsoup4 bug fix
        result = html.unescape(result.replace("&apos", "&apos;"))
        # Clean text
        result = re.sub(" +", " ", result).strip()
        return result
