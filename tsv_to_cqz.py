import sys
import requests
import re
import shutil

def process_tsv(file_name):
    try:
        # Open the input TSV file for reading
        with open(file_name, 'r') as tsv_file:
            # Create the output .cqz file
            output_file_name = file_name.replace('.tsv', '.cqz')
            with open(output_file_name, 'w') as cqz_file:
                cqz_file.write(f"0\n")
                for line in tsv_file:
                    # Check if the line has exactly one tab character
                    if line.count('\t') != 1:
                        sys.exit(f"Fatal error: Row has more than 1 tab - {line.strip()}")
                    
                    col1, col2 = line.strip().split('\t')

                    # Write to the .cqz file
                    cqz_file.write(f"0\t{col1}\t{col2}\n")
        return output_file_name
            
    except FileNotFoundError:
        sys.exit(f"Error: File {file_name} not found.")
    except Exception as e:
        sys.exit(f"An error occurred: {str(e)}")

def download_public_google_sheet_as_tsv(sheet_id, output_file):
    # Google Sheets API endpoint for public sheets
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv"
    
    # Make a request to the Google Sheets API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(output_file, 'w', newline='', encoding='utf-8') as tsv_file:
            tsv_file.write(response.text)
        print(f"Sheet downloaded and saved as {output_file}")
    else:
        print(f"Failed to download sheet. Status code: {response.status_code}")

if __name__ == "__main__":
    tsv_filename = "cpp_quiz.tsv"
    download_public_google_sheet_as_tsv("1GdHzMpIkZoRVfOWKCBNl-VEWFib7teuWIIxruemK6E0", tsv_filename)
    quiz_filename = process_tsv(tsv_filename)
    shutil.copy(quiz_filename, "/home/josh/Dropbox/DefQuizzes/" + quiz_filename)


    
