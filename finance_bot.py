import os
import requests
from datetime import datetime

# ==========================================
# 1. 抓取財經數據與熱門迷因幣/市場熱搜
# ==========================================
def fetch_market_and_trends():
    try:
        # 抓取主流幣與熱門迷因幣數據 (例如 Dogecoin, Shiba Inu 作為迷因熱度指標)
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,shiba-inu&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']
        doge_price = data['dogecoin']['usd']
        doge_change = data['dogecoin']['usd_24h_change']
        
        btc_trend = "強勢上升 🚀" if btc_change > 2 else ("弱勢回調 📉" if btc_change < -2 else "窄幅震盪 ⚖️")
        eth_trend = "強勢上升 🚀" if eth_change > 2 else ("弱勢回調 📉" if eth_change < -2 else "窄幅震盪 ⚖️")
        doge_trend = "迷因狂熱 🔥" if doge_change > 4 else ("隨市調整 💤" if doge_change < -4 else "平穩橫盤 🧊")
        
        market_summary = {
            "btc_price": f"${btc_price:,.2f}",
            "btc_change": f"{btc_change:+.2f}%",
            "btc_trend": btc_trend,
            "eth_price": f"${eth_price:,.2f}",
            "eth_change": f"{eth_change:+.2f}%",
            "eth_trend": eth_trend,
            "doge_price": f"${doge_price:,.4f}",
            "doge_change": f"{doge_change:+.2f}%",
            "doge_trend": doge_trend,
        }
        return market_summary
    except Exception as e:
        print(f"抓取數據失敗: {e}")
        return None

# ==========================================
# 2. 調用 AI Worker 生成包含「潮流熱搜」的專家報告
# ==========================================
def generate_expert_commentary(m):
    worker_url = os.environ.get("AI_WORKER_URL", "https://little-rice-42fa.lcw940708.workers.dev")
    
    prompt = f"""
你是一位資深的加密貨幣市場分析師與迷因幣（Meme Coin）熱度追蹤專家。今日市場即時數據如下：
- 比特幣 (BTC)：{m['btc_price']} (24小時變幅: {m['btc_change']}，現況：{m['btc_trend']})
- 以太幣 (ETH)：{m['eth_price']} (24小時變幅: {m['eth_change']}，現況：{m['eth_trend']})
- 狗狗幣 (DOGE - 迷因熱度指標)：{m['doge_price']} (24小時變幅: {m['doge_change']}，現況：{m['doge_trend']})

請用專業且帶有香港地道風格、貼地幽默的廣東話撰寫一份詳盡的市場分析報告。內容必須包含以下四個部分：
1. 【市況解構】：分析比特幣與以太幣背後的資金流向。
2. 【潮流熱搜與迷因板塊（Trending Topics）】：點評當前社群熱話、散戶情緒、迷因幣（如 DOGE）嘅投機熱度及風險。
3. 【風險評級】：給出今日市場的整體風險評分。
4. 【專家操作建議】：針對短線與長線投資者給出具體部署。
"""
    
    payload = {
        "prompt": prompt,
        "tone": "professional",
        "lang": "hk"
    }
    
    try:
        res = requests.post(worker_url, json=payload, timeout=40)
        res_json = res.json()
        if res_json.get("success"):
            return res_json.get("content")
        else:
            print("AI 回應異常，啟動 Fallback...")
            return get_fallback_commentary(m)
    except Exception as e:
        print(f"AI 請求超時或失敗 ({e})，啟動 Fallback...")
        return get_fallback_commentary(m)

# ==========================================
# 2.1 Fallback 備用內容
# ==========================================
def get_fallback_commentary(m):
    return f"""
    【系統自動提示：AI 模組暫時繁忙，以下為自動生成的趨勢與數據摘要】

    1. 【市況解構】：
    比特幣報價 {m['btc_price']}（變幅：{m['btc_change']}），以太幣報價 {m['eth_price']}（變幅：{m['eth_change']}）。大市近期維持觀望格局，資金流向反覆。

    2. 【潮流熱搜與迷因板塊（Trending Topics）】：
    作為散戶風向標的 Dogecoin（DOGE）現報 {m['doge_price']}（變幅：{m['doge_change']}）。社群熱話近期聚焦於迷因幣的聯動反應與短線資金炒作，散戶情緒波動較大，需慎防過度追高。

    3. 【風險評級】：
    綜合評級：【中度至高風險】。迷因板塊與高槓桿合約交投頻繁，務必做好資金控管。

    4. 【專家操作建議】：
    - 短線炒家：嚴格執行止損，切勿盲目追逐社群迷因熱潮。
    - 長線投資者：建議聚焦主流幣種（BTC/ETH），以定期定額（DCA）穩健佈局為主。
    """

# ==========================================
# 3. 生成 HTML 文章檔案
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
    <title>加密貨幣市場深度分析與迷因熱搜速遞 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-full">🔥 潮流熱搜與深度專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">📈 每日市場解析與迷因風向標</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time} | 數據來源：CoinGecko API</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <!-- 數據與熱搜面板 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white p-5 rounded-xl shadow-xs border border-slate-200">
                <div class="text-xs font-medium text-slate-500 uppercase">比特幣 (BTC)</div>
                <div class="text-xl font-bold text-slate-900 mt-1">{m['btc_price']}</div>
                <div class="text-xs mt-2 font-semibold">變幅：<span class="{'text-emerald-600' if '-' not in m['btc_change'] else 'text-rose-600'}">{m['btc_change']}</span></div>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-xs border border-slate-200">
                <div class="text-xs font-medium text-slate-500 uppercase">以太幣 (ETH)</div>
                <div class="text-xl font-bold text-slate-900 mt-1">{m['eth_price']}</div>
                <div class="text-xs mt-2 font-semibold">變幅：<span class="{'text-emerald-600' if '-' not in m['eth_change'] else 'text-rose-600'}">{m['eth_change']}</span></div>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-xs border border-slate-200">
                <div class="text-xs font-medium text-purple-600 uppercase font-bold">🔥 迷因熱搜 (DOGE)</div>
                <div class="text-xl font-bold text-slate-900 mt-1">{m['doge_price']}</div>
                <div class="text-xs mt-2 font-semibold">變幅：<span class="{'text-emerald-600' if '-' not in m['doge_change'] else 'text-rose-600'}">{m['doge_change']}</span> ({m['doge_trend']})</div>
            </div>
        </div>

        <!-- 專家詳細分析內文 -->
        <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-8 space-y-6">
            <h2 class="text-xl font-bold text-slate-900 border-b border-slate-100 pb-4">💡 專家觀點與迷因熱話解構</h2>
            <div class="prose max-w-none text-slate-700 leading-relaxed space-y-4 whitespace-pre-line">
                {expert_content}
            </div>
            
            <div class="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-r-lg text-xs text-amber-800 mt-6">
                <strong>免責聲明：</strong> 本文內容僅供參考，不構成任何投資邀約或買賣建議。迷因幣（Meme Coins）波動極大，投資者應當自行承擔風險。
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
    
    print(f"成功生成附帶熱搜分析的 HTML 檔案: {filename}")
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
                <a href="{path}" class="block p-5 rounded-xl border border-slate-200 hover:border-purple-500 hover:shadow-sm bg-white transition">
                    <div class="flex justify-between items-center">
                        <span class="text-xs text-purple-600 font-semibold bg-purple-50 px-2.5 py-1 rounded">熱搜與深度分析</span>
                        <span class="text-xs text-slate-400">{date_str}</span>
                    </div>
                    <h3 class="font-bold text-slate-900 mt-2 text-lg">市場日報、迷因熱搜與實戰策略 ({date_str})</h3>
                    <p class="text-sm text-slate-500 mt-1">點擊查看今日主流幣表現、散戶迷因熱話追蹤及專業風險評級。</p>
                </a>"""

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日財經速遞 - 市場分析與潮流熱搜</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-8 shadow-xs">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-3xl font-extrabold text-slate-900 tracking-tight">📈 每日財經速遞</h1>
            <p class="text-slate-500 mt-2">結合加密貨幣即時數據、AI 深度解構與散戶潮流熱搜的自動化平台</p>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-6">
            <h2 class="text-lg font-bold text-slate-900 mb-4">最新市場報告與熱搜</h2>
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
    print("開始執行財經數據與熱搜自動化...")
    market_data = fetch_market_and_trends()
    if market_data:
        expert_commentary = generate_expert_commentary(market_data)
        save_to_html(expert_commentary, market_data)
    else:
        print("未有足夠數據，跳過執行。")