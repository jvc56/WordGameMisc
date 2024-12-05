import pandas as pd
import numpy as np

def calculate_score_stats(input_df):
    """
    Calculate score difference statistics across various dimensions
    """
    # Create a copy of the dataframe to avoid SettingWithCopyWarning
    df = input_df.copy()
    
    # Ensure date is parsed correctly and filter games on or after 2015-01-01
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2015-01-01']
    
    # Ensure numeric columns are converted correctly
    numeric_columns = ['winnerscore', 'loserscore', 'winneroldrating', 'loseroldrating']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculate score difference
    df['score_difference'] = df['winnerscore'] - df['loserscore']
    
    # Initialize results dictionary
    results = {}
    
    # Overall stats
    overall_stats = calculate_stats(df['score_difference'])
    results['Overall'] = {**overall_stats, 'total_games': len(df)}
    
    # Stats by lexicon
    lexicon_stats = {}
    for lexicon in df['lexicon'].unique():
        lexicon_df = df[df['lexicon'] == lexicon]
        lexicon_stats[lexicon] = calculate_stats(lexicon_df['score_difference'])
        lexicon_stats[lexicon]['total_games'] = len(lexicon_df)
    results['Lexicon'] = lexicon_stats
    
    # Stats by minimum rating thresholds
    rating_thresholds = range(0, 2100, 100)
    rating_stats = {}
    
    for threshold in rating_thresholds:
        # Combined lexicon stats for the threshold
        threshold_df = df[
            (df['winneroldrating'] >= threshold) & 
            (df['loseroldrating'] >= threshold)
        ]
        
        # Create a key for the threshold
        key = f'Min Rating {threshold}'
        
        if len(threshold_df) > 0:
            rating_stats[key] = {
                **calculate_stats(threshold_df['score_difference']),
                'total_games': len(threshold_df)
            }
        
        # Lexicon-specific stats for the threshold
        for lexicon in [0, 1]:
            lexicon_threshold_df = threshold_df[threshold_df['lexicon'] == lexicon]
            
            if len(lexicon_threshold_df) > 0:
                lexicon_key = f'Lexicon {lexicon}, Min Rating {threshold}'
                rating_stats[lexicon_key] = {
                    **calculate_stats(lexicon_threshold_df['score_difference']),
                    'total_games': len(lexicon_threshold_df)
                }
    
    results['Rating Thresholds'] = rating_stats
    
    return results

def calculate_stats(data):
    """
    Calculate mean, standard deviation for a series
    """
    return {
        'average': np.mean(data),
        'std_deviation': np.std(data)
    }

def print_results(results):
    """
    Print results in a readable format
    """
    print("Overall Statistics:")
    print(f"Average Score Difference: {results['Overall']['average']:.2f}")
    print(f"Standard Deviation: {results['Overall']['std_deviation']:.2f}")
    print(f"Total Games: {results['Overall']['total_games']}")
    print("\n")
    
    print("Lexicon Statistics:")
    for lexicon, stats in results['Lexicon'].items():
        print(f"Lexicon {lexicon}:")
        print(f"  Average Score Difference: {stats['average']:.2f}")
        print(f"  Standard Deviation: {stats['std_deviation']:.2f}")
        print(f"  Total Games: {stats['total_games']}")
    print("\n")
    
    print("Rating Threshold Statistics:")
    for key, stats in results['Rating Thresholds'].items():
        if stats['total_games'] > 0:
            print(f"{key}:")
            print(f"  Average Score Difference: {stats['average']:.2f}")
            print(f"  Standard Deviation: {stats['std_deviation']:.2f}")
            print(f"  Total Games: {stats['total_games']}")

# Main execution
if __name__ == "__main__":
    # Read the CSV file with low_memory=False to suppress dtype warning
    df = pd.read_csv('all_xt_games.csv', low_memory=False)
    
    # Calculate and print statistics
    results = calculate_score_stats(df)
    print_results(results)