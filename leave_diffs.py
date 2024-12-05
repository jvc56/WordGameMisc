import argparse
import pandas as pd
import os

def compare_csv(csv1, csv2):
    # Extract basenames for header and output filename
    basename1 = os.path.basename(csv1)
    basename2 = os.path.basename(csv2)

    # Extract base names without extensions
    base1 = os.path.splitext(basename1)[0]
    base2 = os.path.splitext(basename2)[0]

    # Load CSV files into DataFrames
    df1 = pd.read_csv(csv1, header=None, names=['leave', 'value'])
    df2 = pd.read_csv(csv2, header=None, names=['leave', 'value'])

    # Merge DataFrames on 'leave' column
    merged_df = pd.merge(df1, df2, on='leave', suffixes=('_csv1', '_csv2'), how='outer', indicator=True)

    # Check for mismatched leaves
    mismatched_df = merged_df[merged_df['_merge'] != 'both']
    if not mismatched_df.empty:
        print("Error: The following leaves do not match between the two files:")
        print(mismatched_df[['leave', '_merge']])
        raise ValueError("Mismatch detected between the CSV files")

    # Remove '_merge' column after check
    merged_df = merged_df.drop(columns=['_merge'])

    # Calculate the difference
    merged_df['diff'] = merged_df['value_csv1'].fillna(0) - merged_df['value_csv2'].fillna(0)

    # Sort by absolute difference
    merged_df = merged_df.sort_values(by='diff', key=abs, ascending=False)

    # Rearrange columns
    result_df = merged_df[['leave', 'diff', 'value_csv1', 'value_csv2']]

    # Output filename using basenames
    output_filename = f"{base1}_vs_{base2}.csv"

    # Print output filename for verification
    print(f"Output filename: {output_filename}")

    # Write result to CSV with column spacing
    result_df.to_csv(output_filename, index=False, header=['leave', 'diff', basename1, basename2], float_format='%.6f')

def main():
    parser = argparse.ArgumentParser(description='Compare values between two CSV files and generate a result CSV.')
    parser.add_argument('csv1', type=str, help='Path to the first CSV file')
    parser.add_argument('csv2', type=str, help='Path to the second CSV file')
    
    args = parser.parse_args()
    
    # Ensure files exist
    if not os.path.isfile(args.csv1):
        raise FileNotFoundError(f"The file {args.csv1} does not exist.")
    if not os.path.isfile(args.csv2):
        raise FileNotFoundError(f"The file {args.csv2} does not exist.")
    
    compare_csv(args.csv1, args.csv2)

if __name__ == '__main__':
    main()
