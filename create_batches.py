import argparse
import os
import random
from collections import defaultdict

def get_alphagram(word):
    return ''.join(sorted(word))

def create_anagram_groups(words, min_length, max_length):
    anagram_groups = defaultdict(list)
    for word in words:
        if min_length <= len(word) <= max_length:
            alphagram = get_alphagram(word)
            anagram_groups[alphagram].append(word)
    return anagram_groups

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def generate_batches(anagram_groups, batch_size, batch_inc):
    ordered_groups = list(anagram_groups.items())
    random.shuffle(ordered_groups)
    
    batches = []
    for start_index in range(0, len(ordered_groups), batch_inc):
        end_index = min(start_index + batch_size, len(ordered_groups))
        batch = ordered_groups[start_index:end_index]
        batches.append((start_index, end_index, batch))
    return batches

def write_batch_to_file(directory, start_index, end_index, batch):
    filename = f"{start_index}_to_{end_index}.txt"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        for _, anagrams in batch:
            file.write('\n'.join(anagrams) + '\n')

def main():
    parser = argparse.ArgumentParser(description='Create anagram groups from a text file.')
    parser.add_argument('filename', help='Path to the text file containing words.')
    parser.add_argument('batch_size', type=int, help='Size of each batch.')
    parser.add_argument('batch_inc', type=int, help='Increment value for the start index of each batch.')
    parser.add_argument('directory', help='Directory to store the output files.')
    parser.add_argument('--min', type=int, default=0, help='Minimum word length to include.')
    parser.add_argument('--max', type=int, default=float('inf'), help='Maximum word length to include.')

    args = parser.parse_args()
    file_path = args.filename
    batch_size = args.batch_size
    batch_inc = args.batch_inc
    output_directory = args.directory
    min_length = args.min
    max_length = args.max

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    words = read_words_from_file(file_path)
    anagram_groups = create_anagram_groups(words, min_length, max_length)
    batches = generate_batches(anagram_groups, batch_size, batch_inc)

    for start_index, end_index, batch in batches:
        write_batch_to_file(output_directory, start_index, end_index, batch)
        print(f'Batch {start_index + 1} to {end_index} written to file.')

if __name__ == "__main__":
    main()
