import json
import time
from fastapi import FastAPI
from websocket import create_connection
from datetime import datetime, timedelta

app = FastAPI()

# আপনার লাইভ সেশন কুকি (এটি নিয়মিত আপডেট করবেন)
LIVE_COOKIE = "lang=en; _ga=GA1.1.453634495.1773337729; __vid1=89f387f95a92729124e9994373142ae3; activeAccount=live;"

@app.get("/")
async def home():
    return {"status": "Quotex History Bridge Active", "owner": "DARK-X-RAYHAN"}

@app.get("/Qx/Qx.php")
async def get_history_data(pair: str = "USDBDT_otc", count: int = 10):
    pair = pair.upper()
    data_list = []
    
    try:
        # Quotex WebSocket কানেকশন
        ws = create_connection(
            "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
            header={
                "Cookie": LIVE_COOKIE,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            },
            timeout=10
        )
        
        # ১. চার্ট ডাটা সাবস্ক্রাইব করা
        ws.send(f'42["mt_subscribe","{pair}"]')
        
        # ২. হিস্টোরি ডাটা রিকোয়েস্ট (এটি Quotex এর ইন্টারনাল কমান্ড)
        # এটি গত কয়েক মিনিটের ডাটা সার্ভার থেকে টেনে আনবে
        current_ts = int(time.time())
        ws.send(f'42["chart_notification", {{"asset": "{pair}", "time": {current_ts}, "offset": {count}}}]')

        # ৩. ডাটা রিসিভ এবং প্রসেসিং
        for _ in range(15):
            msg = ws.recv()
            if "chart_notification" in msg:
                # JSON ডাটা ক্লিন করা
                raw_json = msg[msg.index('{'):]
                history_data = json.loads(raw_json)
                candles = history_data.get('candles', [])
                
                # লুপ চালিয়ে ১০টা ক্যান্ডেল ফরম্যাট করা
                for i, candle in enumerate(candles[-count:]):
                    o = candle[1]
                    c = candle[4]
                    h = candle[2]
                    l = candle[3]
                    ts = datetime.fromtimestamp(candle[0]).strftime("%Y-%m-%d %H:%M:00")
                    
                    data_list.append({
                        "id": str(len(candles) - i),
                        "pair": pair,
                        "candle_time": ts,
                        "open": str(o).replace('.', ','),
                        "high": str(h),
                        "low": str(l),
                        "close": str(c),
                        "color": "green" if float(c) > float(o) else "red"
                    })
                break
        
        ws.close()
        
        if not data_list:
            return {"success": False, "message": "Could not fetch history. Check if pair is active."}

        return {
            "Owner_Developer": "DARK-X-RAYHAN",
            "success": True,
            "count": len(data_list),
            "data": data_list[::-1] # লেটেস্টটা সবার উপরে দেখাবে
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
    }
