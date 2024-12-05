import argparse

def parse_coco_results(file_path):
    players = {}
    results = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            round_num = int(parts[0])
            player1 = parts[1] + ' ' + parts[2]
            score1 = int(parts[3])
            player2 = parts[4] + ' ' + parts[5]
            score2 = int(parts[6])
            
            if player1 not in players:
                players[player1] = len(players) + 1
            if player2 not in players:
                players[player2] = len(players) + 1
            
            results.append((round_num, player1, score1, player2, score2))
    
    # Sort results by round number
    results.sort(key=lambda x: x[0])
    
    return players, results

def convert_to_t_format(players, results, output_path):
    player_games = {player: [] for player in players}
    player_scores = {player: [] for player in players}
    
    for round_num, player1, score1, player2, score2 in results:
        player_games[player1].append(players[player2])
        player_scores[player1].append(score1)
        player_games[player2].append(players[player1])
        player_scores[player2].append(score2)
    
    with open(output_path, 'w') as file:
        for player, index in sorted(players.items(), key=lambda item: item[1]):
            opponents = ' '.join(map(str, player_games[player]))
            scores = ' '.join(map(str, player_scores[player]))
            file.write(f'{player:<24} 1 {opponents}; {scores};\n')

def main():
    parser = argparse.ArgumentParser(description='Convert CoCo results text file to .t file format.')
    parser.add_argument('input_file', type=str, help='Path to the CoCo results text file')
    parser.add_argument('output_file', type=str, help='Path to the output .t file')
    
    args = parser.parse_args()
    
    players, results = parse_coco_results(args.input_file)
    convert_to_t_format(players, results, args.output_file)
    
    print(f'Conversion complete. Output written to {args.output_file}')

if __name__ == '__main__':
    main()
