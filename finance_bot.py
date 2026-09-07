import os
import requests
from datetime import datetime

# ==========================================
# 1. 抓取財經數據 (CoinGecko API)
# ==========================================
def fetch_market_data():
    try:
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
# 3. 直接生成獨立的 HTML 檔案
# ==========================================
def save_to_html(content, raw_data):
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    
    # 確保 posts 目錄存在
    os.makedirs("posts", exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日財經速遞 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-gray-200 py-6 shadow-sm">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">📈 每日財經速遞</h1>
                <p class="text-sm text-gray-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
            <div>
                <h2 class="text-xs font-semibold text-blue-600 uppercase tracking-wider bg-blue-50 inline-block px-2.5 py-1 rounded">AI 市場短評</h2>
                <p class="text-lg text-gray-900 mt-3 leading-relaxed">{content}</p>
            </div>
            
            <hr class="border-gray-100">

            <div>
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider">原始數據摘要</h3>
                <div class="bg-gray-50 p-4 rounded-lg mt-2 text-sm font-mono text-gray-700 border border-gray-100">
                    {raw_data}
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-gray-200 py-6 text-center text-xs text-gray-400">
        <p>© 2026 每日財經速遞. Powered by GitHub Actions & Vercel.</p>
    </footer>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"成功生成 HTML 檔案: {filename}")

if __name__ == "__main__":
    print("開始執行財經數據自動化...")
    data = fetch_market_data()
    if data:
        commentary = generate_ai_commentary(data)
        save_to_html(commentary, data)
    else:
        print("未有足夠數據，跳過執行。")