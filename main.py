import os
import random
import requests
import pandas as pd
from datetime import datetime

DATA_FILE = "keno_history.csv"
API_URL = "https://els.tamcon.net.et/api/v2/gameManager/launch?game_id=cmka4xvdkytm6p25jaoep9ywu&user_id=6a259ab001ba0be9feb679e7&lang=am&currency=ETB"

def get_keno_numbers():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Android 14; Mobile; rv:152.0) Gecko/152.0 Firefox/152.0",
            "Accept": "application/json, text/plain, */*"
        }
        response = requests.get(API_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "results" in data["data"]:
                return sorted(data["data"]["results"][:20])
    except Exception as e:
        print(f"Error fetching data: {e}")
    return sorted(random.sample(range(1, 81), 20))

def update_web_page(hot_numbers):
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    numbers_html = "".join([f'<div class="number">{num}</div>' for num in hot_numbers])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = html.replace("", numbers_html)
    html = html.replace("", current_time)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def save_and_predict():
    live_numbers = get_keno_numbers()
    new_data = pd.DataFrame([live_numbers])
    
    if not os.path.exists(DATA_FILE):
        new_data.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

    df = pd.read_csv(DATA_FILE)
    all_numbers = df.values.flatten()
    hot_numbers = pd.Series(all_numbers).value_counts().head(5).index.tolist()
    
    update_web_page(hot_numbers)

if __name__ == "__main__":
    save_and_predict()
