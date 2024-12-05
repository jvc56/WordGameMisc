import argparse
import re

def read_definitions(file_path):
    definitions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split('\t')
            if len(parts) > 1:
                word = parts[0]
                definition = parts[1].strip()
                definitions.append((word, definition))
    return definitions

def filter_definitions_by_word_length(definitions, min_length, max_length):
    filtered_definitions = [
        (word, definition) for word, definition in definitions 
        if min_length <= len(word) <= max_length
    ]
    return filtered_definitions

def top_n_definitions_by_length(definitions, N):
    sorted_definitions = sorted(definitions, key=lambda x: len(x[1]), reverse=True)
    return sorted_definitions[:N]

def find_definitions_with_4digit_number(definitions):
    regex = re.compile(r'\b\d{3}\b')
    matching_definitions = [
        (word, definition) for word, definition in definitions 
        if regex.search(definition)
    ]
    return matching_definitions

def main(file_path, N, min_length, max_length):
    definitions = read_definitions(file_path)
    filtered_definitions = filter_definitions_by_word_length(definitions, min_length, max_length)
    top_definitions = top_n_definitions_by_length(filtered_definitions, N)
    definitions_with_4digit_number = find_definitions_with_4digit_number(filtered_definitions)

    print("Top N definitions by length:")
    for word, definition in top_definitions:
        print(f"{word}: {definition}")

    print("\nDefinitions containing a 4-digit number:")
    for word, definition in definitions_with_4digit_number:
        print(f"{word}: {definition}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the top N definitions by length from a file and find definitions containing 4-digit numbers.')
    parser.add_argument('file_path', type=str, help='Path to the definitions file')
    parser.add_argument('N', type=int, help='Number of top definitions to retrieve')
    parser.add_argument('--min', type=int, default=1, help='Minimum word length to consider (inclusive)')
    parser.add_argument('--max', type=int, default=float('inf'), help='Maximum word length to consider (inclusive)')
    args = parser.parse_args()
    
    main(args.file_path, args.N, args.min, args.max)
