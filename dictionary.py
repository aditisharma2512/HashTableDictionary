from hash_table import LinearProbeHashTable
import timeit


class Dictionary:
    def __init__(self, hash_base: int = LinearProbeHashTable.DEFAULT_HASH_BASE, table_size: int = LinearProbeHashTable.DEFAULT_TABLE_SIZE) -> None:
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


class Statistics:
    def __init__(self):
        """
        A constructor is not required for this class
        """
        pass

    def load_statistics(self, hash_base: int, table_size: int, filename: str, max_time: int) -> tuple:
        """
        This method loads the statistics for a file from the LinearProbeHashTable
        :param hash_base: Base of the hash table
        :param table_size: Size of the hash table
        :param filename: Filename to be read
        :param max_time: Maximum time till TimeOut
        :return: A tuple containing words, time, collision_count, probe_total, probe_max, rehash_count
        @complexity: O(1) for this method
        """
        if hash_base < 0 or table_size < 0:
            raise ValueError("Hash Base and Table Size must be >= 0")
        dictionary = Dictionary(hash_base, table_size)
        start_time = timeit.default_timer()
        words = 0
        try:
            words = dictionary.load_dictionary(filename, max_time)
        except TimeoutError:
            words = len(dictionary.hash_table)
            end_time = start_time + max_time
        else:
            end_time = timeit.default_timer()
        collision_count, probe_total, probe_max, rehash_count = dictionary.hash_table.statistics()
        time = end_time - start_time
        return words, time, collision_count, probe_total, probe_max, rehash_count

    def table_load_statistics(self, max_time) -> None:
        """
        This method writes a csv file with the description of the statistics while using the dictionary
        :param max_time: Maximum time before timeout
        :return: None
        @complexity: O(m*n*p) where m = number of files, n = number of bases, p = number of table sizes
        """
        file = ['english_small.txt', 'english_large.txt', 'french.txt']
        b = [1, 27183, 250726]
        tablesize = [250727, 402221, 1000081]

        with open('output_task2.csv', mode='w+', encoding='utf-8') as fn:
            fn.write('file,table size,b,words,time,collision_count,probe_total,probe_max,rehash_count\n')
            for f in file:
                for hb in b:
                    for size in tablesize:
                        words, time, collision_count, probe_total, probe_max, rehash_count = \
                            self.load_statistics(hb, size, f, max_time)
                        fn.write(str(f)+","+str(size)+","+str(hb)+","+str(words)+","+str(time)+","+str(collision_count)
                                 + ","+str(probe_total)+","+str(probe_max)+","+str(rehash_count)+"\n")


if __name__ == '__main__':
    d =Dictionary(1234,123456)
    d.menu()
