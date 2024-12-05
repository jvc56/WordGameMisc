import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
file_path = 'all_xt_games.csv'
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter games on or after 2015-01-01
df = df[df['date'] >= '2015-01-01']

# Calculate score difference
df['score_diff'] = abs(df['winnerscore'] - df['loserscore'])

# Function to calculate stats
def calculate_stats(group):
    average = group['score_diff'].mean()
    std_dev = group['score_diff'].std()
    count = len(group)
    return average, std_dev, count

# Thresholds for minimum old rating
thresholds = range(1200, 2001, 100)

# Initialize a results list for all combinations
results = []

# Iterate over lexicon groups
lexicon_groups = df.groupby('lexicon')
for lexicon, group in lexicon_groups:
    print(f"\nLexicon {lexicon}:")

    # Iterate over thresholds
    for threshold in thresholds:
        filtered = group[(group['winneroldrating'] >= threshold) & (group['loseroldrating'] >= threshold)]
        if not filtered.empty:
            avg, std, count = calculate_stats(filtered)
            results.append((lexicon, threshold, avg, std, count))
            print(f"  Threshold >= {threshold}: Avg = {avg:.2f}, StdDev = {std:.2f}, Count = {count}")
        else:
            results.append((lexicon, threshold, None, None, 0))
            print(f"  Threshold >= {threshold}: No games (Count = 0)")

# Convert results to a DataFrame for easier handling
results_df = pd.DataFrame(results, columns=['Lexicon', 'Threshold', 'Average Score Diff', 'StdDev Score Diff', 'Game Count'])

# Save the results to a CSV file (optional)
output_path = 'score_diff_stats_by_lexicon_and_threshold_filtered.csv'
results_df.to_csv(output_path, index=False)
print(f"\nResults saved to {output_path}")
