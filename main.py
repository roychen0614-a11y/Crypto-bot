import time
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1568213818125848758/aH_gU7m_h4mM1WevEHTOC-hWETL5u8d0k7e8glJgssVzrcdCxq3wchMe7gMfthhKyuQA"
TARGETS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT']

def send_startup_notification():
    """ 啟動時發送測試訊息確認連線 """
    try:
        payload = {
            "content": "🤖 **AI 監控機器人已成功啟動！**\n系統連線正常，開始 24 小時守護市場異常波動..."
        }
        res = requests.post(WEBHOOK_URL, json=payload)
        if res.status_code == 204 or res.status_code == 200:
            print("✅ 啟動測試訊息已成功發送至 Discord！")
        else:
            print(f"⚠️ 啟動訊息發送失敗，狀態碼：{res.status_code}")
    except Exception as e:
        print(f"❌ 發送啟動訊息發生錯誤: {e}")

# 1. 程式一啟動先發送測試訊息
send_startup_notification()

print("🤖 AI 異常監控機器人已啟動，正在背景運行...")

def check_market():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url)
        data = res.json()
        
        filtered = [item for item in data if item['symbol'] in TARGETS]
        
        for coin in filtered:
            symbol = coin['symbol'].replace('USDT', ' / USDT')
            change = float(coin['priceChangePercent'])
            price = float(coin['lastPrice'])
            
            if abs(change) >= 3.0:
                direction = "🚀 爆發急拉" if change > 0 else "⚠️ 恐慌下殺"
                payload = {
                    "content": f"**🚨 【市場異常波動警報】**\n"
                               f"• **標的**：`{symbol}`\n"
                               f"• **現價**：`$ {price:,.2f}`\n"
                               f"• **24h 漲跌**：`{change:+.2f}%`\n"
                               f"• **AI 判讀**：{direction}！請注意盤面風險與回測支撐。"
                }
                requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"錯誤: {e}")

while True:
    check_market()
    time.sleep(60)
