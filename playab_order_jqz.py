import os
import argparse

def create_output_files(content, base_filename, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(100, len(content) + 1, 100):
        s = 0
        if i > 2000:
            s = i - 2000
        output_file = os.path.join(output_dir, f'{base_filename}_{s}_to_{i}.jqz')
        with open(output_file, 'w') as f:
            f.write("0\n")
            f.writelines(content[s:i])
    output_file = os.path.join(output_dir, f'{base_filename}_all.jqz')
    with open(output_file, 'w') as f:
        f.write("0\n")
        f.writelines(content[:])

def reorder_jqz_file(jqz_filename, playab_filename, base_filename, output_dir):
    # Read playability values from 'playab' file
    playab_data = {}
    with open(playab_filename, 'r') as playab_file:
        for line in playab_file:
            playability, word = line.strip().split()
            playab_data[word] = float(playability)
    
    # Read and reorder 'jqz' file based on playability values
    jqz_lines = []
    with open(jqz_filename, 'r') as jqz_file:
        # Process the first line
        first_line = jqz_file.readline()
        jqz_lines.append(first_line)
        
        # Process the remaining lines
        for line in jqz_file:
            parts = line.strip().split(';')
            if len(parts) != 3:
                raise ValueError(f"Line does not have 3 parts: {line}")
            
            word = parts[0]
            rank = playab_data.get(word, float('inf'))
            jqz_lines.append((-rank, line))
    
    sorted_jqz_lines = sorted(jqz_lines[1:], key=lambda x: x[0])
    jqz_line_without_rank = [t[1] for t in sorted_jqz_lines]
    create_output_files(jqz_line_without_rank, base_filename, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reorder jqz file based on playability values")
    parser.add_argument("jqz_file", help="Path to the jqz file")
    parser.add_argument("playab_file", help="Path to the playab file")
    parser.add_argument("base_filename", help="Path to the output reordered jqz file")
    parser.add_argument('output_dir', type=str, help='Output directory path')

    args = parser.parse_args()
    reorder_jqz_file(args.jqz_file, args.playab_file, args.base_filename, args.output_dir)
    print("jqz file reordered successfully!")
