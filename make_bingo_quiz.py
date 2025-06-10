import sys
from collections import defaultdict
from math import comb

TILE_COUNTS = {
    'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9,
    'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6,
    'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1
}

def get_all_words_with_definitions(filename):
    """
    Reads a file with tab-separated word and definition pairs and returns a dictionary
    of words (uppercase) to their definitions.

    Args:
        filename (str): The path to the input file.

    Returns:
        dict: A dictionary mapping uppercase words to their definitions.
    """
    word_definitions = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and '\t' in line:
                    parts = line.split('\t', 1)  # Split on first tab only
                    if len(parts) == 2:
                        word = parts[0].strip().upper()
                        definition = parts[1].strip()
                        if word and definition:
                            word_definitions[word] = definition
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    return word_definitions

def extract_parts_of_speech(definition):
    """
    Extracts parts of speech from a definition string.
    Looks for patterns like [n], [v], [adj], [interj], etc.

    Args:
        definition (str): The definition string.

    Returns:
        set: A set of parts of speech found in the definition.
    """
    parts_of_speech = set()
    
    # Find all bracketed content
    import re
    brackets = re.findall(r'\[([^\]]+)\]', definition)
    
    for bracket_content in brackets:
        # Split by commas and spaces to handle multiple parts of speech
        parts = re.split(r'[,\s]+', bracket_content.lower())
        for part in parts:
            part = part.strip()
            # Check for common part of speech abbreviations
            if part in ['n', 'noun', 'nouns']:
                parts_of_speech.add('noun')
            elif part in ['v', 'verb', 'verbs']:
                parts_of_speech.add('verb')
            elif part in ['adj', 'adjective', 'adjectives']:
                parts_of_speech.add('adjective')
            elif part in ['adv', 'adverb', 'adverbs']:
                parts_of_speech.add('adverb')
            elif part in ['interj', 'interjection']:
                parts_of_speech.add('interjection')
            elif part in ['prep', 'preposition']:
                parts_of_speech.add('preposition')
            elif part in ['conj', 'conjunction']:
                parts_of_speech.add('conjunction')
            elif part in ['pron', 'pronoun']:
                parts_of_speech.add('pronoun')
    
    return parts_of_speech

def alphabetize(word):
    """Returns a string with the letters of the word sorted alphabetically."""
    return ''.join(sorted(word))

def get_anagram_groups(words):
    """
    Groups words by their anagrams (words with same letters).

    Args:
        words (iterable): Collection of words to group.

    Returns:
        dict: Dictionary mapping sorted letter signature to list of words.
    """
    anagram_groups = defaultdict(list)
    for word in words:
        # Sort the letters to create an anagram signature
        signature = alphabetize(word)
        anagram_groups[signature].append(word)
    return anagram_groups

def is_word_tricky(word, word_definitions, anagram_groups):
    """
    Checks if a word meets the specified criteria.

    Args:
        word (str): The word to validate (this word will already be uppercase).
        word_definitions (dict): Dictionary of words to their definitions.
        anagram_groups (dict): Dictionary of anagram groups.

    Returns:
        bool: True if the word is valid, False otherwise.
    """
    if len(word) != 7 and len(word) != 8:
        return False

    num_anagrams = len(anagram_groups[alphabetize(word)])

    # Check if word has 3 or fewer anagrams
    if num_anagrams > 3:
        return False

    definition = word_definitions.get(word, "")
    parts_of_speech = extract_parts_of_speech(definition)

    # New criterion: ends with 'ED' and only has adjective part of speech
    if word.endswith("ED") and 'adjective' in parts_of_speech:
        return True

    if word.endswith("ING"):
        plural_form = word + "S"
        if plural_form in word_definitions:
            return True

    suffixes = ["ANT", "ENT", "ITY", "LY", "ABLE", "NESS", "LESS", "LIKE", "EAU", "IEU", "ATE", "OID", "INESS", "IVE", "IAN", "FUL", "FORM", "OSE", "OUS", "ISH", "UM"]
    for suffix in suffixes:
        if word.endswith(suffix):
            return True
    
    if word.endswith("ER") and num_anagrams == 1 and word + "S" in word_definitions:
        return True

    if word.startswith("UN") and word.endswith("ED"):
        return True

    prefixes = ["OVER", "OUT", "NON", "EM", "IM", "EN"]
    for prefix in prefixes:
        if word.startswith(prefix):
            return True

    if sum(1 for char in word if char in "AEIOU") == 5:
        return True

    return False

def process_tricky_words(word_definitions, anagram_groups, alphagram_word_dict):
    for word in word_definitions.keys():
        if is_word_tricky(word, word_definitions, anagram_groups):
            alphagram = alphabetize(word)
            alphagram_word_dict[alphagram] = anagram_groups[alphagram][0]

def calculate_ways_to_draw(rack):
    """
    Calculates the number of ways to draw a set of rack from a Scrabble bag.
    """
    rack_counts = defaultdict(int)
    for char in rack:
        rack_counts[char] += 1

    total_ways = 1

    for char, count in rack_counts.items():
        if TILE_COUNTS[char] < count:
            return 1
        else:
            total_ways *= comb(TILE_COUNTS[char], count)

    return total_ways

def process_missed_bingos(missed_bingos_filepath, alphagram_word_dict):
    """
    Reads 'missed_bingos.txt' into a dictionary.
    Key: alphabetized letters, Value: one valid anagram.
    """
    with open(missed_bingos_filepath, 'r') as f:
        for line in f:
            word = line.strip().upper()
            if word:
                alphagram_word_dict[alphabetize(word)] = word

def process_probable_bingos(anagram_groups, alphagram_word_dict, N):
    num_existing_alphagrams = len(alphagram_word_dict)
    if num_existing_alphagrams >= N:
        return
    sevens_with_probs = []
    eights_with_probs = []
    for alphagram, words in anagram_groups.items():
        if len(words) > 3:
            continue
        if len(alphagram) == 7:
            sevens_with_probs.append((words[0], calculate_ways_to_draw(alphagram)))
        elif len(alphagram) == 8:
            eights_with_probs.append((words[0], calculate_ways_to_draw(alphagram)))
    sevens_with_probs.sort(key=lambda item: item[1], reverse=True)
    eights_with_probs.sort(key=lambda item: item[1], reverse=True)
    last_seven_added = ""
    last_eight_added = ""
    while len(alphagram_word_dict) < N:
        if len(sevens_with_probs) > 0:
            seven = sevens_with_probs[0][0]
            alphagram_word_dict[alphabetize(seven)] = seven
            last_seven_added = seven
            sevens_with_probs.pop(0)
        if len(alphagram_word_dict) < N and len(eights_with_probs) > 0:
            eight = eights_with_probs[0][0]
            alphagram_word_dict[alphabetize(eight)] = eight
            last_eight_added = eight
            eights_with_probs.pop(0)
    print(f"Least probable seven is {last_seven_added}\nLeast probable eight is {last_eight_added}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <N>")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
        if N < 0:
            raise ValueError("N must be a non-negative integer.")
    except ValueError as e:
        print(f"Error: Invalid argument for N. {e}")
        sys.exit(1)

    # Hardcoded file paths (assuming they are in the same directory as the script)
    csw24_with_defs_file = 'csw24.tsv'
    missed_bingos_file = 'missed_bingos.txt'

    # Get all words and definitions from the file
    word_definitions = get_all_words_with_definitions(csw24_with_defs_file)

    if not word_definitions:
        print(f"No words found in '{csw24_with_defs_file}' to process.")
        sys.exit(0)

    # Create anagram groups for anagram counting
    anagram_groups = get_anagram_groups(word_definitions.keys())

    final_dict = {}

    process_tricky_words(word_definitions, anagram_groups, final_dict)
    num_tricky_words = len(final_dict)
    print(f"Generated {num_tricky_words} tricky words.")

    process_missed_bingos(missed_bingos_file, final_dict)
    num_tricky_word_and_missed_bingos = len(final_dict)
    print(f"Generated {num_tricky_word_and_missed_bingos - num_tricky_words} new unique missed bingos.")

    print(f"Generated {len(final_dict)} unique alphagrams in total.")
    num_extra = N - len(final_dict)
    if num_extra > 0:
        print(f"Generating {N - len(final_dict)} additional unique probable bingos...")
        process_probable_bingos(anagram_groups, final_dict, N)

    output_file = f"bingo_words_{N}.txt"
    with open(output_file, 'w') as f:
        for index, word in enumerate(final_dict.values()):
            if index > 0:
                f.write('\n')
            f.write(word)

    print(f"Generated '{output_file}' with {len(final_dict)} words.")

if __name__ == "__main__":
    main()