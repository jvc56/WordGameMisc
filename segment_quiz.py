import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Split a quiz file into multiple smaller quizzes.")
    parser.add_argument("filename", type=str, help="The name of the input file containing the quiz data.")
    parser.add_argument("quiz_size", type=int, help="The number of questions per quiz.")
    return parser.parse_args()

def split_quizzes(filename, quiz_size):
    # Read the contents of the file
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Remove the initial "0" line if present
    if lines[0].strip() == "0":
        lines = lines[1:]
    
    # Split lines into quizzes of the specified size
    quizzes = [lines[i:i + quiz_size] for i in range(0, len(lines), quiz_size)]
    
    # Get the base filename without extension
    base_filename = os.path.splitext(filename)[0]
    
    # Write each quiz to a new file, starting each with "0\n"
    for idx, quiz in enumerate(quizzes):
        output_filename = f"{base_filename}_{idx + 1}.jqz"
        with open(output_filename, 'w') as output_file:
            output_file.write("0\n")  # Start each quiz with "0"
            output_file.writelines(quiz)

def main():
    args = parse_arguments()
    split_quizzes(args.filename, args.quiz_size)

if __name__ == "__main__":
    main()
