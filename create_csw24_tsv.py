import requests
import csv
import sys

# Paths to input files
csw24_path = "csw24.txt"
csw21_with_defs_path = "csw21_with_defs.txt"

# Output file
output_file = "csw24_crowdsourced.txt"

# Google Sheets ID
sheet_id = "1t4XMJiW684soWcETFBbA0ae2T00gOxhq-CARGCR00yc"

def download_public_google_sheet_as_tsv(sheet_id, output_file):
    """Download a public Google Sheets file as a TSV."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv"
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'w', newline='', encoding='utf-8') as tsv_file:
            tsv_file.write(response.text)
    else:
        raise Exception(f"Failed to download sheet. Status code: {response.status_code}")

def load_csw24_words(file_path):
    """Load words from csw24.txt into a sorted list."""
    with open(file_path, "r") as file:
        words = sorted(line.strip() for line in file)
        print(f"Number of CSW24 words loaded: {len(words)}")
        return words

def load_csw21_definitions(file_path):
    """Load word definitions from csw21_with_defs.txt into a dictionary."""
    definitions = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row:
                word, definition = row[0], row[1]
                definitions[word] = definition
    return definitions

def load_updated_definitions(tsv_file):
    """Load updated definitions from the downloaded TSV file into a dictionary."""
    definitions = {}
    with open(tsv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if len(row) < 6:
                sys.exit("Fatal error: Downloaded TSV does not have at least 6 columns.")
            word, definition = row[0].strip(), row[5].strip()
            if word and definition:
                definitions[word] = definition
    return definitions

def create_csw24_dict(csw24_words, csw21_definitions, updated_definitions):
    """Create a dictionary of CSW24 words to definitions."""
    csw24_dict = {}
    used_words = set()

    for word in csw24_words:
        if word in updated_definitions:
            csw24_dict[word] = updated_definitions[word]
            used_words.add(word)
        elif word in csw21_definitions:
            csw24_dict[word] = csw21_definitions[word]
            used_words.add(word)
        else:
            sys.exit(f"Fatal error: Missing definition for word '{word}'")

    unused_csw21_words = set(csw21_definitions.keys()) - used_words
    if unused_csw21_words:
        print("Unused words from CSW21 definitions:")
        for word in sorted(unused_csw21_words):
            print(word)

    return csw24_dict

def write_csw24_to_file(csw24_dict, output_file):
    """Write the CSW24 dictionary to a file, tab-delimited."""
    with open(output_file, "w", encoding="utf-8") as file:
        for word, definition in sorted(csw24_dict.items()):
            file.write(f"{word}\t{definition}\n")
    print(f"Number of rows written to {output_file}: {len(csw24_dict)}")

def main():
    # Temporary file for the downloaded sheet
    tsv_file = "updated_definitions.tsv"

    # Download the Google Sheet as a TSV file
    try:
        download_public_google_sheet_as_tsv(sheet_id, tsv_file)
    except Exception as e:
        sys.exit(str(e))

    # Load words and definitions
    csw24_words = load_csw24_words(csw24_path)
    csw21_definitions = load_csw21_definitions(csw21_with_defs_path)
    updated_definitions = load_updated_definitions(tsv_file)

    # Create the CSW24 dictionary
    csw24_dict = create_csw24_dict(csw24_words, csw21_definitions, updated_definitions)

    # Write the CSW24 dictionary to the output file
    write_csw24_to_file(csw24_dict, output_file)

if __name__ == "__main__":
    main()
