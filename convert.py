import requests
import json

# The URL you provided
JSON_URL = "https://raw.githubusercontent.com/hasanhabibmottakin/Z5/refs/heads/main/rest_api.json"
OUTPUT_FILE = "zee5_playlist.m3u"

def convert_to_m3u(url, output_filename):
    print(f"Downloading data from {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not isinstance(data, list):
            print("Error: JSON root is not a list.")
            return

        print(f"Found {len(data)} channels. creating M3U...")

        with open(output_filename, "w", encoding="utf-8") as f:
            # Write M3U Header
            f.write("#EXTM3U\n")
            
            for item in data:
                # Extract basic info
                name = item.get("name", "Unknown Channel")
                logo = item.get("logo", "")
                group = item.get("group", "Uncategorized")
                
                # Extract Source info
                source = item.get("source", {})
                stream_url = source.get("url", "")
                
                # Extract Headers (User-Agent)
                headers = source.get("headers", {})
                user_agent = headers.get("User-Agent", "")

                if stream_url:
                    # 1. Write the metadata line (#EXTINF)
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                    
                    # 2. Write VLC specific option (Optional, helps VLC player specifically)
                    if user_agent:
                        f.write(f'#EXTVLCOPT:http-user-agent={user_agent}\n')
                    
                    # 3. Write the URL
                    # We append |User-Agent=... to the URL. This is the standard way 
                    # for IPTV apps (Tivimate, OTT Navigator) to recognize headers.
                    if user_agent:
                        final_url = f"{stream_url}|User-Agent={user_agent}"
                    else:
                        final_url = stream_url
                        
                    f.write(f"{final_url}\n")

        print(f"Success! Playlist saved as: {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_to_m3u(JSON_URL, OUTPUT_FILE)
