from Parser import UrbandictionaryParser
from URLManager import CharacterURLManager, WordURLManager
import csv


class UrbandictionaryScraper:
    def run(self, start_index=0, end_index=0):
        character_url_manager = CharacterURLManager(start_index)
        previous_character = ""
        while True:
            if previous_character != character_url_manager.get_current_character():
                previous_character = character_url_manager.get_current_character()
                csv_file = open("./data/" + str(character_url_manager.get_current_character()) + ".csv", "w+",
                                newline="")
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(["url", "word", "alias", "meaning", "example", "good", "bad", "tags"])
            # Get a list of terms and partial urls
            list = UrbandictionaryParser.parse_character_page(character_url_manager.get_soup())
            for term, partial_URL in list:
                word_url_manager = WordURLManager(partial_URL)
                while True:
                    word = UrbandictionaryParser.parse_word_page(word_url_manager.get_soup(), term)
                    for meaning_list in word.report():
                        row = [word_url_manager.get_URL()] + meaning_list
                        csv_writer.writerow(row)
                        print("Character:", character_url_manager.get_current_character())
                        print("Character Page:", character_url_manager.current_page)
                        print("Word Page:", word_url_manager.current_page)
                        print("Term:", term)
                        print("Row:", row)
                        print()
                    if not word_url_manager.next():
                        break
            if not character_url_manager.next():
                break
            if character_url_manager.current_character_index > end_index:
                break


if __name__ == '__main__':
    UrbandictionaryScraper().run(0, 0)
