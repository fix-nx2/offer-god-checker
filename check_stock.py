import os
import time
import requests
from bs4 import BeautifulSoup
import urllib3

# 關閉 SSL 憑證警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 目標網址 (上環文武廟 Offer God 頁面)
URL = "https://temples.tungwahcsd.org/product/470"

# 從 GitHub 設定的安全秘密中讀取 Telegram 資訊
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("未設定 Telegram 憑證")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    # 發送時也加上 verify=False
    requests.post(url, json=payload, verify=False)

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        # 關鍵：加上 verify=False 來略過憑證驗證
        response = requests.get(URL, headers=headers, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"網頁訪問失敗，狀態碼: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()
        
        # 檢查網頁是否還在缺貨 (如果你剛剛為了測試改成亂碼，可以先維持亂碼來測試 TG，或者改回原本的「缺貨」)
        if "缺貨" in page_text or "Out of Stock" in page_text:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 目前仍然缺貨中...")
            # 為了測試 TG 是否能通，我們這裡也先強制發送一則測試訊息
            send_telegram("🎉 【測試訊息】SSL 憑證問題已修複，這是測試通知！")
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🎉 好像有貨啦！")
            send_telegram("🎉 【Offer God 補貨通知】文武廟的 Offer God 好像有貨啦！快去搶：https://temples.tungwahcsd.org/product/470")
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    check_stock()
