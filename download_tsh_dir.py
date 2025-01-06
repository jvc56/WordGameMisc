import os
import sys
import requests

def download_file(url, output_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        with open(output_path, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <url> <directory> <division>")
        sys.exit(1)

    base_url = sys.argv[1]
    directory = sys.argv[2]
    division = sys.argv[3]

    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)

    # URLs for the files
    config_url = f"{base_url.rstrip('/')}/config.tsh"
    division_url = f"{base_url.rstrip('/')}/{division}.t"

    # Paths to save the files
    config_path = os.path.join(directory, "config.tsh")
    division_path = os.path.join(directory, f"{division}.t")

    # Download the files
    print(f"Downloading {config_url} to {config_path}...")
    download_file(config_url, config_path)

    print(f"Downloading {division_url} to {division_path}...")
    download_file(division_url, division_path)

    print("Files downloaded successfully.")

if __name__ == "__main__":
    main()

