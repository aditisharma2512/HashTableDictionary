from hash_table import LinearProbeHashTable
import timeit


class Dictionary:
    def __init__(self, hash_base: int, table_size: int) -> None:
        """
        Constructs a Hash Table with given parameters
        :param hash_base: contains the base of the hash table
        :param table_size: contains the size of the hash table
        :raises ValueError if either of the parameters are less than 0
        :returns None
        @complexity: O(1) for this method
        """
        if hash_base < 0 or table_size < 0:
            raise ValueError("Hash base and table size must be >= 0")
        self.hash_table = LinearProbeHashTable(hash_base, table_size)

    def load_dictionary(self, filename: str, time_limit: int = None) -> int:
        """
        Loads a file and loads the content (lines) of the file into the Hash table
        :param filename: Name of the file being read
        :param time_limit: Max time limit before timeout error (defaults to none if not provided)
        :return: number of words in the file (which is number of lines since each line has one word)
        @complexity: O(n) where n is the number of lines in the file
        """

        with open(filename, mode='r', encoding='utf-8') as fn:
            file = fn.readlines()
        words = 0
        start = timeit.default_timer()
        for line in file:
            line = line.strip('\n')
            self.hash_table[line.lower()] = 1
            words += 1
            current = timeit.default_timer()
            if time_limit and (current - start) > time_limit:
                raise TimeoutError("Time limit exceeded")
            else:
                pass
        return words

    def add_word(self, word: str) -> None:
        """
        Adds a word specified by the user
        :param word: word to be added to the dictionary
        :return: None
        @Complexity: O(1)
        """
        self.hash_table[word.lower()] = 1

    def find_word(self, word: str) -> bool:
        """
        Checks if the word exists in the dictionary
        :param word: Word to be searched
        :return: True if found, else false
        @Complexity: O(1)
        """
        return word in self.hash_table

    def delete_word(self, word: str) -> None:
        """
        Deletes a word from the hash table
        :param word: The word to be deleted
        :return: None
        @Complexity: O(1)
        """
        del self.hash_table[word.lower()]

    def get_word_input(self) -> str:
        return input("Enter the word: ")

    def menu(self) -> None:
        """
        Displays a menu for the user to interact with
        :return: None
        @Complexity: O(number of times user wants to run the menu)
        """
        cont = True
        while cont:
            print("\nMenu\n\n1. Read File\n2. Add Word\n3. Find Word\n4. Delete Word\n5. Exit")
            try:
                user_input = int(input("Enter your choice (1-5) : "))
            except ValueError:
                print("ERROR: Only enter from 1 to 5")
                cont = True
            else:
                if user_input == 1:
                    filename = input("Enter the filename (make sure the file is in the same directory : ")
                    try:
                        self.load_dictionary(filename)
                    except TimeoutError:
                        print("Reading the file timed out")
                    else:
                        print("Successfully read!")
                elif user_input == 2:
                    self.add_word(self.get_word_input())
                    print("Added word")
                elif user_input == 3:
                    print(self.find_word(self.get_word_input()))
                elif user_input == 4:
                    self.delete_word(self.get_word_input())
                    print("Deleted word")
                elif user_input == 5:
                    cont = False
