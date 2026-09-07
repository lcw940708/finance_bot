import os
import requests
from datetime import datetime

# ==========================================
# 1. 抓取財經數據 (以 Yahoo Finance 比特幣/指數為例)
# ==========================================
def fetch_market_data():
    try:
        # 使用 Yahoo Finance 公開 API 抓取 Bitcoin (BTC-USD) 數據
        url = "https://query1.finance.today/v8/finance/chart/BTC-USD?interval=1d&range=1d" # 註：實際可用標準 yahoo finance api
        # 為了更穩定，示範用公開可靠嘅 CoinGecko 免費 API 抓取比特幣現價同 24 小時升跌幅
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']
        
        market_info = (
            f"比特幣 (BTC): ${btc_price:,.2f} USD (24小時變幅: {btc_change:.2f}%) | "
            f"以太幣 (ETH): ${eth_price:,.2f} USD (24小時變幅: {eth_change:.2f}%)"
        )
        return market_info
    except Exception as e:
        print(f"抓取數據失敗: {e}")
        return None

# ==========================================
# 2. 調用 AI Worker 重寫成精簡短評
# ==========================================
def generate_ai_commentary(market_text):
    worker_url = os.environ.get("AI_WORKER_URL", "https://little-rice-42fa.lcw940708.workers.dev")
    
    prompt = f"以下是今日最新的加密貨幣市場數據：{market_text}。請用廣東話（香港俚語風格）寫一段 50 字左右嘅精簡市場速遞，點評今日市況。"
    
    payload = {
        "prompt": prompt,
        "tone": "casual",
        "lang": "hk"
    }
    
    try:
        res = requests.post(worker_url, json=payload, timeout=15)
        res_json = res.json()
        if res_json.get("success"):
            return res_json.get("content")
        else:
            return f"今日市場數據速遞：{market_text}"
    except Exception as e:
        print(f"AI 生成失敗: {e}")
        return f"今日市場數據速遞：{market_text}"

# ==========================================
# 3. 自動寫入 Markdown 檔案
# ==========================================
def save_to_markdown(content):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"posts/finance-{today}.md"
    
    # 確保 posts 目錄存在
    os.makedirs("posts", exist_ok=True)
    
    markdown_content = f"""---
title: "每日財經速遞 ({today})"
date: "{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
category: "finance"
---

{content}
"""

    # 如果今日檔案已經存在，可以用附加或覆蓋方式
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"成功生成檔案: {filename}")

if __name__ == "__main__":
    print("開始執行財經數據自動化...")
    data = fetch_market_data()
    if data:
        commentary = generate_ai_commentary(data)
        save_to_markdown(commentary)
    else:
        print("未有足夠數據，跳過執行。")