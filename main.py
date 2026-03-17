from fastapi import FastAPI, Request
from datetime import datetime, timedelta
import random

app = FastAPI()

# ৫৪টি পেয়ারের লিস্ট
SUPPORTED_PAIRS = [
    "AUDCAD_otc", "AUDCHF_otc", "AUDJPY_otc", "AUDNZD_otc", "AUDUSD_otc", "AXP_otc",
    "BABA_otc", "BRLUSD_otc", "BTCUSD_otc", "CADCHF_otc", "CADJPY_otc", "CHFJPY_otc",
    "EURAUD_otc", "EURCAD_otc", "EURCHF_otc", "EURGBP_otc", "EURJPY_otc", "EURNZD_otc",
    "EURSGD_otc", "EURUSD_otc", "FB_otc", "GBPAUD_otc", "GBPCAD_otc", "GBPCHF_otc",
    "GBPJPY_otc", "GBPNZD_otc", "GBPUSD_otc", "GOOG_otc", "INTC_otc", "JNJ_otc",
    "KO_otc", "MCD_otc", "MSFT_otc", "NZDCAD_otc", "NZDCHF_otc", "NZDJPY_otc",
    "NZDUSD_otc", "PFE_otc", "PG_otc", "USDBDT_otc", "USDCAD_otc", "USDCHF_otc",
    "USDCOP_otc", "USDDZD_otc", "USDEGP_otc", "USDIDR_otc", "USDINR_otc", "USDJPY_otc",
    "USDMXN_otc", "USDNGN_otc", "USDPKR_otc", "USDTRY_otc", "USDZAR_otc", "XAUUSD_otc"
]

def get_color(o, c):
    return "green" if float(c) > float(o) else "red" if float(c) < float(o) else "doji"

# হোম রুট (যাতে Not Found না আসে)
@app.get("/")
async def home():
    return {
        "status": "Online",
        "message": "Visit /Qx/Qx.php?pair=USDBDT_otc&count=10",
        "developer": "DARK-X-RAYHAN"
    }

# মেইন এপিআই পাথ (Case Insensitive করার চেষ্টা করা হয়েছে)
@app.get("/Qx/Qx.php")
async def get_data(pair: str = "USDBDT_otc", count: int = 100):
    data_list = []
    now = datetime.now()
    pair = pair.upper()

    # বেস প্রাইস সিলেকশন
    if "BTC" in pair: base = 68000.0
    elif "XAU" in pair: base = 2160.0
    elif "BDT" in pair: base = 128.25
    else: base = 1.1234

    for i in range(count):
        dt = now - timedelta(minutes=i)
        ts = dt.strftime("%Y-%m-%d %H:%M:00")
        
        # ইউনিক ডাটার জন্য সিড
        random.seed(int(dt.timestamp()))
        
        diff = base * 0.0004
        open_p = round(base + random.uniform(-diff, diff), 5)
        close_p = round(open_p + random.uniform(-diff/2, diff/2), 5)
        high_p = round(max(open_p, close_p) + random.uniform(0, diff/5), 5)
        low_p = round(min(open_p, close_p) - random.uniform(0, diff/5), 5)

        data_list.append({
            "id": str(i + 1),
            "pair": pair,
            "timeframe": "M1",
            "candle_time": ts,
            "open": str(open_p).replace('.', ','),
            "high": f"{high_p:.5f}",
            "low": f"{low_p:.5f}",
            "close": f"{close_p:.5f}",
            "volume": str(random.randint(40, 300)),
            "color": get_color(open_p, close_p),
            "created_at": ts
        })

    return {
        "Owner_Developer": "DARK-X-RAYHAN",
        "Telegram": "@mdrayhan85",
        "success": True,
        "count": len(data_list),
        "data": data_list
    }
