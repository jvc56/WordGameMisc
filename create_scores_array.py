import pandas as pd
import argparse

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
    
    # Ensure the array is sorted
    result_array.sort()
    
    return result_array, total_games, score_diff_counts

def generate_go_array_literal(score_diff_array):
    """
    Generate a Go array literal as a string from the score difference array.
    """
    go_literal = "package standings\n\nvar ScoreDifferences = []int{\n"
    
    # Write array elements, 10 per line for readability
    for i, diff in enumerate(score_diff_array):
        # Add a comma and newline every 10 elements
        line_end = ',\n' if (i+1) % 10 == 0 else ', '
        
        # Last element should not have a comma
        if i == len(score_diff_array) - 1:
            line_end = '\n'
        
        go_literal += f"{diff}{line_end}"
    
    go_literal += "}\n"
    
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
    with open('score_differences.go', 'w') as f:
        f.write(go_array_literal)
