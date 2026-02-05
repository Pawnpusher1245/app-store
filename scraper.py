import requests
import pandas as pd
import datetime
import os

# CONFIGURATION
RSS_URL = "https://rss.applemarketingtools.com/api/v2/us/apps/top-free/50/apps.json"
CSV_FILE = "data.csv"

def fetch_data():
    # 1. Fetch JSON from Apple
    try:
        # We add a User-Agent so Apple doesn't block the bot
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        apps = data['feed']['results']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2. Prepare the new data
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    new_rows = []
    
    for rank, app in enumerate(apps, start=1):
        new_rows.append({
            "timestamp": timestamp,
            "rank": rank,
            "name": app['name'],
            "id": app['id'],
            "artist": app['artistName']
        })

    df_new = pd.DataFrame(new_rows)

    # 3. Load or Create CSV
    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(CSV_FILE, index=False)
        print(f"Updated {CSV_FILE}. Total rows: {len(df_combined)}")
    else:
        df_new.to_csv(CSV_FILE, index=False)
        print(f"Created {CSV_FILE}.")

if __name__ == "__main__":
    fetch_data()
