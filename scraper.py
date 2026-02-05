import requests
import pandas as pd
import datetime
import os

# --- CONFIGURATION ---
URLS = {
    "Free": "https://rss.applemarketingtools.com/api/v2/us/apps/top-free/50/apps.json",
    "Paid": "https://rss.applemarketingtools.com/api/v2/us/apps/top-paid/50/apps.json"
}
CSV_FILE = "data.csv"

def fetch_data():
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    all_rows = []

    # Loop through both Free and Paid URLs
    for category, url in URLS.items():
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            apps = data['feed']['results']
            
            # Process each app
            for rank, app in enumerate(apps, start=1):
                all_rows.append({
                    "timestamp": timestamp,
                    "category": category, 
                    "rank": rank,
                    "name": app['name'],
                    "id": app['id'],
                    "artist": app['artistName']
                })
        except Exception as e:
            print(f"Error fetching {category} apps: {e}")

    if not all_rows:
        return

    # Convert to DataFrame
    df_new = pd.DataFrame(all_rows)

    # Save to CSV
    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(CSV_FILE, index=False)
        print(f"Updated {CSV_FILE}. Total rows: {len(df_combined)}")
    else:
        df_new.to_csv(CSV_FILE, index=False)
        print(f"Created {CSV_FILE} with {len(all_rows)} rows.")

if __name__ == "__main__":
    fetch_data()
