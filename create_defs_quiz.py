import argparse

LAST_WORD_STRING = "LAST_WORD"

def word_has_front_hooks(word_info):
    # The split string function discards
    # empty strings so if word_info is
    # length 4 we know that the word
    # must have front hooks
    return len(word_info) == 4

def create_word_defs_dict(filename):
    word_answer_dict = {}
    word_lists_by_length = {}
    with open(filename, 'r') as file:
        for line in file:
            word_info = line.strip().split('\t')
            if len(word_info) < 3:
                print(f"Invalid line:\n{line}\n")
                exit(1)

            front_hooks = ''
            if word_has_front_hooks(word_info):
                front_hooks = word_info[0]
                word_info.pop(0)
            # The length of word_info is now guaranteed
            # to be 3
            word_with_inner_hooks = word_info[0].strip().upper()
            word = word_with_inner_hooks
            if word[0] == '·':
                word = word[1:]
            if word[-1] == '·':
                word = word[:-1]
            back_hooks = word_info[1]
            definition = word_info[2].replace(";", ":")
            word_answer_dict[word] = f"{front_hooks}/{word_with_inner_hooks}/{back_hooks}<br>{definition}"
            word_len = len(word)
            if word_len not in word_lists_by_length:
                word_lists_by_length[word_len] = []
            word_lists_by_length[word_len].append(word)

    return word_answer_dict, word_lists_by_length

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('defs', help='lexicon with front hooks, back hooks, inner hooks, and definitions')
    parser.add_argument('words', help='quiz words')
    args = parser.parse_args()

    defs_filename = args.defs
    words_filename = args.words

    word_answer_dict, word_lists_by_length = create_word_defs_dict(defs_filename)

    next_words = {}

    # Alphabetize each word list and set next words dict:
    for word_list in word_lists_by_length.values():
        word_list.sort()
        for i in range(len(word_list) - 1):
            next_words[word_list[i]] = word_list[i+1]
        next_words[word_list[-1]] = LAST_WORD_STRING
    
    print('0')
    with open(words_filename, 'r') as file:
        for line in file:
            word = line.strip().upper()
            if word not in word_answer_dict:
                raise ValueError(f"Word {word} not found in lexicon")
            if word not in next_words:
                raise ValueError(f"Word {word} not found in next words")
            answer = word_answer_dict[word]
            next_word = next_words[word]
            next_answer = 'LAST WORD'
            if next_word != LAST_WORD_STRING:
                next_answer = word_answer_dict[next_word]
            print(f"{word};{answer}<br>***<br>{next_answer};0")

    