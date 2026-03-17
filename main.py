from fastapi import FastAPI
from datetime import datetime, timedelta
import random

app = FastAPI()

# ৫৪টি পেয়ারের লিস্ট (যাতে ডাটা ফিল্টার করা যায়)
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

def get_candle_color(open_p, close_p):
    return "green" if float(close_p) > float(open_p) else "red" if float(close_p) < float(open_p) else "doji"

@app.get("/")
async def root():
    return {"status": "API Active", "owner": "DARK-X-RAYHAN", "pairs_count": len(SUPPORTED_PAIRS)}

@app.get("/Qx/Qx.php")
async def get_qx_data(pair: str = "USDBDT_otc", count: int = 100):
    # পেয়ারটি লিস্টে না থাকলেও কাজ করবে, তবে লিস্টের সাথে মিলিয়ে নেওয়া ভালো
    target_pair = pair.upper() if pair.lower() in [p.lower() for p in SUPPORTED_PAIRS] else pair.upper()
    
    data_list = []
    now = datetime.now()
    
    # পেয়ার অনুযায়ী বেস প্রাইস ঠিক করা (যাতে ডাটা রিয়েলিস্টিক লাগে)
    if "BTC" in target_pair: base_price = 65000.0
    elif "XAU" in target_pair: base_price = 2150.0
    elif "BDT" in target_pair: base_price = 128.25
    elif "JPY" in target_pair: base_price = 150.50
    else: base_price = 1.1234 # সাধারণ ফোরেক্স পেয়ারের জন্য

    for i in range(count):
        candle_dt = now - timedelta(minutes=i)
        time_str = candle_dt.strftime("%Y-%m-%d %H:%M:00")
        
        # টাইমস্ট্যাম্প অনুযায়ী সিড সেট করা যাতে রিফ্রেশ করলে প্রাইস না বদলায়
        random.seed(int(candle_dt.timestamp()))
        
        # ভোলাটিলিটি সেট করা
        vol = base_price * 0.0005 
        open_p = round(base_price + random.uniform(-vol, vol), 5)
        close_p = round(open_p + random.uniform(-vol/2, vol/2), 5)
        high_p = round(max(open_p, close_p) + random.uniform(0, vol/4), 5)
        low_p = round(min(open_p, close_p) - random.uniform(0, vol/4), 5)

        data_list.append({
            "id": str(i + 1),
            "pair": target_pair,
            "timeframe": "M1",
            "candle_time": time_str,
            "open": str(open_p).replace('.', ','),
            "high": f"{high_p:.5f}",
            "low": f"{low_p:.5f}",
            "close": f"{close_p:.5f}",
            "volume": str(random.randint(20, 200)),
            "color": get_candle_color(open_p, close_p),
            "created_at": time_str
        })

    return {
        "Owner_Developer": "DARK-X-RAYHAN",
        "Telegram": "@mdrayhan85",
        "Channel": "https://t.me/mdrayhan85",
        "success": True,
        "count": len(data_list),
        "data": data_list
    }
