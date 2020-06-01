from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from string import punctuation
from enum import Enum


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    MISSPELT = -1

    def find_rarity(self, max, score):
        if not score or score == 0:
            return Rarity.MISSPELT
        if score >= (max/100):
            return Rarity.COMMON
        elif score <  max/1000:
            return Rarity.RARE
        else:
            return Rarity.UNCOMMON

class Frequency:
    def __init__(self, hash_base: int, table_size: int) -> None:
        self.hash_table = LinearProbeHashTable(hash_base, table_size)
        self.dictionary = Dictionary(hash_base, table_size)
        self.dictionary.load_dictionary('english_large.txt')
        self.max_word = (None, 0)

    def __prepare_word(self, word: str) -> str:
        word = word.lower()
        word = word.strip('\n')
        if word[:-1] in punctuation:
            word = word[0:len(word) - 2]
        if word[0] in punctuation:
            word = word[1:]
        return word

    def add_file(self, filename: str) -> None:
        with open(filename, mode='r', encoding='utf-8') as fn:
            lines = fn.readlines()
            for line in lines:
                words = line.split()
                for word in words:
                    fixed_word = self.__prepare_word(self, word)
                    if self.dictionary.find_word(fixed_word):
                        if fixed_word not in self.hash_table:
                            self.hash_table[fixed_word] = 1
                        else:
                            self.hash_table[fixed_word] += 1
                        if self.hash_table[fixed_word] > self.max_word[1]:
                            self.max_word = (fixed_word, self.hash_table[fixed_word])

    def rarity(self, word: str) -> Rarity:
        fixed_word = self.__prepare_word(word)
        max = self.max_word[1]
        if word in self.hash_table:
            count = self.hash_table[word]
            return Rarity.find_rarity(max, count)


