import json
import os
from datetime import datetime

def generate_fengshui_data():
    """生成基本數據"""
    os.makedirs("data", exist_ok=True)
    data = {"status": "ready", "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open("data/fengshui.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("成功生成: data/fengshui.json")

def generate_index_page():
    """生成主頁 index.html"""
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI 姓名與生辰運勢批算站</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-slate-900">🔮 Richard AI 姓名與生辰運勢批算站</h1>
            <p class="text-xs text-slate-500 mt-1">Richard AI坐鎮，結合生辰、精密星座與姓名磁場，即時為你提供專業運程、幸運數字與開運花卉指導。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h2 class="text-lg font-bold text-slate-800">Richard AI全方位運勢批算</h2>
            <p class="text-sm text-slate-600">輸入閣下大名與出生日期，Richard AI 即刻為你開壇解構今日運勢、最旺數字同開運花卉！</p>
            <div>
                <a href="fengshui_chat.html" class="inline-block bg-amber-600 hover:bg-amber-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">立即請教 Richard AI </a>
            </div>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 Richard AI 姓名與生辰運勢批算站
    </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: index.html")

def generate_chat_page():
    """生成包含前端精確星座計算、即時時間與專家批算的 fengshui_chat.html"""
    chat_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI 專家級生辰姓名深度批算</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <a href="index.html" class="text-xs text-amber-600 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
                <h1 class="text-2xl font-bold text-slate-900 mt-1">🔮  AI Richard級生辰姓名批算</h1>
                <p class="text-xs text-slate-500 mt-1">Richard級專家坐鎮，精準對應星座、姓名磁場、今日最旺數字及開運花卉。</p>
            </div>
            <!-- 即時日期時間顯示 -->
            <div id="live-clock" class="text-right text-xs font-mono text-slate-500 bg-slate-100 px-3 py-2 rounded-lg border border-slate-200">
                載入中...
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4">
        <!-- 輸入卡片 -->
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label for="user-name" class="block text-xs font-bold text-slate-700 mb-1">閣下的中或英文姓名:</label>
                    <input type="text" id="user-name" placeholder="例如：陳大文 或 David Chan" class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-amber-500">
                </div>
                <div>
                    <label for="user-dob" class="block text-xs font-bold text-slate-700 mb-1">出生日期:</label>
                    <input type="date" id="user-dob" class="w-full border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-amber-500">
                </div>
            </div>
            <div>
                <button onclick="getFortune()" id="send-btn" class="w-full bg-amber-600 hover:bg-amber-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition">請 Richard AI 批算今日運勢</button>
            </div>
        </div>

        <!-- 結果展示對話區 -->
        <div id="chat-container" class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4 min-h-[350px] max-h-[500px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-700 max-w-[80%]">
                    「老實講，坐低慢慢嘆杯茶。請喺上面填好你個大名同埋出生日期，本AI即刻結合今日天時、精準星座、姓名磁場，同你批算出嚟今日最旺你嘅數字同開運花卉！」
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 AI Richard級運勢批算系統
    </footer>

    <script>
        // 即時更新日期時間
        function updateClock() {
            const now = new Date();
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            document.getElementById('live-clock').innerText = now.toLocaleString('zh-HK', options);
        }
        setInterval(updateClock, 1000);
        updateClock();

        // 精確計算星座函數（保證 0 誤差）
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
                alert('請完整填寫你的姓名同埋出生日期先至可以請 Richard AI 批算！');
                return;
            }

            // 前端精確計算星座，杜絕 AI 亂估
            const dobDate = new Date(userDob);
            const month = dobDate.getMonth() + 1;
            const day = dobDate.getDate();
            const exactZodiac = getZodiacSign(month, day);

            const currentDateTimeStr = new Date().toLocaleString('zh-HK', { hour12: false });

            chatContainer.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-amber-50 text-slate-800 rounded-lg p-3 text-sm max-w-[80%]"><b>[${escapeHtml(userName)} | 生日: ${escapeHtml(userDob)} | 星座: ${exactZodiac}]</b> 請 Richard AI 批算（批算時間：${currentDateTimeStr}）</div>
                    <div class="bg-slate-800 text-white text-xs px-2.5 py-1 rounded-full font-bold">你</div>
                </div>
            `;
            
            nameField.disabled = true;
            dobField.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = 'Richard AI正以專業視角推算中...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                    <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-500 italic">Richard AI 正結合今日（${currentDateTimeStr}）天時、精確星座【${exactZodiac}】與姓名磁場為「${escapeHtml(userName)}」進行深度權威批算...</div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            try {
                // 請確保換上你真實的 Cloudflare Worker 網址
                const response = await fetch('https://mainbot.lcw940708.workers.dev/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        name: userName, 
                        dob: userDob, 
                        zodiac: exactZodiac, // 傳送前端算好的正確星座
                        requestTime: currentDateTimeStr,
                        prompt: "請以玄學權威專家身分批算全方位運勢，並必須給出今日最旺數字及開運花卉建議。" 
                    })
                });

                const data = await response.json();
                document.getElementById(loadingId).remove();

                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                        <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-700 max-w-[80%]" style="white-space: pre-line;">${escapeHtml(data.content || '師傅一時靈感天機閉塞，請稍後重試。')}</div>
                    </div>
                `;

            } catch (error) {
                document.getElementById(loadingId).remove();
                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">系統</div>
                        <div class="bg-rose-50 text-rose-700 rounded-lg p-3 text-sm max-w-[80%]">天機被雲端遮擋（連線出錯），請檢查網絡或 Worker 設定。</div>
                    </div>
                `;
            }

            nameField.disabled = false;
            dobField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '請 Richard AI 批算今日運勢';
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
    print("成功生成: fengshui_chat.html (專家級 + 前端精確星座鎖死版)")

if __name__ == "__main__":
    print("開始執行 Richard AI 專家級系統生成程序...")
    generate_fengshui_data()
    generate_index_page()
    generate_chat_page()
    print("全部檔案生成完畢！")