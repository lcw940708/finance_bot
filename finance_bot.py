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
    
    prompt = f"以下是今日最新的加密貨幣市場數據：{market_text}。請用廣東話（香港俚語風格）寫一段 500 字左右嘅精簡市場速遞，點評今日市況。"
    
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
# 3. 生成獨立的 HTML 文章檔案
# ==========================================
def save_to_html(content, raw_data):
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    
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
    update_index_page(today)

# ==========================================
# 4. 自動更新主頁 index.html
# ==========================================
def update_index_page(today):
    index_path = "index.html"
    
    # 掃描 posts 目錄底下所有 html 檔案
    posts = []
    if os.path.exists("posts"):
        for file in sorted(os.listdir("posts"), reverse=True):
            if file.endswith(".html"):
                date_str = file.replace("finance-", "").replace(".html", "")
                posts.append((date_str, f"posts/{file}"))

    # 組合所有文章列表的 HTML 項目
    list_items_html = ""
    for date_str, path in posts:
        list_items_html += f"""
                <a href="{path}" class="block p-4 rounded-lg border border-gray-100 hover:border-blue-500 hover:bg-blue-50/50 transition">
                    <span class="text-xs text-blue-600 font-medium bg-blue-50 px-2 py-0.5 rounded">財經速遞</span>
                    <h3 class="font-medium text-gray-900 mt-1">每日財經速遞 ({date_str})</h3>
                    <p class="text-sm text-gray-500 mt-1">點擊查看當日的市場即時數據與 AI 短評。</p>
                </a>"""

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日財經速遞 - AI 自動化市場速遞</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-800 font-sans min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 py-6 shadow-sm">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-gray-900">📈 每日財經速遞</h1>
            <p class="text-sm text-gray-500 mt-1">由 AI 自動監測與生成的市場即時速遞</p>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-800 mb-4">最新文章列表</h2>
            
            <div id="post-list" class="space-y-3">
                {list_items_html}
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-200 py-6 text-center text-xs text-gray-400">
        <p>© 2026 每日財經速遞. Powered by GitHub Actions & Vercel.</p>
    </footer>
</body>
</html>
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("成功自動更新 index.html 列表！")

if __name__ == "__main__":
    print("開始執行財經數據自動化...")
    data = fetch_market_data()
    if data:
        commentary = generate_ai_commentary(data)
        save_to_html(commentary, data)
    else:
        print("未有足夠數據，跳過執行。")
