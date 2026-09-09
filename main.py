import json
import os
from datetime import datetime

def calculate_name_fortune(name):
    """根據中英文名字計算趣味運勢與靈動數"""
    name = name.strip()
    if not name:
        name = "善信"
    
    # 計算姓名特徵值
    total_score = 0
    is_chinese = any('\u4e00' <= char <= '\u9fff' for char in name)
    
    if is_chinese:
        # 中文名：以字數同字符編碼模擬筆劃能量
        total_score = sum(ord(char) for char in name)
        method_desc = f"中文字體氣場檢測（字數：{len(name)}）"
    else:
        # 英文名：將英文字母轉為數值 (A=1, B=2...)
        clean_name = name.lower()
        total_score = sum(ord(char) - 96 for char in clean_name if 'a' <= char <= 'z')
        if total_score == 0:
            total_score = len(name) * 7
        method_desc = f"英文字母靈動數計算"

    # 用餘數分拆出唔同嘅運勢結果
    remainder = total_score % 5
    
    fortunes = [
        {
            "level": "大吉 🌟",
            "title": "紫氣東來，貴人扶持",
            "desc": "名字筆劃磁場極佳，近排在財運或工作上容易遇到貴人提攜，心想事成，宜積極進取！",
            "lucky_direction": "正東方（財神位）",
            "lucky_color": "赤紅色 / 鮮黃色"
        },
        {
            "level": "中吉 ✨",
            "title": "穩步上揚，謀事可成",
            "desc": "氣場平和穩健，雖然過程可能有一小波折，但只要按部就班，最終必有收穫，切忌心浮氣躁。",
            "lucky_direction": "正南方（喜神位）",
            "lucky_color": "墨綠色 / 寶藍色"
        },
        {
            "level": "平吉 🌙",
            "title": "以靜制動，宜守不宜攻",
            "desc": "今日磁場稍見波動，不適合過度冒險或作重大決定。穩陣行事、飲杯茶抖足精神，自然平安順遂。",
            "lucky_direction": "西北方（福德位）",
            "lucky_color": "米白色 / 沉實灰"
        },
        {
            "level": "上吉 ☀️",
            "title": "靈光乍現，財運亨通",
            "desc": "名字能量異常活躍，靈感湧現，特別適合處理投資理財或開拓新項目，今日眼光獨到！",
            "lucky_direction": "正西方（生財位）",
            "lucky_color": "金黃色 / 亮銀色"
        },
        {
            "level": "小吉 🍃",
            "title": "順其自然，心安理得",
            "desc": "運勢平穩和順，無風無浪。最適合用嚟整理思緒、陪伴屋企人或者享受悠閒時光。",
            "lucky_direction": "東北方（如意位）",
            "lucky_color": "大地色 / 淺卡其"
        }
    ]
    
    result = fortunes[remainder]
    result["name"] = name
    result["method"] = method_desc
    result["date"] = datetime.now().strftime("%Y-%m-%d")
    return result

def generate_fengshui_data():
    """生成基礎通勝數據"""
    os.makedirs("data", exist_ok=True)
    default_data = calculate_name_fortune("陳大文")
    with open("data/fengshui.json", "w", encoding="utf-8") as f:
        json.dump(default_data, f, ensure_ascii=False, indent=4)
    print("成功生成: data/fengshui.json")

def generate_index_page():
    """生成主頁 index.html"""
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 姓名運勢速測站</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-slate-900">🔮 AI 姓名運勢速測站</h1>
            <p class="text-xs text-slate-500 mt-1">融合中英文姓名學與精準運算，即時為你推算今日氣場。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h2 class="text-lg font-bold text-slate-800">姓名算命速測</h2>
            <p class="text-sm text-slate-600">無需等待 AI 聯網，輸入你的中英文名，一秒睇出今日運勢、吉方與幸運顏色。</p>
            <div>
                <a href="fengshui_chat.html" class="inline-block bg-amber-600 hover:bg-amber-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">立即開始姓名算命</a>
            </div>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 AI 姓名運勢速測站
    </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: index.html")

def generate_chat_page():
    """生成純前端運算、秒出結果嘅姓名算命介面 fengshui_chat.html"""
    chat_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>姓名運勢實時速測</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-white border-b border-slate-200 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <a href="index.html" class="text-xs text-amber-600 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
            <h1 class="text-2xl font-bold text-slate-900 mt-1">🔮 姓名運勢實時速測</h1>
            <p class="text-xs text-slate-500 mt-1">輸入閣下的中或英文名，秒速為你解構今日專屬靈動數與方位吉凶。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-6">
        <!-- 輸入表單卡片 -->
        <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div>
                <label for="user-name" class="block text-xs font-bold text-slate-700 mb-1">請輸入你的中英文姓名:</label>
                <div class="flex gap-2">
                    <input type="text" id="user-name" placeholder="例如：陳大文 或 David Chan" class="flex-grow border border-slate-300 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-amber-500">
                    <button onclick="calculateFortune()" class="bg-amber-600 hover:bg-amber-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition whitespace-nowrap">開始算命</button>
                </div>
            </div>
        </div>

        <!-- 結果展示區 -->
        <div id="result-container" class="hidden bg-white rounded-xl border border-amber-200 p-6 shadow-xs space-y-4 bg-amber-50/30">
            <div class="border-b border-amber-100 pb-3 flex justify-between items-center">
                <h3 id="res-name-title" class="text-base font-bold text-slate-900"></h3>
                <span id="res-level" class="text-xs font-bold px-3 py-1 rounded-full bg-amber-600 text-white"></span>
            </div>
            
            <div class="space-y-3 text-sm">
                <div>
                    <span class="text-xs font-bold text-slate-500 block">運勢批語：</span>
                    <p id="res-title" class="text-base font-bold text-amber-900 mt-0.5"></p>
                    <p id="res-desc" class="text-slate-700 mt-1"></p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                    <div class="bg-white p-3 rounded-lg border border-slate-200">
                        <span class="text-xs font-bold text-slate-400 block">今日吉方</span>
                        <p id="res-direction" class="text-slate-800 font-medium text-sm mt-0.5"></p>
                    </div>
                    <div class="bg-white p-3 rounded-lg border border-slate-200">
                        <span class="text-xs font-bold text-slate-400 block">幸運顏色</span>
                        <p id="res-color" class="text-slate-800 font-medium text-sm mt-0.5"></p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t py-4 text-center text-xs text-slate-400 bg-white">
        © 2026 姓名運勢速測系統
    </footer>

    <script>
        function calculateFortune() {
            const nameInput = document.getElementById('user-name');
            const name = nameInput.value.trim();
            if (!name) {
                alert('請先輸入姓名先至可以算命！');
                return;
            }

            // 本地簡易靈動數計算邏輯（與 Python 保持一致）
            let totalScore = 0;
            const isChinese = /[\\u4e00-\\u9fff]/.test(name);
            
            if (isChinese) {
                for (let i = 0; i < name.length; i++) {
                    totalScore += name.charCodeAt(i);
                }
            } else {
                const cleanName = name.toLowerCase();
                for (let i = 0; i < cleanName.length; i++) {
                    const code = cleanName.charCodeAt(i);
                    if (code >= 97 && code <= 122) {
                        totalScore += (code - 96);
                    }
                }
                if (totalScore === 0) totalScore = name.length * 7;
            }

            const remainder = totalScore % 5;
            const fortunes = [
                {
                    level: "大吉 🌟",
                    title: "紫氣東來，貴人扶持",
                    desc: "名字筆劃磁場極佳，近排在財運或工作上容易遇到貴人提攜，心想事成，宜積極進取！",
                    direction: "正東方（財神位）",
                    color: "赤紅色 / 鮮黃色"
                },
                {
                    level: "中吉 ✨",
                    title: "穩步上揚，謀事可成",
                    desc: "氣場平和穩健，雖然過程可能有一小波折，但只要按部就班，最終必有收穫，切忌心浮氣躁。",
                    direction: "正南方（喜神位）",
                    color: "墨綠色 / 寶藍色"
                },
                {
                    level: "平吉 🌙",
                    title: "以靜制動，宜守不宜攻",
                    desc: "今日磁場稍見波動，不適合過度冒險或作重大決定。穩陣行事、飲杯茶抖足精神，自然平安順遂。",
                    direction: "西北方（福德位）",
                    color: "米白色 / 沉實灰"
                },
                {
                    level: "上吉 ☀️",
                    title: "靈光乍現，財運亨通",
                    desc: "名字能量異常活躍，靈感湧現，特別適合處理投資理財或開拓新項目，今日眼光獨到！",
                    direction: "正西方（生財位）",
                    color: "金黃色 / 亮銀色"
                },
                {
                    level: "小吉 🍃",
                    title: "順其自然，心安理得",
                    desc: "運勢平穩和順，無風無浪。最適合用嚟整理思緒、陪伴屋企人或者享受悠閒時光。",
                    direction: "東北方（如意位）",
                    color: "大地色 / 淺卡其"
                }
            ];

            const res = fortunes[remainder];

            // 填入 DOM
            document.getElementById('res-name-title').innerText = `「${name}」今日運勢批算`;
            document.getElementById('res-level').innerText = res.level;
            document.getElementById('res-title').innerText = res.title;
            document.getElementById('res-desc').innerText = res.desc;
            document.getElementById('res-direction').innerText = res.direction;
            document.getElementById('res-color').innerText = res.color;

            // 顯示結果卡片
            document.getElementById('result-container').classList.remove('hidden');
        }

        // 支援按 Enter 鍵直接算命
        document.getElementById('user-name').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                calculateFortune();
            }
        });
    </script>
</body>
</html>
"""
    with open("fengshui_chat.html", "w", encoding="utf-8") as f:
        f.write(chat_content)
    print("成功生成: fengshui_chat.html (姓名算命專用版)")

if __name__ == "__main__":
    print("開始執行姓名算命系統生成程序...")
    generate_fengshui_data()
    generate_index_page()
    generate_chat_page()
    print("全部檔案生成完畢！")