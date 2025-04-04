import argparse
import csv

def read_csv(file_path):
    """Reads a CSV file and returns a dictionary with keys as identifiers and values as floats."""
    data = {}
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                key, value = row[0].strip(), float(row[1])
                data[key] = value
    return data

def compute_differences(data1, data2):
    """Computes the differences between two dictionaries."""
    differences = {}
    for key in data1.keys() & data2.keys():
        differences[key] = (data1[key], data2[key], data2[key] - data1[key])
    return differences

def main():
    parser = argparse.ArgumentParser(description='Compare two CSV files and find top N differences.')
    parser.add_argument('file1', help='First CSV file')
    parser.add_argument('file2', help='Second CSV file')
    parser.add_argument('N', type=int, help='Number of top differences to display')
    parser.add_argument('--smallest', action='store_true', help='Display smallest absolute differences instead of biggest differences')
    args = parser.parse_args()

    data1 = read_csv(args.file1)
    data2 = read_csv(args.file2)

    differences = compute_differences(data1, data2)
    sorted_diffs = sorted(differences.items(), key=lambda x: abs(x[1][2])) if args.smallest else sorted(differences.items(), key=lambda x: x[1][2])

    print(f"Top {args.N} negative differences:")
    print(f"{'Key':<10} {args.file1:<15} {args.file2:<15} {'Difference':<15}")
    for key, (val1, val2, diff) in sorted_diffs[:args.N]:
        print(f"{key:<10} {val1:<15.6f} {val2:<15.6f} {diff:<15.6f}")

    print(f"\nTop {args.N} positive differences:")
    print(f"{'Key':<10} {args.file1:<15} {args.file2:<15} {'Difference':<15}")
    for key, (val1, val2, diff) in sorted_diffs[-args.N:][::-1]:
        print(f"{key:<10} {val1:<15.6f} {val2:<15.6f} {diff:<15.6f}")

if __name__ == '__main__':
    main()
