import sys

def load_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r') as file:
        for line in file:
            word, definition = line.strip().split('\t')
            dictionary[word.strip()] = definition
    return dictionary

def add_definitions(dictionary, input_file_path, output_file_path):
    at_first = True
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            if at_first:
                output_file.write("0\n")
                at_first = False
                continue
            word1, word2, value = line.strip().split(';')
            if word1 in dictionary and word2 in dictionary:
                definition1 = dictionary[word1].replace(';', '')
                definition2 = dictionary[word2].replace(';', '')
                line = f"{word1}<br>{definition1};{word2}<br>{definition2};{value}"
            else:
                print("word(s) not in dict:\n")
                print(f"{word1},{word2}")
            output_file.write(line + '\n')

if __name__ == '__main__':
    dictionary_file_path = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    dictionary = load_dictionary(dictionary_file_path)
    add_definitions(dictionary, input_file_path, output_file_path)

