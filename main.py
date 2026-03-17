import json
import time
from fastapi import FastAPI
from websocket import create_connection
from datetime import datetime

app = FastAPI()

# আপনার লাইভ সেশন কুকি
LIVE_COOKIE = "lang=en; _ga=GA1.1.453634495.1773337729; __vid1=89f387f95a92729124e9994373142ae3; activeAccount=live;"

# আপনার ৫২টি পেয়ার
PAIRS = [
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

def fetch_quotex_candle(pair):
    try:
        # Quotex WebSocket কানেকশন
        ws = create_connection(
            "wss://ws2.qxbroker.com/socket.io/?EIO=3&transport=websocket",
            header={"Cookie": LIVE_COOKIE},
            timeout=7
        )
        
        # ডাটা সাবস্ক্রাইব
        ws.send(f'42["mt_subscribe","{pair.upper()}"]')
        
        # লাইভ টিক ডাটা পাওয়ার চেষ্টা
        for _ in range(8):
            msg = ws.recv()
            if "mt_tick" in msg:
                # মেসেজ থেকে ডাটা পার্সিং
                res = json.loads(msg[2:])
                ws.close()
                return res[1]
        ws.close()
    except:
        return None

@app.get("/")
async def home():
    return {"status": "Live Session Active", "owner": "DARK-X-RAYHAN"}

@app.get("/Qx/Qx.php")
async def get_real_time_data(pair: str = "USDBDT_otc", count: int = 1):
    target_pair = pair.lower()
    
    # লাইভ ডাটা নিয়ে আসা
    qx_data = fetch_quotex_candle(target_pair)
    
    if not qx_data:
        return {"success": False, "message": "Failed to sync live data. Refresh Cookie."}

    # Quotex থেকে আসা রিয়েল ডাটা
    o = qx_data.get('open')
    c = qx_data.get('close')
    h = qx_data.get('high')
    l = qx_data.get('low')
    
    color = "green" if float(c) > float(o) else "red" if float(c) < float(o) else "doji"

    return {
        "Owner_Developer": "DARK-X-RAYHAN",
        "success": True,
        "pair": target_pair.upper(),
        "data": [{
            "id": "1",
            "candle_time": datetime.now().strftime("%Y-%m-%d %H:%M:00"),
            "open": str(o).replace('.', ','),
            "high": str(h),
            "low": str(l),
            "close": str(c),
            "color": color
        }]
    }
