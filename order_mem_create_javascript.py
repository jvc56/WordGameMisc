def get_words(filename):
    words = []
    with open(filename) as f:
        words = f.read().splitlines()
    return words

def quote_word(word):
    return '"{}"'.format(word)

def get_words_javascript_array(words):
    return '[{}]'.format(', '.join(map(quote_word, words)))

def combine_javascript_arrays(arrays):
    return 'var words = [\n{}];'.format(',\n'.join(arrays))

def convert_filename_to_javascript_array(filename):
    return get_words_javascript_array(get_words(filename))

if __name__ == '__main__':
    print(combine_javascript_arrays(map(convert_filename_to_javascript_array, ['csw21_threes.txt', 'csw21_fours.txt', 'csw21_fives.txt'])))