import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_horoscope_data():
    """從網上（例如公開運程或氣象資訊網站）動態抓取最新數據"""
    os.makedirs("data", exist_ok=True)
    
    target_url = "https://example.com/horoscope-daily"
    
    scraped_content = {}
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(target_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            main_text = soup.get_text(strip=True)[:500]
            scraped_content = {
                "source_status": "success",
                "raw_text": main_text
            }
        else:
            raise Exception(f"HTTP Status: {response.status_code}")
            
    except Exception as e:
        scraped_content = {
            "source_status": "fallback_mode",
            "error": str(e),
            "malicious_stars": {
                "五鬼": "今日易惹小人暗算，職場上慎防言語衝突。",
                "大耗": "破財危機顯現，切忌進行高風險投資。"
            },
            "zodiac_taboos": {
                "白羊座": "衝動易破財，注意交通安全。",
                "金牛座": "財運受阻，避免大額借貸。",
                "雙子座": "卷舌凶星入宮，慎防合約文件陷阱。",
                "巨蟹座": "情緒化導致無謂消費。",
                "獅子座": "過分自信易招嫉妒。",
                "處女座": "壓力過大注意腸胃健康。",
                "天秤座": "人際摩擦增加。",
                "天蠍座": "疑神疑鬼影響判斷。",
                "人馬座 (射手座)": "遠行或外出小心財物。",
                "山羊座 (摩羯座)": "工作繁重易計錯數。",
                "水瓶座": "思路混亂不宜作重大決定。",
                "雙魚座": "容易心軟受騙。"
            }
        }

    final_data = {
        "status": "scraped_and_ready",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": scraped_content
    }

    with open("data/fengshui.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("成功抓取並生成: data/fengshui.json")

def generate_index_page():
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI 網上動態抓取預警站</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-slate-800 border-b border-rose-900/50 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-rose-400">🌐 Richard AI 網絡實時抓取與危機預警站</h1>
            <p class="text-xs text-slate-400 mt-1">結合 Python 網絡爬蟲實時同步最新玄學、運程與凶星資訊。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-slate-800 rounded-xl border border-rose-900/40 p-6 shadow-lg space-y-4">
            <h2 class="text-lg font-bold text-rose-300">實時抓取數據與批算</h2>
            <p class="text-sm text-slate-300">後台透過爬蟲獲取最新數據，結合精確星座與姓名，由 Richard AI 為你解析今日危機！</p>
            <div>
                <a href="fengshui_chat.html" class="inline-block bg-rose-600 hover:bg-rose-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">進入對話批算頁面</a>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI 抓取預警系統
    </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: index.html")

def generate_chat_page():
    chat_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI 實時抓取批算系統</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-slate-800 border-b border-rose-900/50 py-6">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <a href="index.html" class="text-xs text-rose-400 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
                <h1 class="text-2xl font-bold text-rose-400 mt-1">🌐 Richard AI 實時抓取運程批算</h1>
                <p class="text-xs text-slate-400 mt-1">結合動態抓取數據與大師級香港廣東話剖析。</p>
            </div>
            <div id="live-clock" class="text-right text-xs font-mono text-rose-300 bg-slate-900 px-3 py-2 rounded-lg border border-rose-900/40">
                載入中...
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4">
        <div class="bg-slate-800 rounded-xl border border-rose-900/40 p-6 shadow-lg space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label for="user-name" class="block text-xs font-bold text-rose-300 mb-1">閣下的中或英文姓名:</label>
                    <input type="text" id="user-name" placeholder="例如：陳大文 或 David Chan" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-rose-500">
                </div>
                <div>
                    <label for="user-dob" class="block text-xs font-bold text-rose-300 mb-1">出生日期:</label>
                    <input type="date" id="user-dob" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-rose-500">
                </div>
            </div>
            <div>
                <button onclick="getFortune()" id="send-btn" class="w-full bg-rose-600 hover:bg-rose-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition shadow-md">請 Richard AI 結合抓取數據批算</button>
            </div>
        </div>

        <div id="chat-container" class="bg-slate-800 rounded-xl border border-rose-900/40 p-6 shadow-lg space-y-4 min-h-[350px] max-h-[500px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]">
                    「老實講，後台已經幫你自動抓取咗最新嘅網上運程同凶星數據。填好你個名同生日，本大師即刻同你拆解！」
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI 抓取預警系統
    </footer>

    <script>
        function updateClock() {
            const now = new Date();
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            document.getElementById('live-clock').innerText = now.toLocaleString('zh-HK', options);
        }
        setInterval(updateClock, 1000);
        updateClock();

        function getZodiacSign(month, day) {
            if ((month == 1 && day >= 20) || (month == 2 && day <= 18)) return "水瓶座";
            if ((month == 2 && day >= 19) || (month == 3 && day <= 20)) return "雙魚座";
            if ((month == 3 && day >= 21) || (month == 4 && day <= 19)) return "白羊座";
            if ((month == 4 && day >= 20) || (month == 5 && day <= 20)) return "金牛座";
            if ((month == 5 && day >= 21) || (month == 6 && day <= 21)) return "雙子座";
            if ((month == 6 && day >= 22) || (month == 7 && day <= 22)) return "巨蟹座";
            if ((month == 7 && day >= 23) || (month == 8 && day <= 22)) return "獅子座";
            if ((month == 8 && day >= 23) || (month == 9 && day <= 22)) return "處女座";
            if ((month == 9 && day >= 23) || (month == 10 && day <= 23)) return "天秤座";
            if ((month == 10 && day >= 24) || (month == 11 && day <= 21)) return "天蠍座";
            if ((month == 11 && day >= 22) || (month == 12 && day <= 21)) return "人馬座 (射手座)";
            return "山羊座 (摩羯座)";
        }

        async function getFortune() {
            const nameField = document.getElementById('user-name');
            const dobField = document.getElementById('user-dob');
            const chatContainer = document.getElementById('chat-container');
            const sendBtn = document.getElementById('send-btn');
            
            const userName = nameField.value.trim();
            const userDob = dobField.value;

            if (!userName || !userDob) {
                alert('請完整填寫姓名同出生日期！');
                return;
            }

            let scrapedData = {};
            try {
                const res = await fetch('data/fengshui.json');
                scrapedData = await res.json();
            } catch (e) {
                scrapedData = { status: "error" };
            }

            const dobDate = new Date(userDob);
            const month = dobDate.getMonth() + 1;
            const day = dobDate.getDate();
            const exactZodiac = getZodiacSign(month, day);
            const currentDateTimeStr = new Date().toLocaleString('zh-HK', { hour12: false });

            chatContainer.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-slate-700 text-slate-100 rounded-lg p-3 text-sm max-w-[80%]"><b>[${escapeHtml(userName)} | 生日: ${escapeHtml(userDob)} | 星座: ${exactZodiac}]</b> 請 Richard AI 大師批算</div>
                    <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">你</div>
                </div>
            `;
            
            nameField.disabled = true;
            dobField.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = '大師正結合抓取數據分析中...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                    <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-400 italic">正在剖析最新網絡抓取數據，為「${escapeHtml(userName)}」（${exactZodiac}）進行深度批算...</div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            try {
                const response = await fetch('https://mainbot.lcw940708.workers.dev/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        name: userName, 
                        dob: userDob, 
                        zodiac: exactZodiac, 
                        scrapedData: scrapedData,
                        requestTime: currentDateTimeStr,
                        prompt: "請結合網絡抓取數據與精確星座，嚴厲指出今日要小心咩陷阱、最旺數字同開運花卉。" 
                    })
                });

                const data = await response.json();
                document.getElementById(loadingId).remove();

                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                        <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]" style="white-space: pre-line;">${escapeHtml(data.content || '師傅一時天機閉塞，請稍後重試。')}</div>
                    </div>
                `;

            } catch (error) {
                document.getElementById(loadingId).remove();
                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">系統</div>
                        <div class="bg-rose-900/50 border border-rose-700 text-rose-200 rounded-lg p-3 text-sm max-w-[80%]">連線出錯，請檢查 Worker 設定。</div>
                    </div>
                `;
            }

            nameField.disabled = false;
            dobField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '請 Richard AI 結合抓取數據批算';
            nameField.focus();
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""
    with open("fengshui_chat.html", "w", encoding="utf-8") as f:
        f.write(chat_content)
    print("成功生成: fengshui_chat.html (實時抓取整合版)")

if __name__ == "__main__":
    print("開始執行 Richard AI 網絡爬蟲與網頁生成程序...")
    scrape_horoscope_data()
    generate_index_page()
    generate_chat_page()
    print("全部檔案生成完畢！")