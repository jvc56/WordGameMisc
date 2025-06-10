import requests
import os
import json
import re
import argparse
from datetime import datetime
import csv
from io import StringIO

BASE_URL = "https://cross-tables.com/rest/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Script/1.0; +http://example.com/bot)",
    "Accept": "application/json"
}

def make_api_request(endpoint, params=None):
    headers = {
        "Accept": "*/*"  # Allow any response content type
    }
    try:
        response = requests.get(BASE_URL + endpoint, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # Handle CSV for allanno.php
        if endpoint == "allanno.php":
            decoded = response.content.decode('utf-8')
            reader = csv.DictReader(StringIO(decoded))
            return {"results": list(reader)}

        # Otherwise, assume JSON
        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Fatal error making API request to {endpoint}: {e}")
    except json.JSONDecodeError:
        raise RuntimeError(f"Fatal error: Could not decode JSON response from {endpoint}.")


def get_player_tournaments_in_range(player_id, start_date, end_date):
    print(f"Fetching tournament history for player ID: {player_id}...")
    data = make_api_request("player.php", params={"player": player_id, "results": 1})["player"]

    if "results" not in data:
        raise RuntimeError("Fatal error: 'results' field not in player data. Player ID may be invalid.")

    relevant_tournaments = {}
    for tourney in data["results"]:
        try:
            tourney_date_obj = datetime.strptime(tourney["date"], "%Y-%m-%d").date()
            if start_date <= tourney_date_obj <= end_date:
                tourney_name = tourney["tourneyname"].replace("/", "-").replace("\\", "-")
                relevant_tournaments[tourney["tourneyid"]] = {
                    "name": tourney_name,
                    "date": tourney["date"]
                }
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Fatal error processing tournament data: {e}")
            
    if not relevant_tournaments:
        raise RuntimeError("Fatal error: No tournaments found in the specified date range.")

    print(f"Found {len(relevant_tournaments)} tournaments in the specified date range.")
    return relevant_tournaments

def sanitize_filename(name):
    s = name.replace(' ', '')
    return re.sub(r'(?u)[^-\w.]', '', s)

def download_annotated_games(player_id, start_date, end_date, tournaments):
    """
    Downloads all annotated games for a player from a given list of tournaments.

    Args:
        player_id (int): The player's unique ID.
        tournaments (dict): A dictionary of relevant tournament IDs and their info.
    """
    print("Fetching all annotated games from the server... (This may take a moment)")
    data = make_api_request("allanno.php")
    if not data or "results" not in data:
        raise RuntimeError("Fatal error: Could not fetch annotated games.")

    all_games = data["results"]
    print(f"Processing {len(all_games)} total annotated games...")

    downloaded_count = 0
    tourney_ids = set(tournaments.keys())

    # Define root folder path using player ID and date range
    root_folder = f"{player_id}_annos_{start_date}_to_{end_date}"

    for raw_game in all_games:
        # Normalize all keys by stripping whitespace
        game = {k.strip(): v for k, v in raw_game.items()}

        try:
            game_tourney_id = game["tourneyID"]
            if game_tourney_id not in tourney_ids:
                # player did not player in this tourney or it is outside the date range
                continue

            url = game["url"].strip()
            if not url:
                # this game was not annotated
                continue

            player1_id = int(game["player1ID"])
            player2_id = int(game["player2ID"])

            if player_id not in (player1_id, player2_id):
                continue

            # Determine opponent's name
            if player_id == player1_id:
                opp_name = game["player2Name"].strip()
            else:
                opp_name = game["player1Name"].strip()

            tourney_info = tournaments[game_tourney_id]
            round_num = game["round"].strip()

            # Format folder name: YYYY-MM-DD-Tournament-Name
            folder_name = os.path.join(
                root_folder,
                f"{tourney_info['date']}-{sanitize_filename(tourney_info['name'])}"
            )
            os.makedirs(folder_name, exist_ok=True)

            # Format file name: r<round>_<opp_name>.gcg
            file_name = f"r{round_num}_{sanitize_filename(opp_name)}.gcg"
            file_path = os.path.join(folder_name, file_name)

            # Download and save the .gcg file
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            downloaded_count += 1
            print(f"  -> Saved game {game.get('ID')} to '{file_path}'")

        except (KeyError, ValueError, requests.RequestException) as e:
            raise RuntimeError(f"Fatal error processing game: {e}")

    if downloaded_count == 0:
        raise RuntimeError("No annotated games found for this player in the specified date range.")
    else:
        print(f"\nFinished. Downloaded {downloaded_count} annotated games.")

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date: '{s}'. Expected format is YYYY-MM-DD.")

def main():
    parser = argparse.ArgumentParser(
        description="Download annotated Scrabble games for a player from cross-tables.com.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("player_id", help="The unique numeric ID of the player.", type=int)
    parser.add_argument("start_date", help="The start date in YYYY-MM-DD format.", type=valid_date)
    parser.add_argument("end_date", help="The end date in YYYY-MM-DD format.", type=valid_date)

    args = parser.parse_args()

    print("--- Cross-Tables Annotated Game Downloader ---")

    if args.start_date > args.end_date:
        raise RuntimeError("Fatal error: The start date cannot be after the end date.")

    player_id = args.player_id
    relevant_tournaments = get_player_tournaments_in_range(player_id, args.start_date, args.end_date)
    download_annotated_games(player_id, args.start_date, args.end_date,relevant_tournaments)

if __name__ == "__main__":
    main()
