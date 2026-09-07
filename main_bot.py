import os
import requests
from datetime import datetime

# ==========================================
# 模組一：財經數據分析與日報生成
# ==========================================
def run_finance_module(worker_url):
    print(">>> 開始執行財經數據模組...")
    try:
        api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']
        
        btc_trend = "強勢上升 🚀" if btc_change > 2 else ("弱勢回調 📉" if btc_change < -2 else "窄幅震盪 ⚖️")
        eth_trend = "強勢上升 🚀" if eth_change > 2 else ("弱勢回調 📉" if eth_change < -2 else "窄幅震盪 ⚖️")
        
        m = {
            "btc_price": f"${btc_price:,.2f}",
            "btc_change": f"{btc_change:+.2f}%",
            "btc_trend": btc_trend,
            "eth_price": f"${eth_price:,.2f}",
            "eth_change": f"{eth_change:+.2f}%",
            "eth_trend": eth_trend,
        }
    except Exception as e:
        print(f"抓取財經數據失敗: {e}")
        return

    prompt = f"""
你是一位資深的加密貨幣市場分析師與風險管理專家。今日市場即時數據如下：
- 比特幣 (BTC)：{m['btc_price']} (24小時變幅: {m['btc_change']}，現況：{m['btc_trend']})
- 以太幣 (ETH)：{m['eth_price']} (24小時變幅: {m['eth_change']}，現況：{m['eth_trend']})

請用專業、客觀且具備實戰指導意義的廣東話撰寫一份詳盡的市場分析報告。內容必須包含：
1. 【市況解構】
2. 【風險評級】
3. 【專家操作建議】
"""
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "professional", "lang": "hk"}, timeout=30)
        print(f"財經模組 - 雲端 Worker 回應狀態碼: {res.status_code}")
        print(f"財經模組 - 雲端 Worker 實際內容: {res.text}")
        
        res_json = res.json()
        expert_content = res_json.get("content") if res_json.get("success") else get_fallback_finance(m)
    except Exception as e:
        print(f"財經模組 - 詳細錯誤原因: {e}")
        expert_content = get_fallback_finance(m)

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"posts/finance-{today}.html"
    os.makedirs("posts", exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>專業加密貨幣市場深度分析 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">專業財經專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">📈 每日加密貨幣深度市場解析</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-white p-5 rounded-xl border border-slate-200">
                <div class="text-sm font-medium text-slate-500">比特幣 (BTC)</div>
                <div class="text-2xl font-bold text-slate-900 mt-1">{m['btc_price']}</div>
                <div class="text-sm mt-2">變幅：{m['btc_change']} ({m['btc_trend']})</div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200">
                <div class="text-sm font-medium text-slate-500">以太幣 (ETH)</div>
                <div class="text-2xl font-bold text-slate-900 mt-1">{m['eth_price']}</div>
                <div class="text-sm mt-2">變幅：{m['eth_change']} ({m['eth_trend']})</div>
            </div>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-8 space-y-6">
            <h2 class="text-xl font-bold text-slate-900 border-b pb-4">💡 專家觀點與操盤建議</h2>
            <div class="prose max-w-none text-slate-700 leading-relaxed whitespace-pre-line">{expert_content}</div>
        </div>
    </main>
    <footer class="border-t py-6 text-center text-xs text-slate-400 bg-white">© 2026 每日財經速遞</footer>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"成功生成財經 HTML: {filename}")

def get_fallback_finance(m):
    return f"【系統提示：AI 模組繁忙】今日 BTC 報價 {m['btc_price']} ({m['btc_change']})，ETH 報價 {m['eth_price']} ({m['eth_change']})。建議保持中度觀望，嚴控風險。"

# ==========================================
# 模組二：潮流熱搜與迷因解構生成
# ==========================================
def run_trends_module(worker_url):
    print(">>> 開始執行潮流熱搜模組...")
    topics = [
        {"keyword": "#加密貨幣迷因", "volume": "高熱度"},
        {"keyword": "#AI自動化", "volume": "急升"},
        {"keyword": "#港股與美股連動", "volume": "穩定"},
        {"keyword": "#週末好去處", "volume": "熱搜"}
    ]
    topics_str = ", ".join([f"{t['keyword']} ({t['volume']})" for t in topics])
    
    prompt = f"你是一位對網路迷因極度敏銳的專欄作家。今日網上熱搜關鍵字如下：- {topics_str}。請用貼地、幽默的廣東話撰寫一份迷因解構報告（【熱話解構】與【迷因文化觀點】）。"
    
    try:
        res = requests.post(worker_url, json={"prompt": prompt, "tone": "casual", "lang": "hk"}, timeout=30)
        print(f"潮流模組 - 雲端 Worker 回應狀態碼: {res.status_code}")
        print(f"潮流模組 - 雲端 Worker 實際內容: {res.text}")
        
        res_json = res.json()
        trends_content = res_json.get("content") if res_json.get("success") else "今日網絡迷因討論熱烈！"
    except Exception as e:
        print(f"潮流模組 - 詳細錯誤原因: {e}")
        trends_content = "今日網絡迷因討論熱烈！"

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"trends/trend-{today}.html"
    os.makedirs("trends", exist_ok=True)
    
    list_html = "".join([f'<div class="bg-slate-50 p-4 rounded-lg border flex justify-between"><span class="font-bold">{t["keyword"]}</span><span class="text-xs bg-purple-100 text-purple-700 px-2.5 py-1 rounded-full">{t["volume"]}</span></div>' for t in topics])

    html_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>潮流熱搜與迷因關鍵字解構 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b border-slate-200 py-6 shadow-xs">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-semibold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-full">潮流與迷因專欄</span>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">🔥 潮流熱搜與迷因關鍵字</h1>
                <p class="text-xs text-slate-500 mt-1">發布時間：{now_time}</p>
            </div>
            <a href="../index.html" class="text-sm text-blue-600 hover:underline font-medium">← 返回主頁</a>
        </div>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="bg-white rounded-xl border border-slate-200 p-6 space-y-4">
            <h2 class="text-lg font-bold text-slate-900">📊 今日熱門關鍵字排行榜</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">{list_html}</div>
        </div>
        <div class="bg-white rounded-xl border border-slate-200 p-8 space-y-4">
            <h2 class="text-xl font-bold text-slate-900 border-b pb-4">💡 迷因與熱話深度解構</h2>
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

    finance_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-blue-500 bg-white transition"><span class="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded">財經專欄</span><h3 class="font-bold mt-1">加密貨幣市場日報 ({d})</h3></a>' for d, p in finance_posts])
    trends_html = "".join([f'<a href="{p}" class="block p-4 rounded-xl border hover:border-purple-500 bg-white transition"><span class="text-xs text-purple-600 bg-purple-50 px-2 py-0.5 rounded">潮流迷因</span><h3 class="font-bold mt-1">潮流熱搜與迷因解構 ({d})</h3></a>' for d, p in trends_posts])

    index_content = f"""<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自動化內容平台 - 財經與潮流速遞</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">
    <header class="bg-white border-b py-8 shadow-xs">
        <div class="max-w-4xl mx-auto px-4">
            <h1 class="text-3xl font-extrabold text-slate-900">📈 每日財經與潮流速遞</h1>
            <p class="text-slate-500 mt-2">由 AI 驅動的自動化市場分析與潮流熱話聚合平台</p>
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
    worker_url = os.environ.get("AI_WORKER_URL", "https://little-rice-42fa.lcw940708.workers.dev")
    run_finance_module(worker_url)
    run_trends_module(worker_url)
    update_index_page()