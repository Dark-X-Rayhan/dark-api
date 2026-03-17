from fastapi import FastAPI
from datetime import datetime, timedelta
import random

app = FastAPI()

# ক্যান্ডেল কালার লজিক
def get_candle_color(open_p, close_p):
    if close_p > open_p:
        return "green"
    elif close_p < open_p:
        return "red"
    else:
        return "doji"

@app.get("/Qx/Qx.php")
async def get_data(pair: str = "USDBDT_otc", count: int = 500):
    data_list = []
    # বর্তমান সময় থেকে শুরু করে পেছনের দিকে ডেটা জেনারেট হবে
    base_time = datetime.now()

    for i in range(count):
        # স্যাম্পল রিয়েলিস্টিক প্রাইস জেনারেশন
        # নোট: রিয়েল লাইভ ডাটার জন্য এখানে WebSocket ইন্টিগ্রেশন প্রয়োজন
        open_val = round(random.uniform(128.200, 128.300), 5)
        close_val = round(random.uniform(128.200, 128.300), 5)
        high_val = max(open_val, close_val) + round(random.uniform(0.001, 0.005), 5)
        low_val = min(open_val, close_val) - round(random.uniform(0.001, 0.005), 5)
        
        candle_time = (base_time - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:00")

        data_list.append({
            "id": str(i + 1),
            "pair": pair,
            "timeframe": "M1",
            "candle_time": candle_time,
            "open": str(open_val).replace('.', ','), # আপনার ফরম্যাট অনুযায়ী কমা ব্যবহার
            "high": f"{high_val:.3f}",
            "low": f"{low_val:.3f}",
            "close": f"{close_val:.3f}",
            "volume": str(random.randint(20, 150)),
            "color": get_candle_color(open_val, close_val),
            "created_at": candle_time
        })

    return {
        "Owner_Developer": "DARK-X-RAYHAN",
        "Telegram": "@mdrayhan85",
        "Channel": "https://t.me/mdrayhan85",
        "success": True,
        "count": count,
        "data": data_list
    }

# হোম রুট যাতে সার্ভার চেক করা যায়
@app.get("/")
async def root():
    return {"status": "API is Running", "developer": "@mdrayhan85"}
