import re

from URLManager import CharacterURLManager, WordURLManager
from Resource import Word, Meaning


class UrbandictionaryParser:
    @staticmethod
    def parse_word_page(soup, term):
        word = Word(term)
        definitions = soup.find(id="content")
        if definitions is None:
            return word
        definitions = definitions.findAll('div', {"class", "def-panel"})
        for definition in definitions:
            meaning = Meaning()
            meaning.parse(definition, term)
            word.add_meaning(meaning)
        return word

    @staticmethod
    def parse_character_page(soup):
        tags = soup.find(id="columnist")
        if tags is None:
            return []
        tags = tags.findAll('a')
        list = []
        for tag in tags:
            term = tag.text
            href = tag["href"]
            list.append((term, href))
        return list

# manager = WordURLManager(term)
# while True:
#     UrbandictionaryScraper().parse_word_page(manager.get_soup(), term)
#     if not manager.next():
#         break
