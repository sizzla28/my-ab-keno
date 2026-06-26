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
    # ኤፒአዩ ካልሠራ በራሱ ዝም ብሎ 20 ቁጥሮችን ይመርጣል
    return sorted(random.sample(range(1, 81), 20))

def update_web_page(hot_numbers):
    # መጀመሪያ template.html መኖሩን ያረጋግጣል፤ ከሌለ ራሱ ይፈጥረዋል
    if not os.path.exists("template.html"):
        with open("template.html", "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <title>Winner's Mindset - Keno Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 15px; border: 2px solid #00ffcc; }
        h1 { color: #00ffcc; }
        .numbers-box { display: flex; justify-content: center; gap: 10px; margin: 25px 0; flex-wrap: wrap; }
        .number { background: #00ffcc; color: #121212; font-weight: bold; font-size: 20px; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>የአሸናፊ ስነ ልቦና</h1>
        <p>የኬኖ ቀጣይ ዙር ሊወጡ የሚችሉ (Hot) ቁጥሮች ትንበያ</p>
        <div class="numbers-box"></div>
        <p>የሰርቨር ማመሳሰያ ሰዓት፦ <br><span></span></p>
    </div>
</body>
</html>""")

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
