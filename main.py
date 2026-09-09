import json
import os
from datetime import datetime

def generate_fengshui_data():
    """生成今日風水通勝數據 JSON"""
    os.makedirs("data", exist_ok=True)
    
    fengshui_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "update_time": datetime.now().strftime("%H:%M:%S"),
        "auspicious_direction": "正東方（財神位）、正南方（喜神位）",
        "inavoidable_taboo": "宜：納財、開市、出行；忌：動土、破土",
        "daily_advice": "今日氣場和順，行事積極主動容易獲得貴人相助，投資理財宜穩健為主。"
    }
    
    with open("data/fengshui.json", "w", encoding="utf-8") as f:
        json.dump(fengshui_data, f, ensure_ascii=False, indent=4)
    print("成功生成: data/fengshui.json")

def generate_index_page():
    """生成主頁 index.html"""
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 風水與財經資訊站</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-slate-900">🔮 AI 風水與財經資訊站</h1>
            <p class="text-xs text-slate-500 mt-1">結合中英文姓名學與實時通勝數據的自動化 AI 平台。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h2 class="text-lg font-bold text-slate-800">精選服務</h2>
            <p class="text-sm text-slate-600">輸入你的中英文名與問題，讓 AI 師傅為你進行姓名學與今日運勢速測。</p>
            <div>
                <a href="fengshui_chat.html" class="inline-block bg-amber-600 hover:bg-amber-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">進入 AI 姓名風水師問答</a>
            </div>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 AI 風水與財經資訊站
    </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: index.html")

def generate_chat_page():
    """生成支援中英文名輸入的對話介面 fengshui_chat.html"""
    chat_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 智能姓名風水師問答</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <a href="index.html" class="text-xs text-amber-600 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
            <h1 class="text-2xl font-bold text-slate-900 mt-1">🔮 AI 智能姓名風水師</h1>
            <p class="text-xs text-slate-500 mt-1">輸入閣下的中英文名與想問的事，師傅即時為你解構姓名能量與今日吉凶。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4">
        <!-- 姓名輸入列 -->
        <div class="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex items-center space-x-3">
            <label for="user-name" class="text-xs font-bold text-slate-700 whitespace-nowrap">中/英文姓名:</label>
            <input type="text" id="user-name" placeholder="例如：陳大文 或 David Chan" class="flex-grow border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-amber-500">
        </div>

        <!-- 對話視窗 -->
        <div id="chat-container" class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4 min-h-[320px] max-h-[450px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">AI</div>
                <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-700 max-w-[80%]">
                    你好！請在上方輸入你的中英文名，並在下方問事，師傅會結合姓名學同今日通勝為你解答！
                </div>
            </div>
        </div>

        <!-- 輸入問題列 -->
        <div class="flex gap-2">
            <input type="text" id="user-input" placeholder="例如：今日去邊個方位最好？..." class="flex-grow border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-amber-500">
            <button onclick="sendQuestion()" id="send-btn" class="bg-amber-600 hover:bg-amber-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">發送</button>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 AI 風水問答系統
    </footer>

    <script>
        async function sendQuestion() {
            const nameField = document.getElementById('user-name');
            const inputField = document.getElementById('user-input');
            const chatContainer = document.getElementById('chat-container');
            const sendBtn = document.getElementById('send-btn');
            
            const userName = nameField.value.trim() || "善信";
            const question = inputField.value.trim();
            if (!question) return;

            chatContainer.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-amber-50 text-slate-800 rounded-lg p-3 text-sm max-w-[80%]"><b>[${escapeHtml(userName)}]</b> ${escapeHtml(question)}</div>
                    <div class="bg-slate-800 text-white text-xs px-2.5 py-1 rounded-full font-bold">你</div>
                </div>
            `;
            
            inputField.value = '';
            inputField.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = '推算緊...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">AI</div>
                    <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-500 italic">正在分析姓名能量與今日通勝數據...</div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            try {
                // 請確保換上你真實的 Cloudflare Worker 網址
                const response = await fetch('https://mainbot.lcw940708.workers.dev/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: userName, prompt: question })
                });

                const data = await response.json();
                document.getElementById(loadingId).remove();

                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-amber-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">AI</div>
                        <div class="bg-slate-100 rounded-lg p-3 text-sm text-slate-700 max-w-[80%]">${escapeHtml(data.content || '暫時無法取得回覆，請稍後再試。')}</div>
                    </div>
                `;

            } catch (error) {
                document.getElementById(loadingId).remove();
                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-rose-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">系統</div>
                        <div class="bg-rose-50 text-rose-700 rounded-lg p-3 text-sm max-w-[80%]">連線發生錯誤，請檢查網絡或 Worker 設定。</div>
                    </div>
                `;
            }

            inputField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '發送';
            inputField.focus();
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        document.getElementById('user-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendQuestion();
            }
        });
    </script>
</body>
</html>
"""
    with open("fengshui_chat.html", "w", encoding="utf-8") as f:
        f.write(chat_content)
    print("成功生成: fengshui_chat.html (支援中英文名)")

if __name__ == "__main__":
    print("開始執行自動化生成程序...")
    generate_fengshui_data()
    generate_index_page()
    generate_chat_page()
    print("全部檔案生成完畢！")