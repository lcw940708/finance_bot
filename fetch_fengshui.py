import os
import json
from datetime import datetime
import subprocess

def fetch_and_save_data():
    print(">>> 開始抓取最新風水數據...")
    
    # 呢度你可以換成去天文台、通勝 API 或其他網址抓取數據
    # 暫時以結構化 JSON 模擬實時數據
    today = datetime.now().strftime("%Y-%m-%d")
    fengshui_data = {
        "date": today,
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "auspicious_direction": "正東方（財神位）、正南方（喜神位）",
        "inavoidable_taboo": "正西方三煞，不宜動土",
        "lucky_element": "木、火",
        "daily_advice": "今日吉星高照，利於動工、簽約及投資部署，財運亨通。"
    }

    # 確保 data 資料夾存在
    os.makedirs("data", exist_ok=True)
    file_path = "data/fengshui.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(fengshui_data, f, ensure_ascii=False, indent=4)
    
    print(f"成功儲存數據至 {file_path}")
    return file_path

def git_commit_push():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "data/fengshui.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update fengshui data via GitHub Actions"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("成功自動 Push 最新數據到 GitHub！")
    except Exception as e:
        print(f"Git push 失敗（可能無變更或權限不足）: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
    git_commit_push()