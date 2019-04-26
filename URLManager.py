import string
import requests
from bs4 import BeautifulSoup
import re


class CharacterURLManager:
    def __init__(self, start_character_index=0):
        self.base_URL = "https://www.urbandictionary.com/browse.php"
        self.base_characters = string.ascii_uppercase[:26] + "*"
        self.current_character_index = start_character_index
        self.current_page = 1
        self.current_soup = BeautifulSoup(requests.get(self.get_URL()).content, "html.parser")

    def get_URL(self):
        if self.current_page == 1:
            return self.base_URL + "?character=" + str(self.base_characters[self.current_character_index])
        else:
            return self.base_URL + "?character=" + str(
                self.base_characters[self.current_character_index]) + "&" + "page=" + str(self.current_page)

    def next(self):
        pagination = self.current_soup.find("ul", {"class", "pagination"})
        if re.search('next', pagination.text, re.IGNORECASE):
            self.current_page += 1
            self.update_soup()
            return True
        self.current_page = 1
        self.current_character_index += 1
        if self.current_character_index > 25:
            return False
        else:
            self.update_soup()
            return True

    def get_soup(self):
        return self.current_soup

    def update_soup(self):
        current_URL = self.get_URL()
        current_page_content = requests.get(current_URL).content
        self.current_soup = BeautifulSoup(current_page_content, "html.parser")

    def get_current_character(self):
        return self.base_characters[self.current_character_index]


class WordURLManager:
    def __init__(self, partial_URL):
        self.base_URL = "https://www.urbandictionary.com" + partial_URL
        self.current_page = 1
        self.current_soup = BeautifulSoup(requests.get(self.get_URL()).content, "html.parser")

    def get_URL(self):
        if self.current_page == 1:
            return self.base_URL
        else:
            return self.base_URL + "&page=" + str(self.current_page)

    def next(self):
        pagination = self.current_soup.find("ul", {"class", "pagination"})
        if pagination is None:
            return False
        if re.search('next', pagination.text, re.IGNORECASE):
            self.current_page += 1
            self.update_soup()
            return True
        return False

    def get_soup(self):
        return self.current_soup

    def update_soup(self):
        current_URL = self.get_URL()
        current_page_content = requests.get(current_URL).content
        self.current_soup = BeautifulSoup(current_page_content, "html.parser")
