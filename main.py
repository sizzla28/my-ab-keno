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
    # ትክክለኛና ንጹህ የኤችቲኤምኤል (HTML) ዲዛይን
    html_content = f"""<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Winner's Mindset - Keno Predictor</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0c0f12; color: #ffffff; text-align: center; padding: 20px; margin: 0; }}
        .container {{ max-width: 450px; margin: 40px auto; background: #161b22; padding: 30px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,255,204,0.1); border: 2px solid #00ffcc; }}
        h1 {{ color: #00ffcc; margin-bottom: 5px; font-size: 28px; }}
        .subtitle {{ color: #8b949e; font-size: 14px; margin-bottom: 30px; }}
        .numbers-box {{ display: flex; justify-content: center; gap: 12px; margin: 25px 0; flex-wrap: wrap; }}
        .number {{ background: linear-gradient(135deg, #00ffcc, #00b3ff); color: #0c0f12; font-weight: bold; font-size: 22px; width: 55px; height: 55px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,255,204,0.3); }}
        .footer-time {{ margin-top: 30px; border-top: 1px solid #21262d; padding-top: 15px; color: #8b949e; font-size: 13px; }}
        .time-val {{ color: #ffeb3b; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>የአሸናፊ ስነ ልቦና</h1>
        <div class="subtitle">የኬኖ ቀጣይ ዙር ሊወጡ የሚችሉ (Hot) ቁጥሮች ትንበያ</div>
        <div class="numbers-box">
            {"".join([f'<div class="number">{num}</div>' for num in hot_numbers])}
        </div>
        <div class="footer-time">
            የሰርቨር ማመሳሰያ ሰዓት፦ <br><span class="time-val">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        </div>
    </div>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

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
