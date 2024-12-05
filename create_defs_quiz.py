import argparse

def word_has_front_hooks(word_info):
    # The split string function discards
    # empty strings so if word_info is
    # length 4 we know that the word
    # must have front hooks
    return len(word_info) == 4

def create_word_defs_dict(filename, min_length, max_length):
    print('0')
    with open(filename, 'r') as file:
        for line in file:
            word_info = line.strip().split('\t')

            front_hooks = ''
            if word_has_front_hooks(word_info):
                front_hooks = word_info[0]
                word_info.pop(0)
            # The length of word_info is now guaranteed
            # to be 3
            word_with_inner_hooks = word_info[0].strip()
            word = word_with_inner_hooks
            if word[0] == '·':
                word = word[1:]
            if word[-1] == '·':
                word = word[:-1]
            if len(word) < min_length or len(word) > max_length:
                continue
            back_hooks = word_info[1]
            definition = word_info[2].replace(";", ":")
            quiz_line = f"{word};{front_hooks}/{word_with_inner_hooks}/{back_hooks}<br>{definition};0"
            print(quiz_line)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Input file name')
    parser.add_argument('min', type=int, help='Minimum word length')
    parser.add_argument('max', type=int, help='Maximum word length')
    args = parser.parse_args()

    filename = args.filename
    min_length = args.min
    max_length = args.max

    create_word_defs_dict(filename, min_length, max_length)
