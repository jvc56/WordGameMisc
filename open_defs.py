import re
import csv

def read_word_definitions(file_path):
    """
    Reads a file containing words and their definitions in a specific format.
    
    Args:
        file_path (str): Path to the input file.
    
    Returns:
        dict: A dictionary mapping words (uppercase) to their definitions, or 1 if no definition exists.
    
    Raises:
        ValueError: If a line does not begin with a contiguous string of A-Z letters.
    """
    word_definitions = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split("\t", 1)
            word = parts[0].strip().upper()
            
            if not word.isalpha():
                raise ValueError(f"Invalid line format: {line}")
            
            definition = parts[1].strip() if len(parts) > 1 else 1
            word_definitions[word] = definition
    
    return word_definitions


def load_and_print_file_info(file_path):
    """
    Loads a file using read_word_definitions and prints its information.
    
    Args:
        file_path (str): Path to the file.
        description (str): Description of the file being loaded.
    
    Returns:
        dict: A dictionary of words and their definitions from the file.
    """
    word_dict = read_word_definitions(file_path)
    print(f"Total words loaded from {file_path}: {len(word_dict)}")
    return word_dict


def get_words_with_expurgated_in_definition(csw21_defs, expurgated_words):
    """
    Checks each definition in csw21_defs to see if any word in the definition 
    is present in expurgated_words. Returns a dictionary of words to expurgated words
    found in their definitions.

    Args:
        csw21_defs (dict): A dictionary of words and their definitions from csw21_defs.
        expurgated_words (dict): A dictionary of words from csw19 or csw21 that are not in csw24.

    Returns:
        dict: A dictionary mapping words from csw21_defs to expurgated words found in their definitions.
    """
    expurgated_in_definitions = {}

    # Iterate through each word in csw21_defs
    for word, definition in csw21_defs.items():
        # Split the definition by whitespace and clean up the words
        words_in_definition = re.findall(r'[A-Za-z]+', definition)  # Find words with letters only
        cleaned_words = [w.upper() for w in words_in_definition]  # Remove non-letters and capitalize

        # Check if any cleaned word is in the expurgated_words dictionary
        expurgations = {word for word in cleaned_words if word in expurgated_words}
        
        if expurgations:
            expurgated_in_definitions[word] = expurgations

    return expurgated_in_definitions

def get_new_root_words_to_new_inflections(new_words, csw24_defs):
    root_words_to_new_words = {}
    for word in new_words:
        def_root_words = re.findall(r'[A-Z]+', csw24_defs[word])
        for root_word in def_root_words:
            if root_word in csw24_defs:
                if root_word not in root_words_to_new_words:
                    root_words_to_new_words[root_word] = set()
                root_words_to_new_words[root_word].add(word)
    return root_words_to_new_words

def export_words_to_csv(words_to_update, output_file='words_to_update.csv'):
    """
    Exports the list of words and their definitions to a CSV file.

    Args:
        words_to_update (list): The list of words to update.
        output_file (str): The name of the output CSV file.
    """
    # Writing to CSV with tab delimiter and no quotes around fields
    with open('words_to_update.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t', quotechar='', quoting=csv.QUOTE_NONE)
        writer.writerow(['Word', 'Definition', 'Source', 'New Inflection', 'Expurgations'])  # Header row
        for word, definition, source, new_inflection, expurgations in words_to_update:
            expurgations_str = ', '.join(expurgations)
            new_inflection_str = ', '.join(new_inflection)
            writer.writerow([word, definition, source, new_inflection_str, expurgations_str])

def dict_to_csv(dictionary, filename, delimiter=','):
    """
    Write a dictionary to a CSV file.

    Args:
        dictionary (dict): The dictionary to write to the CSV file.
        filename (str): The name of the CSV file to write to.
        delimiter (str): The delimiter to use in the CSV file (default is ',').

    Returns:
        None
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for key, value in dictionary.items():
            writer.writerow([key, value])

if __name__ == "__main__":
    csw19_path = 'csw19.txt'
    csw21_path = 'csw21_defs.txt'
    csw24_path = 'csw24_defs.txt'

    csw19_words = load_and_print_file_info(csw19_path)
    csw21_defs = load_and_print_file_info(csw21_path)
    csw24_defs = load_and_print_file_info(csw24_path)

    csw24_new_words_list = [word for word in csw24_defs if word not in csw21_defs]
    csw24_root_words_to_new_inflections_dict = get_new_root_words_to_new_inflections(csw24_new_words_list, csw24_defs)
    
    
    csw19_expurgated_words = {word 
                    for word in set(csw19_words) 
                    if word not in csw21_defs}
    

    csw21_expurgated_words = {word 
                    for word in set(csw21_defs) 
                    if word not in csw24_defs}


    expurgated_words_set = csw19_expurgated_words | csw21_expurgated_words


    csw21_words_to_expurgated_words_in_defs = get_words_with_expurgated_in_definition(csw21_defs, expurgated_words_set)

    print(f"CSW19 -> CSW21 expurgated words: {len(csw19_expurgated_words)}")
    print(f"CSW21 -> CSW24 expurgated words: {len(csw21_expurgated_words)}")
    print(f"Total expurgated words: {len(expurgated_words_set)}")
    print(f"New words in CSW24: {len(csw24_new_words_list)}")
    print(f"Root words to new words in CSW24: {len(csw24_root_words_to_new_inflections_dict)}")
    print(f"Total expurgated words: {len(expurgated_words_set)}")
    print(f"Words with expurgated words in definitions: {len(csw21_words_to_expurgated_words_in_defs)}")

    # Create words_to_update as a list of tuples (word, definition, source)
    words_to_update = []

    # Add words from new_words with source 'CSW24' and empty expurgations
    for word in csw24_new_words_list:
        definition = csw24_defs.get(word)
        if not definition:
            raise ValueError(f"Definition missing for new CSW24 word '{word}' in CSW24!")
        
        # Add tuple with empty expurgations
        words_to_update.append((word, definition, 'CSW24', set(), set()))

    # Add words from expurgated_in_definitions with source 'CSW21'
    for word, expurgations in csw21_words_to_expurgated_words_in_defs.items():
        if word not in csw24_defs:
            continue
        definition = csw21_defs.get(word)
        if not definition:
            raise ValueError(f"Definition missing for CSW21 word '{word}' in CSW21!")

        words_to_update.append((word, definition, 'CSW21', set(), expurgations))

    csw21_possible_new_inflections_count = 0
    for root_word, new_words in csw24_root_words_to_new_inflections_dict.items():
        if word not in csw24_defs:
            raise ValueError(f"Definition missing for new root CSW24 word '{word}' in CSW24!")
        definition = csw21_defs.get(root_word)
        if definition:
            words_to_update.append((root_word, definition, 'CSW21', new_words, set()))
            csw21_possible_new_inflections_count += 1

    print(f"CSW21 Possible New Inflections: {csw21_possible_new_inflections_count}")

    # Sort the words_to_update list alphabetically by the word
    words_to_update = sorted(words_to_update, key=lambda x: x[0])

    # Print words_to_update details
    print(f"Total words to update: {len(words_to_update)}")

    dict_to_csv(csw24_root_words_to_new_inflections_dict, 'new_inflections.csv')
    # Export the words_to_update and their definitions to a CSV file
    export_words_to_csv(words_to_update, 'words_to_update.csv')

