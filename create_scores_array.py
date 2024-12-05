import pandas as pd
import argparse
import shutil
import os

def generate_score_difference_array(input_df, min_rating, start_date, scaling_factor):
    """
    Generate a sorted array of score differences with proportional frequency based on a scaling factor.
    """
    # Create a copy of the dataframe
    df = input_df.copy()
    
    # Ensure date and numeric columns are converted correctly
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['winnerscore', 'loserscore', 'winneroldrating', 'loseroldrating']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter games based on the start date and minimum rating
    df_filtered = df[
        (df['date'] >= start_date) & 
        (df['winneroldrating'] >= min_rating) & 
        (df['loseroldrating'] >= min_rating)
    ].copy()  # Explicitly create a copy to avoid SettingWithCopyWarning
    
    # Calculate score difference
    df_filtered.loc[:, 'score_difference'] = df_filtered['winnerscore'] - df_filtered['loserscore']
    
    # Count frequency of score differences
    score_diff_counts = df_filtered['score_difference'].value_counts()
    total_games = len(df_filtered)
    
    # Print out all score difference frequencies sorted by score difference
    print("Score Difference Frequencies:")
    print("Score Difference | Count | Percentage | Scaled Count")
    print("-" * 40)
    
    # Sort by score difference
    for diff in sorted(score_diff_counts.index):
        count = score_diff_counts[diff]
        scaled_count = round(count / scaling_factor)
        percentage = (count / total_games) * 100
        print(f"{diff:14d} | {count:5d} | {percentage:6.2f}% | {scaled_count:5d}")
    
    print(f"\nTotal games (min rating {min_rating}): {total_games}")

    # Calculate the number of instances for each score difference in the Go array based on scaling factor
    score_diff_instances = {}
    for diff, count in score_diff_counts.items():
        instances = round(count / scaling_factor)  # Number of times score diff should appear in Go array
        score_diff_instances[diff] = instances
    
    # Create the final array based on calculated instances
    result_array = []
    
    for score_diff, instances in sorted(score_diff_instances.items()):
        # Add instances to the result array
        result_array.extend([score_diff] * instances)
    
    print(f"\n Final array length: {len(result_array)}")

    # Ensure the array is sorted
    result_array.sort()
    
    return result_array, total_games, score_diff_counts

def generate_go_array_literal(score_diff_array):
    """
    Generate a Go file with a function that returns an array literal
    from the score difference array.
    """
    go_literal = """package standings

func GetScoreDifferences() []uint64 {
    return []uint64{
"""
    
    # Write array elements, 10 per line for readability
    for i, diff in enumerate(score_diff_array):
        # Add a comma and newline every 10 elements
        line_end = ',\n' if (i + 1) % 10 == 0 else ', '
        go_literal += f" {diff}{line_end}"
    
    go_literal += "    }\n}\n"
    
    return go_literal

# Main execution
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate a score difference array.")
    parser.add_argument("min_rating", type=int, help="Minimum rating to filter games.")
    parser.add_argument("start_date", help="Start date to filter games (YYYY-MM-DD).")
    parser.add_argument("scaling_factor", type=float, help="Scaling factor for determining score diff occurrences.")
    args = parser.parse_args()
    
    # Hard-coded CSV file
    input_csv = 'all_xt_games.csv'
    
    # Read the CSV file
    df = pd.read_csv(input_csv, low_memory=False)
    
    # Generate score difference array
    score_diff_array, total_games, score_diff_counts = generate_score_difference_array(
        df, args.min_rating, args.start_date, args.scaling_factor
    )
    
    # Generate Go array literal
    go_array_literal = generate_go_array_literal(score_diff_array)
    
    # Write to the Go file
    filename = 'score_differences.go'
    with open(filename, 'w') as f:
        f.write(go_array_literal)
    shutil.copy(filename, os.path.expandvars('$HOME/liwords/pkg/pair/standings/' + filename))
