import os
import requests
from datetime import datetime

# ==========================================
# 模組一：環球全景財經數據（指數 + 港股10大 + 美股10大）
# ==========================================
def run_finance_module(worker_url):
    print(">>> 開始執行環球全景財經數據模組...")
    
    # 1. 抓取加密貨幣數據 (CoinGecko)
    crypto_data = {}
    try:
        cg_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        res = requests.get(cg_url, timeout=10).json()
        btc_price = res['bitcoin']['usd']
        btc_change = res['bitcoin']['usd_24h_change']
        eth_price = res['ethereum']['usd']
        eth_change = res['ethereum']['usd_24h_change']
        
        crypto_data = {
            "BTC": f"${btc_price:,.2f} ({btc_change:+.2f}%)",
            "ETH": f"${eth_price:,.2f} ({eth_change:+.2f}%)"
        }
    except Exception as e:
        print(f"抓取加密貨幣失敗: {e}")
        crypto_data = {"BTC": "暫無數據", "ETH": "暫無數據"}

    # 2. 定義環球指數與港美股 10 大熱門標的
    indices_symbols = {
        "恒生指數 (HSI)": "^HSI",
        "恒生科技指數": "HSTECH.HK",
        "標普 500 (SPX)": "^GSPC",
        "納斯達克綜合指數": "^IXIC",
        "道瓊斯工業指數": "^DJI"
    }

    hk_stocks = {
        "騰訊控股 (0700.HK)": "0700.HK",
        "阿里巴巴 (9988.HK)": "9988.HK",
        "美團 (3690.HK)": "3690.HK",
        "小米集團 (1810.HK)": "1810.HK",
        "香港交易所 (0388.HK)": "0388.HK",
        "中國移動 (0941.HK)": "0941.HK",
        "友邦保險 (1299.HK)": "1299.HK",
        "建設銀行 (0939.HK)": "0939.HK",
        "滙豐控股 (0005.HK)": "0005.HK",
        "比亞迪股份 (1211.HK)": "1211.HK"
    }

    us_stocks = {
        "Apple (AAPL)": "AAPL",
        "NVIDIA (NVDA)": "NVDA",
        "Microsoft (MSFT)": "MSFT",
        "Alphabet/Google (GOOGL)": "GOOGL",
        "Amazon (AMZN)": "AMZN",
        "Meta (META)": "META",
        "Tesla (TSLA)": "TSLA",
        "Netflix (NFLX)": "NFLX",
        "AMD (AMD)": "AMD",
        "Intel (INTC)": "INTC"
    }

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    def fetch_market_data(target_dict):
        results = {}
        for name, sym in target_dict.items():
            try:
                yf_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=2d"
                res = requests.get(yf_url, headers=headers, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    meta = data['chart']['result'][0]['meta']
                    price = meta.get('regularMarketPrice')
                    prev_close = meta.get('chartPreviousClose')
                    if price and prev_close:
                        change_pct = ((price - prev_close) / prev_close) * 100
                        results[name] = f"{price:,.2f} ({change_pct:+.2f}%)"
                    else:
                        results[name] = "數據暫缺"
                else:
                    results[name] = "暫無報價"
            except Exception:
                results[name] = "連線逾時"
        return results

    print("正在抓取環球指數...")
    indices_data = fetch_market_data(indices_symbols)
    print("正在抓取港股 10 大熱門股...")
    hk_data = fetch_market_data(hk_stocks)
    print("正在抓取美股 10 大巨頭...")
    us_data = fetch_market_data(us_stocks)

    # 組裝成結構化的 Prompt 傳送給 AI
    prompt = f"""
你是一位頂級的環球宏觀經濟學家與資深基金經理。今日環球市場核心即時數據如下：

【主要市場指數】
{chr(10).join([f"- {k}: {v}" for k, v in indices_data.items()])}

【加密貨幣】
{chr(10).join([f"- {k}: {v}" for k, v in crypto_data.items()])}

【港股 10 大熱門指標股】
{chr(10).join([f"- {k}: {v}" for k, v in hk_data.items()])}

【美股 10 大科技與巨頭】
{chr(10).join([f"- {k}: {v}" for k, v in us_data.items()])}

請用專業、精辟且具備實戰指導意義的廣東話撰寫一份詳盡的「環球全景財經與跨市聯動分析報告」。內容必須包含：
1. 【總體經濟與美股科技巨頭走勢解構】
2. 【港股 10 大核心標的表現與資金流向評析】
3. 【加密貨幣與環球風險資產聯動】
4. 【具體操盤建議與風險評級】
"""
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "professional", "lang": "hk"}, timeout=60)
        print(f"財經模組 - 雲端 Worker 回應狀態碼: {res.status_code}")
        res_json = res.json()
        expert_content = res_json.get("content") if res_json.get("success") else "【系統提示：AI 模組繁忙】環球市場波動加劇，建議嚴控注碼、多元配置。"
    except Exception as e:
        print(f"財經模組 - 詳細錯誤原因: {e}")
        expert_content = "【系統提示：AI 模組繁忙】環球市場波動加劇，建議嚴控注碼、多元配置。"

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    os.makedirs("posts", exist_ok=True)
    
    # 建立前端呈現 HTML (精美表格展示所有股票數據)
    def render_table_rows(data_dict):
        return "".join([f'<div class="flex justify-between py-2 border-b border-slate-100 text-sm"><span class="font-medium text-slate-700">{k}</span><span class="font-bold text-slate-900">{v}</span></div>' for k, v in data_dict.items()])

    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>環球全景財經與港美股深度解析 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">專業財經專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">📈 環球指數與港美股 20 大巨頭深度日報</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-blue-600">📊 環球指數與加密貨幣</h3>
                {render_table_rows(indices_data)}
                {render_table_rows(crypto_data)}
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-purple-600">🇭🇰 港股 10 大熱門指標</h3>
                {render_table_rows(hk_data)}
            </div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
            <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-emerald-600">🇺🇸 美股 10 大科技巨頭</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6">
                {render_table_rows(us_data)}
            </div>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-8 space-y-6 shadow-xs">
            <h2 class="text-xl font-bold text-slate-900 border-b pb-4">💡 基金經理深度跨市解構</h2>
            <div class="prose max-w-none text-slate-700 leading-relaxed whitespace-pre-line">{expert_content}</div>
        </div>
    </main>
    <footer class="border-t py-6 text-center text-xs text-slate-400 bg-white">© 2026 環球財經速遞</footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"成功生成財經 HTML: {filename}")

# ==========================================
# 模組二：10 大潮流熱搜與迷因解構生成
# ==========================================
def run_trends_module(worker_url):
    print(">>> 開始執行潮流熱搜模組...")
    
    prompt = "請為今日香港網民生成剛好 10 個不同範疇的熱門搜尋話題（涵蓋城中熱話、生活、科技、港股美股動向等），並逐一用貼地、幽默的廣東話進行迷因解構報告。"
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "casual", "lang": "hk"}, timeout=60)
        print(f"潮流模組 - 雲端 Worker 回應狀態碼: {res.status_code}")
        res_json = res.json()
        trends_content = res_json.get("content") if res_json.get("success") else "今日網絡迷因討論熱烈！"
    except Exception as e:
        print(f"潮流模組 - 詳細錯誤原因: {e}")
        trends_content = "今日網絡迷因討論熱烈！"

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"trends/trend-{today}.html"
    os.makedirs("trends", exist_ok=True)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>10 大潮流熱搜與迷因解構 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-full">潮流與迷因專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">🔥 今日 10 大潮流熱搜與迷因解構</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="bg-white rounded-xl border border-slate-200 p-8 space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b pb-4">💡 10 大熱話與迷因深度解構</h2>
            <div class="prose max-w-none text-slate-700 leading-relaxed whitespace-pre-line">{trends_content}</div>
        </div>
    </main>
    <footer class="border-t py-6 text-center text-xs text-slate-400 bg-white">© 2026 潮流專欄</footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"成功生成潮流 HTML: {filename}")

# ==========================================
# 總控：統一更新主頁 index.html
# ==========================================
def update_index_page():
    finance_posts = []
    if os.path.exists("posts"):
        for file in sorted(os.listdir("posts"), reverse=True):
            if file.endswith(".html"):
                finance_posts.append((file.replace("finance-", "").replace(".html", ""), f"posts/{file}"))

    trends_posts = []
    if os.path.exists("trends"):
        for file in sorted(os.listdir("trends"), reverse=True):
            if file.endswith(".html"):
                trends_posts.append((file.replace("trend-", "").replace(".html", ""), f"trends/{file}"))

    finance_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-blue-500 bg-white transition"><span class="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded">財經專欄</span><h3 class="font-bold mt-1">環球全景與 20 大巨頭日報 ({d})</h3></a>' for d, p in finance_posts])
    trends_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-purple-500 bg-white transition"><span class="text-xs text-purple-600 bg-purple-50 px-2 py-0.5 rounded">潮流迷因</span><h3 class="font-bold mt-1">10大潮流熱搜與迷因解構 ({d})</h3></a>' for d, p in trends_posts])

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自動化內容平台 - 環球財經與潮流速遞</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b py-8 shadow-xs">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-3xl font-extrabold text-slate-900">📈 每日環球財經與潮流速遞</h1>
            <p class="text-slate-500 mt-2">由 AI 驅動的自動化環球全景分析與潮流熱話聚合平台</p>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-8">
        <div class="bg-white rounded-xl border p-6">
            <h2 class="text-lg font-bold mb-4 text-blue-600">📈 最新財經報告</h2>
            <div class="space-y-3">{finance_html}</div>
        </div>
        <div class="bg-white rounded-xl border p-6">
            <h2 class="text-lg font-bold mb-4 text-purple-600">🔥 最新潮流迷因</h2>
            <div class="space-y-3">{trends_html}</div>
        </div>
    </main>
    <footer class="border-t py-6 text-center text-xs text-slate-400 bg-white">© 2026 自動化內容平台</footer>
</body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    print("成功更新主頁 index.html！")

if __name__ == "__main__":
    worker_url = os.environ.get("AI_WORKER_URL") or "https://mainbot.lcw940708.workers.dev"
    run_finance_module(worker_url)
    run_trends_module(worker_url)
    update_index_page()