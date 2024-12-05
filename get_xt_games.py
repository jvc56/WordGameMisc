import time
import requests
import argparse
import csv
import os

# Define headers to be used for all API calls
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Script/1.0; +http://example.com/bot)",
    "Accept": "application/json"
}

def get_highest_game_id():
    """Retrieve the highest existing game ID using the info API."""
    url = "https://cross-tables.com/rest/info.php"
    print(f"Querying: {url}")  # Print querying message
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return int(data["maxgameid"])
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError:
        print("Error decoding JSON response.")
    return None  # Return None if there's an error

def query_games(min_id, max_id):
    """Query cross-tables.com for games in the given ID range, retrying up to 3 times on failure."""
    url = f"https://cross-tables.com/rest/games.php?minid={min_id}&maxid={max_id}"
    print(f"Querying: {url}")  # Print querying message
    max_retries = 10  # Maximum number of retries
    attempt = 0  # Current attempt count

    while attempt < max_retries:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()  # Raise an error for HTTP error responses
            
            # Check if the response content is empty
            if response.content.strip() == b"":  # Checking for empty response
                print("Received an empty response.")
                return []  # Return an empty list for no games
            
            data = response.json()  # Attempt to decode JSON
            return data["games"]

        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Request error: {e}. Attempt {attempt}/{max_retries}")
            
            if attempt == max_retries:
                print("Max retries reached. Exiting query.")
                return []  # Return an empty list after max retries
            else:
                # Optionally wait before retrying (e.g., 1 second)
                time.sleep(5)
        
        except ValueError:
            print("Error decoding JSON response.")
            return []  # Return an empty list if there's an error


def write_games_to_csv(games, filename):
    """Append the collected games to a CSV file."""
    # Define CSV headers based on the keys of the first game entry
    headers = games[0].keys()

    # Append mode for writing to CSV file
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write headers only if the file is new
        if file.tell() == 0:  # If file is empty, write headers
            writer.writeheader()
        
        writer.writerows(games)  # Write all games

    print(f"Wrote {len(games)} games to {filename}")

def collect_games(starting_id, num_games, output_file):
    """Collect games from cross-tables.com, starting from starting_id, until num_games is reached."""
    current_id = starting_id

    # Overwrite the existing CSV file if it exists
    if os.path.isfile(output_file):
        print(f"Overwriting existing file: {output_file}")

    # Create a new file by opening it in write mode
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        pass  # Just create/overwrite the file

    while num_games > 0:
        max_id = current_id - 1
        min_id = max(max_id - 999, 1)  # Query at most 1000 games at a time, ensuring min_id is at least 1
        if max_id > min_id:
            break
        batch = query_games(min_id, max_id)

        # Check if the batch is empty
        if not batch:
            print(f"No games found in range {min_id} to {max_id}. Continuing to next range.")
            current_id = min_id  # Move current_id down to continue querying lower IDs
            continue  # Skip to the next iteration if batch is empty

        # Update remaining number of games to collect
        num_to_write = min(len(batch), num_games)
        write_games_to_csv(batch[:num_to_write], output_file)
        num_games -= num_to_write
        current_id = min_id  # Move to the next range

    print(f"Finished collecting games. Total games requested: {num_games}.")


def main():
    parser = argparse.ArgumentParser(description="Retrieve games from cross-tables.com and save to CSV.")
    parser.add_argument("num_games", type=int, help="Number of games to retrieve")
    parser.add_argument("output_file", type=str, help="Output CSV filename")
    args = parser.parse_args()

    highest_game_id = get_highest_game_id()
    if highest_game_id is None:
        print("Could not retrieve the highest game ID.")
        return

    print(f"Highest existing game ID: {highest_game_id}")

    collect_games(highest_game_id, args.num_games, args.output_file)

if __name__ == "__main__":
    main()
