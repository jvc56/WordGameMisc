import syllapy

def get_words():
    words = []
    with open('csw21.txt') as f:
        words = f.read().splitlines()
    return words

def word_key(subword, a, word, b):
    return "%s (%d) -> %s (%d)" % (subword, a, word, b)

def populate_words_to_number_of_syllables():
    words_to_number_of_syllables = {}
    for word in words:
        number_of_syllables = syllapy.count(word)
        if number_of_syllables > 0:
            words_to_number_of_syllables[word] = number_of_syllables
    return words_to_number_of_syllables


if __name__ == '__main__':
    words = get_words()
    words_to_number_of_syllables = populate_words_to_number_of_syllables()
    pairs = set()
    for word in words_to_number_of_syllables:
        number_of_syllables_in_word = words_to_number_of_syllables[word]
        for i in range(len(word)):
            subword = word[:i] + word[i+1:]
            number_of_syllables_in_subword = words_to_number_of_syllables.get(subword, -1)
            if number_of_syllables_in_subword > number_of_syllables_in_word:
                pairs.add(word_key(subword, number_of_syllables_in_subword, word, number_of_syllables_in_word))
    pairs_list = list(pairs)
    pairs_list.sort()
    for el in pairs_list:
        print (el)