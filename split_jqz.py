import argparse

def split_file(input_file, n):
    # Read all lines from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    i = 1

    # Iteratively create new files with increasing line counts
    while (i * n) + 1 <= total_lines:
        new_file_name = f"{input_file}_{i}.txt"
        with open(new_file_name, 'w') as new_file:
            # Write the first i*N lines to the new file
            new_file.writelines(lines[:i * n + 1])
        print(f"Created: {new_file_name} with {i * n + 1} lines")
        i += 1

    # If the last file would contain fewer than N additional lines, write the rest
    if i * n + 1 > total_lines:
        new_file_name = f"{input_file}_{i}.txt"
        with open(new_file_name, 'w') as new_file:
            new_file.writelines(lines)
        print(f"Created: {new_file_name} with all {total_lines} lines")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a file into parts with increasing number of lines.')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('n', type=int, help='Number of lines to increment by')
    
    args = parser.parse_args()
    split_file(args.input_file, args.n)

