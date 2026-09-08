import os
import json
import re
import random
import requests
from datetime import datetime

# ==========================================
# 模組一：環球全景財經數據（指數 + 港股10大 + 美股10大）
# ==========================================
def run_finance_module(worker_url):
    print(">>> 開始執行環球全景財經數據模組...")
    
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
        "NVIDIA (NVDA)": "NVIDIA",
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

    indices_data = fetch_market_data(indices_symbols)
    hk_data = fetch_market_data(hk_stocks)
    us_data = fetch_market_data(us_stocks)

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

請用專業、精辟且具備實戰指導意義的廣東話撰寫一份詳盡的「環球全景財經與跨市聯動分析報告」。
"""
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "professional", "lang": "hk"}, timeout=60)
        res_json = res.json()
        if isinstance(res_json, dict):
            expert_content = res_json.get("content") or res_json.get("result") or "市場波動加劇，建議嚴控注碼。"
        else:
            expert_content = str(res_json)
    except Exception as e:
        print(f"財經模組錯誤: {e}")
        expert_content = "市場波動加劇，建議嚴控注碼。"

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    os.makedirs("posts", exist_ok=True)
    
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
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">專業財經專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">📈 環球指數與港美股 20 大巨頭深度日報</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200">
                <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-blue-600">📊 環球指數與加密貨幣</h3>
                {render_table_rows(indices_data)}
                {render_table_rows(crypto_data)}
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200">
                <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-purple-600">🇭🇰 港股 10 大熱門指標</h3>
                {render_table_rows(hk_data)}
            </div>
        </div>
        <div class="bg-white p-5 rounded-xl border border-slate-200">
            <h3 class="font-bold text-slate-900 mb-3 pb-2 border-b text-emerald-600">🇺🇸 美股 10 大科技巨頭</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6">
                {render_table_rows(us_data)}
            </div>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-8 space-y-6">
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
    prompt = "請為今日香港網民生成剛好 10 個不同範疇的熱門搜尋話題，並逐一用貼地、幽默的廣東話進行迷因解構報告。"
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "casual", "lang": "hk"}, timeout=60)
        res_json = res.json()
        if isinstance(res_json, dict):
            trends_content = res_json.get("content") or res_json.get("result") or "今日網絡迷因討論熱烈！"
        else:
            trends_content = str(res_json)
    except Exception as e:
        print(f"潮流模組錯誤: {e}")
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
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-full">潮流與迷因專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">🔥 今日 10 大潮流熱搜與迷因解構</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline">← 返回主頁</a>
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
# 模組三：每日星座運程（榜首展示分數，其餘隨機亂排不顯示分數）
# ==========================================
def run_horoscope_module(worker_url):
    print(">>> 開始執行每日星座運程模組...")
    prompt = """
請為 12 個星座（白羊座、金牛座、雙子座、巨蟹座、獅子座、處女座、天秤座、天蠍座、射手座、摩羯座、水瓶座、雙魚座）編寫今日詳細運程。
必須嚴格以 JSON 格式回傳一個 Array，不要包含任何 markdown 程式碼標記（如 ```json），格式如下：
[
  {
    "sign": "星座名稱",
    "score": 95,
    "summary": "一句話總結今日整體運勢",
    "career": "事業與工作運詳細分析（廣東話，約50字）",
    "love": "愛情與人際關係詳細分析（廣東話，約50字）",
    "wealth": "財運與投資理財建議（廣東話，約50字）",
    "tip": "今日開運貼士與幸運顏色/數字"
  }
]
每個星座的 score 必須是 1 到 100 之間的整數，且其中一個必須最高以選出榜首。
"""
    horoscopes = []
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "casual", "lang": "hk"}, timeout=60)
        res_json = res.json()
        content = ""
        if isinstance(res_json, dict):
            content = res_json.get("content") or res_json.get("result") or ""
        else:
            content = str(res_json)
        
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            clean_content = match.group(0)
            horoscopes = json.loads(clean_content)
        else:
            raise ValueError("找不到合法的 JSON Array 結構")
            
    except Exception as e:
        print(f"星座模組解析失敗: {e}，啟用備用數據")
        signs = ["白羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"]
        for idx, s in enumerate(signs):
            horoscopes.append({
                "sign": s,
                "score": 98 - idx,
                "summary": "今日運勢平穩，心態決定一切。",
                "career": "工作按部就班，保持專注即可順利過關。",
                "love": "多聆聽伴侶或朋友意見，感情更融洽。",
                "wealth": "理財宜保守，切忌盲目跟風投機。",
                "tip": "開運顏色：藍色 | 幸運數字：7"
            })

    # 找出最高分作為榜首，其餘隨機亂排
    if horoscopes:
        horoscopes = sorted(horoscopes, key=lambda x: x.get('score', 0), reverse=True)
        top_one = horoscopes[0]
        rest_horoscopes = horoscopes[1:]
        random.shuffle(rest_horoscopes) # 亂排其餘星座
    else:
        top_one = {}
        rest_horoscopes = []

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"horoscope/horoscope-{today}.html"
    os.makedirs("horoscope", exist_ok=True)

    top_card_html = f"""
    <div class="bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-2xl p-8 shadow-lg space-y-4">
        <div class="flex justify-between items-center">
            <span class="text-xs font-bold bg-white text-amber-600 px-3 py-1 rounded-full shadow-xs">👑 今日最強運勢榜首</span>
            <span class="text-lg font-extrabold tracking-wider">運勢指數：{top_one.get('score')} 分</span>
        </div>
        <h2 class="text-3xl font-extrabold">{top_one.get('sign')}</h2>
        <p class="text-lg font-medium opacity-95">{top_one.get('summary')}</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t border-amber-400/50">
            <div class="bg-black/10 p-3 rounded-xl"><strong class="block text-xs uppercase tracking-wide opacity-80 mb-1">💼 事業運勢</strong><span class="text-sm">{top_one.get('career')}</span></div>
            <div class="bg-black/10 p-3 rounded-xl"><strong class="block text-xs uppercase tracking-wide opacity-80 mb-1">❤️ 愛情人際</strong><span class="text-sm">{top_one.get('love')}</span></div>
            <div class="bg-black/10 p-3 rounded-xl"><strong class="block text-xs uppercase tracking-wide opacity-80 mb-1">💰 財運理財</strong><span class="text-sm">{top_one.get('wealth')}</span></div>
        </div>
        <div class="text-xs bg-black/20 px-4 py-2 rounded-lg font-semibold inline-block">✨ 開運貼士：{top_one.get('tip')}</div>
    </div>
    """

    # 渲染其餘 11 個星座（不設分數、不設排名次序）
    cards_html = ""
    for item in rest_horoscopes:
        cards_html += f"""
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-3">
            <h3 class="text-xl font-bold text-slate-900">{item.get('sign')}</h3>
            <p class="text-sm font-semibold text-slate-600">{item.get('summary')}</p>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs text-slate-700 bg-slate-50 p-3 rounded-lg">
                <div><span class="font-bold text-slate-900">💼 事業：</span>{item.get('career')}</div>
                <div><span class="font-bold text-slate-900">❤️ 愛情：</span>{item.get('love')}</div>
                <div><span class="font-bold text-slate-900">💰 財運：</span>{item.get('wealth')}</div>
            </div>
            <p class="text-xs text-amber-700 bg-amber-50 p-2 rounded">✨ {item.get('tip')}</p>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日 12 星座運程速遞 - {today}</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full">星座運程專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">✨ 每日 12 星座運程速遞</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-8">
        <div>
            <h2 class="text-lg font-bold text-slate-900 mb-4">👑 今日最旺星座</h2>
            {top_card_html}
        </div>
        <div>
            <h2 class="text-lg font-bold text-slate-900 mb-4">📋 其他星座運程</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {cards_html}
            </div>
        </div>
    </main>
    <footer class="border-t py-6 text-center text-xs text-slate-400 bg-white">© 2026 星座運程專欄</footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"成功生成星座 HTML: {filename}")

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

    horoscope_posts = []
    if os.path.exists("horoscope"):
        for file in sorted(os.listdir("horoscope"), reverse=True):
            if file.endswith(".html"):
                horoscope_posts.append((file.replace("horoscope-", "").replace(".html", ""), f"horoscope/{file}"))

    finance_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-blue-500 bg-white transition"><span class="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded">財經專欄</span><h3 class="font-bold mt-1">環球全景與 20 大巨頭日報 ({d})</h3></a>' for d, p in finance_posts])
    trends_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-purple-500 bg-white transition"><span class="text-xs text-purple-600 bg-purple-50 px-2 py-0.5 rounded">潮流迷因</span><h3 class="font-bold mt-1">10大潮流熱搜與迷因解構 ({d})</h3></a>' for d, p in trends_posts])
    horoscope_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-amber-500 bg-white transition"><span class="text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded">星座運程</span><h3 class="font-bold mt-1">每日 12 星座運程速遞 ({d})</h3></a>' for d, p in horoscope_posts])

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自動化內容平台 - 財經、潮流與星座速遞</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b py-8 shadow-xs">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-3xl font-extrabold text-slate-900">📈 每日環球財經、潮流與星座速遞</h1>
            <p class="text-slate-500 mt-2">由 AI 驅動的自動化多元內容聚合平台</p>
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
        <div class="bg-white rounded-xl border p-6">
            <h2 class="text-lg font-bold mb-4 text-amber-600">✨ 最新星座運程</h2>
            <div class="space-y-3">{horoscope_html}</div>
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
    run_horoscope_module(worker_url)
    update_index_page()