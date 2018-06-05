import random

my_file_names = ['doyle-27.txt', 'doyle-case-27.txt', 'alice-27.txt', 'london-call-27.txt', 'melville-billy-27.txt',
                 'twain-adventures-27.txt']
my_dictionary = {}


class Entry:
    def __init__(self, the_entry_word: str):
        self.word = the_entry_word
        self.count = 1


class EntryDict:
    def __init__(self, the_entry_word: str):
        self.word = the_entry_word
        self.dictionary = {}
        self.count = 1


# Fills the dictionary with trigrams. Will stop at the third to last word in every file.
def read_files(the_first_index: int, the_size: int):
    for i in range(the_first_index, the_size):
        with open(my_file_names[i], 'r') as file:
            words = [word.lower() for line in file for word in line.split()]
        for j in range(0, words.__len__() - 2):
            if words[j] not in my_dictionary:
                my_dictionary[words[j]] = EntryDict(words[j])
            first_level_entry = my_dictionary[words[j]]
            if words[j + 1] not in first_level_entry.dictionary:
                first_level_entry.dictionary[words[j + 1]] = EntryDict(words[j + 1])
            else:
                first_level_entry.dictionary[words[j + 1]].count += 1
            second_level_entry: EntryDict = first_level_entry.dictionary[words[j + 1]]
            if words[j + 2] not in second_level_entry.dictionary:
                second_level_entry.dictionary[words[j + 2]] = Entry(words[j + 2])
            else:
                second_level_entry.dictionary[words[j + 2]].count += 1


# Picks a random value in the dictionary by weighing them using their frequency of appearance.
def weighted_random(the_dictionary: dict):
    weighted_list = []
    for entry in the_dictionary.values():
        weighted_list.extend([entry] * entry.count)
    return random.choice(weighted_list)


# Generates a story using the generated dictionary. Will crash if it randomly picks any of the 2 last words in any
# files that appears for the first time because they don't exist in the dictionary yet. A simple fix is to check if
# a key exist in the dictionary and pick a random word if it does not. However, the possibility is too low for the speed
# trade-off
def write_story(the_output_name: str, length: int):
    output = open(the_output_name, 'w')
    first_level_entry: EntryDict = my_dictionary[random.choice([*my_dictionary])]
    output.write(first_level_entry.word + ' ')
    while length > 0:
        second_level_entry = weighted_random(first_level_entry.dictionary)
        output.write(second_level_entry.word + ' ')
        third_level_entry = weighted_random(second_level_entry.dictionary)
        output.write(third_level_entry.word + ' ')
        first_level_entry = my_dictionary[third_level_entry.word]
        length -= 1
    output.close()


read_files(0, 2)
write_story('output_2.txt', 1000)
read_files(2, 6)
write_story('output_6.txt', 1000)
