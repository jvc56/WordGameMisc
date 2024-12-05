import argparse
import statistics

# Create an argument parser
parser = argparse.ArgumentParser(description='Read a text file with word probabilities.')

# Add an argument for the input lexicon file
parser.add_argument('lexicon', help='the input lexicon file')

# Add an argument for the file containing the words to check
parser.add_argument('words_file', help='the file containing the words')

# Parse the command-line arguments
args = parser.parse_args()

# Retrieve the input lexicon filename from the arguments
lexicon = args.lexicon

# Retrieve the filename containing the words to check from the arguments
words_file = args.words_file

# Create an empty dictionary to store the word probabilities
word_probabilities = {}

# Open the lexicon file and read its contents
with open(lexicon, 'r') as file:
    for line in file:
        # Split the line into word and probability
        word, probability = line.strip().split()

        # Store the word and probability in the dictionary
        word_probabilities[word.upper()] = int(probability)

# Read the file containing the words to check
with open(words_file, 'r') as file:
    words_to_check = [word.strip().upper() for word in file]

# Create a dictionary to store the word lengths and their respective word probabilities
word_lengths = {}

# Calculate the total probability for each word length
for word in words_to_check:
    length = len(word)
    if length in word_lengths:
        word_lengths[length].append(word_probabilities[word])
    else:
        word_lengths[length] = [word_probabilities[word]]

# Calculate the average probability for each word length
for length, probabilities in word_lengths.items():
    print(f"Word Length: {length}")
    print(f"Count: {len(probabilities)}")
    print(f"Average Probability: {statistics.mean(probabilities):.2f}")
    if len(probabilities) > 1:
        print(f"Standard Deviation: {statistics.stdev(probabilities):.2f}")
    else:
        print("Standard Deviation: Not applicable (only one word of this length)")
    print()
