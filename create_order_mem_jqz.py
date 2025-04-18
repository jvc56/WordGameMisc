def get_words(filename):
    words = []
    with open(filename) as f:
        words = f.read().splitlines()
    return words

def convert_file_to_jqz(filename):
    words = get_words(filename)
    fs = "0\n*;{};0\n".format(words[0])
    for i in range(len(words) - 1):
        fs += "{};{};0\n".format(words[i], words[i+1])
    fs += "{};-;0\n".format(words[len(words) - 1])
    return fs

if __name__ == '__main__':
    print(convert_file_to_jqz('csw21_fives.txt'));