from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from string import punctuation
from enum import Enum
from list import ArrayList
import sys


class Rarity(Enum):
    """
    This class will return the Rarity value
    """
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    MISSPELT = -1


class Frequency:
    """
    This class with calculate and store the frequency of words in a file mentioned by the user.
    """
    def __init__(self, hash_base: int = LinearProbeHashTable.DEFAULT_HASH_BASE, table_size: int = LinearProbeHashTable.DEFAULT_TABLE_SIZE) -> None:
        """
        Constructor for the frequency class, creates a dictionary using the English large file
        :param hash_base: Sets the base for the hash table, defaults to the default value mentioned in
        the Linear Probe Hash Table
        :param table_size: Sets the size for the hash table, defaults to the default value mentioned in
        the Linear Probe Hash Table
        """
        self.hash_table = LinearProbeHashTable(hash_base, table_size)
        self.dictionary = Dictionary(hash_base, table_size)
        self.dictionary.load_dictionary('english_large.txt')
        self.max_word = (None, 0)

    def __prepare_word(self, word: str) -> str:
        """
        Prepares the word to be added to the dictionary
        :param word: The word to be added
        :return: The fixed word, after converting to lowercase and removing punctuations
        """
        word = word.lower()
        word = word.strip('\n')
        if len(word) < 1:
            return word
        fixed_word = ''
        for i in range(len(word)):
            if i == 0 and word[i] in punctuation:
                pass
            elif i == len(word) - 1 and word[i] in punctuation:
                pass
            else:
                fixed_word += word[i]
        return fixed_word

    def add_file(self, filename: str) -> None:
        """
        Reads the file mentioned by the user and counts the words
        :param filename: Filename of the file to be read
        :return: None
        """
        with open(filename, mode='r', encoding='utf-8') as fn:
            lines = fn.readlines()
            for line in lines:
                words = line.split()
                for word in words:
                    fixed_word = self.__prepare_word(word)
                    if self.dictionary.find_word(fixed_word):
                        if fixed_word not in self.hash_table:
                            self.hash_table[fixed_word] = 1
                        else:
                            self.hash_table[fixed_word] += 1
                        if self.hash_table[fixed_word] > self.max_word[1]:
                            self.max_word = (fixed_word, self.hash_table[fixed_word])

    def rarity(self, word: str) -> Rarity:
        """
        Gets the rarity of the word from the Rarity class
        :param word: the word to be checked
        :return: The Rarity value of the word
        """
        fixed_word = self.__prepare_word(word)
        max = self.max_word[1]
        if fixed_word in self.hash_table:
            count = self.hash_table[fixed_word]
            if count >= max / 100:
                return Rarity.COMMON
            elif count < (max / 1000):
                return Rarity.RARE
            else:
                return Rarity.UNCOMMON
        else:
            return Rarity.MISSPELT

    def partition(self, array: ArrayList[tuple], low: int, high: int) -> int:
        """
        Creates a partition for the quick sort
        :param array: The array to be sorted
        :param low: lower index
        :param high: high index
        :return: the index till where the array is sorted
        """
        # Select the pivot element
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j][1] >= pivot[1]:
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])
        (array[i + 1], array[high]) = (array[high], array[i + 1])
        return i + 1

    def quickSort(self, array: ArrayList[tuple], low: int, high: int) -> ArrayList[tuple]:
        """
        Quick sorts the ArrayList
        :param array: The ArrayList to be sorted
        :param low: Lower index
        :param high: High index
        :return: A sorted list
        """
        if low < high:
            # Select pivot position and put all the elements smaller
            # than pivot on left and greater than pivot on right
            pi = self.partition(array, low, high)

            # Sort the elements on the left of pivot
            self.quickSort(array, low, pi - 1)

            # Sort the elements on the right of pivot
            self.quickSort(array, pi + 1, high)
        return array

    def ranking(self) -> ArrayList[tuple]:
        """
        Sets the ranking of each word in the ArrayList
        :return: A list of words with their ranking, in descending order
        """
        sys.setrecursionlimit(99999)
        list_of_words = ArrayList(len(self.hash_table))
        for word, freq in self.hash_table:
            if word is not None and word != '':
                list_of_words.insert(len(list_of_words), (word, freq))
        list_of_words = self.quickSort(list_of_words, 0, len(list_of_words)-1)
        return list_of_words


def frequency_analysis() -> None:
    filename = '84-0.txt'
    f = Frequency(31, 250727)
    f.add_file(filename)
    ranks = f.ranking()
    cont = True
    while cont:
        print("How many words do you want to see? (0 to quit) ")
        try:
            user_input = int(input())
        except ValueError:
            print("You must enter an integer")
        else:
            if user_input == 0:
                cont = False
            for i in range(user_input):
                print("Word: " + str(ranks[i][0]))
                print("Occurrences: " + str(ranks[i][1]))
                print("Rarity: " + str(f.rarity(ranks[i][0])))
                print("\n")


if __name__ == '__main__':
    frequency_analysis()
