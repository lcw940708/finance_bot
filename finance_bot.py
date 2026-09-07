import os
import requests
from datetime import datetime

# ==========================================
# 1. 抓取財經數據並進行初步量化分析
# ==========================================
def fetch_and_analyze_market():
    try:
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']
        
        # 專家級數據特徵萃取
        btc_trend = "強勢上升 🚀" if btc_change > 2 else ("弱勢回調 📉" if btc_change < -2 else "窄幅震盪 ⚖️")
        eth_trend = "強勢上升 🚀" if eth_change > 2 else ("弱勢回調 📉" if eth_change < -2 else "窄幅震盪 ⚖️")
        
        market_summary = {
            "btc_price": f"${btc_price:,.2f}",
            "btc_change": f"{btc_change:+.2f}%",
            "btc_trend": btc_trend,
            "eth_price": f"${eth_price:,.2f}",
            "eth_change": f"{eth_change:+.2f}%",
            "eth_trend": eth_trend,
        }
        return market_summary
    except Exception as e:
        print(f"抓取數據失敗: {e}")
        return None

# ==========================================
# 2. 調用 AI Worker 生成「財經專家級」詳盡分析
# ==========================================
def generate_expert_commentary(m):
    worker_url = os.environ.get("AI_WORKER_URL", "https://little-rice-42fa.lcw940708.workers.dev")
    
    # 建立高質素、結構化嘅專業 Prompt
    prompt = f"""
你是一位資深的加密貨幣市場分析師與風險管理專家。今日市場即時數據如下：
- 比特幣 (BTC)：{m['btc_price']} (24小時變幅: {m['btc_change']}，現況：{m['btc_trend']})
- 以太幣 (ETH)：{m['eth_price']} (24小時變幅: {m['eth_change']}，現況：{m['eth_trend']})

請用專業、客觀且具備實戰指導意義的廣東話（金融專業語調帶點貼地風格）撰寫一份詳盡的市場分析報告。內容必須包含以下三個部分：
1. 【市況解構】：分析目前比特幣與以太幣的走勢背後可能反映的資金動向或市場情緒。
2. 【風險評級】：給出今日市場的整體風險評分（例如：高風險、中度觀望、合適分段吸納等）。
3. 【專家操作建議】：針對短線交易者與長線投資者分別給出具體的部署建議（切記加上合適的風險提示）。
"""
    
    payload = {
        "prompt": prompt,
        "tone": "professional",
        "lang": "hk"
    }
    
    try:
        res = requests.post(worker_url, json=payload, timeout=60)
        res_json = res.json()
        if res_json.get("success"):
            return res_json.get("content")
        else:
            return "暫時無法透過 AI 生成深度分析，請參考下方即時客觀數據。"
    except Exception as e:
        print(f"AI 生成失敗: {e}")
        return "AI 伺服器連接超時，請稍後重試。"

# ==========================================
# 3. 生成排版精美且符合 AdSense 結構的 HTML 文章
# ==========================================
def save_to_html(expert_content, m):
    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    
    os.makedirs("posts", exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>專業加密貨幣市場深度分析與操作建議 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">專業財經專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">📈 每日加密貨幣深度市場解析</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time} | 數據來源：CoinGecko API</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <!-- 數據面板 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-white p-5 rounded-xl shadow-xs border border-slate-200">
                <div class="text-sm font-medium text-slate-500">比特幣 (BTC / USD)</div>
                <div class="text-2xl font-bold text-slate-900 mt-1">{m['btc_price']}</div>
                <div class="text-sm mt-2 font-semibold">變幅：<span class="{'text-emerald-600' if '-' not in m['btc_change'] else 'text-rose-600'}">{m['btc_change']}</span> ({m['btc_trend']})</div>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-xs border border-slate-200">
                <div class="text-sm font-medium text-slate-500">以太幣 (ETH / USD)</div>
                <div class="text-2xl font-bold text-slate-900 mt-1">{m['eth_price']}</div>
                <div class="text-sm mt-2 font-semibold">變幅：<span class="{'text-emerald-600' if '-' not in m['eth_change'] else 'text-rose-600'}">{m['eth_change']}</span> ({m['eth_trend']})</div>
            </div>
        </div>

        <!-- 專家詳細分析內文 -->
        <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-8 space-y-6">
            <h2 class="text-xl font-bold text-slate-900 border-b border-slate-100 pb-4">💡 專家觀點與操盤建議</h2>
            <div class="prose max-w-none text-slate-700 leading-relaxed space-y-4 whitespace-pre-line">
                {expert_content}
            </div>
            
            <div class="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-r-lg text-xs text-amber-800 mt-6">
                <strong>免責聲明：</strong> 本文內容僅供參考，不構成任何投資邀約、買賣建議或擔保。加密貨幣市場波動極大，投資者應獨立評估風險並自負盈虧。
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-200 py-6 text-center text-xs text-slate-400 bg-white">
        <p>© 2026 每日財經速遞. Powered by GitHub Actions & Vercel.</p>
    </footer>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"成功生成專家級 HTML 檔案: {filename}")
    update_index_page(today)

# ==========================================
# 4. 自動更新主頁 index.html
# ==========================================
def update_index_page(today):
    index_path = "index.html"
    posts = []
    
    if os.path.exists("posts"):
        for file in sorted(os.listdir("posts"), reverse=True):
            if file.endswith(".html"):
                date_str = file.replace("finance-", "").replace(".html", "")
                posts.append((date_str, f"posts/{file}"))

    list_items_html = ""
    for date_str, path in posts:
        list_items_html += f"""
                <a href="{path}" class="block p-5 rounded-xl border border-slate-200 hover:border-blue-500 hover:shadow-sm bg-white transition">
                    <div class="flex justify-between items-center">
                        <span class="text-xs text-blue-600 font-semibold bg-blue-50 px-2.5 py-1 rounded">專家深度分析</span>
                        <span class="text-xs text-slate-400">{date_str}</span>
                    </div>
                    <h3 class="font-bold text-slate-900 mt-2 text-lg">加密貨幣市場日報與實戰策略 ({date_str})</h3>
                    <p class="text-sm text-slate-500 mt-1">點擊查看今日比特幣與以太幣的詳細數據、風險評級及專業操盤建議。</p>
                </a>"""

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日財經速遞 - 專業市場分析與投資策略</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-8 shadow-xs">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">📈 每日財經速遞</h1>
            <p class="text-slate-500 mt-2">由 AI 驅動的自動化加密貨幣市場監測、數據分析與實戰策略平台</p>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-6">
            <h2 class="text-lg font-bold text-slate-900 mb-4">最新市場分析報告</h2>
            <div id="post-list" class="space-y-4">
                {list_items_html}
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-200 py-6 text-center text-xs text-slate-400 bg-white">
        <p>© 2026 每日財經速遞. Powered by GitHub Actions & Vercel.</p>
    </footer>
</body>
</html>
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print("成功自動更新 index.html 列表！")

if __name__ == "__main__":
    print("開始執行專業財經自動化分析...")
    market_data = fetch_and_analyze_market()
    if market_data:
        expert_commentary = generate_expert_commentary(market_data)
        save_to_html(expert_commentary, market_data)
    else:
        print("未有足夠數據，跳過執行。")
