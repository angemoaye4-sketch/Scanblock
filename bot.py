import requests
import time
import telebot
from threading import Thread
from flask import Flask

# Tes identifiants réels
TOKEN = "8207003530:AAF18p_vZj200gSC0rCZBs5mrlsij1atUJo"
CHAT_ID = "1691499910"
bot = telebot.TeleBot(TOKEN)

# Mini serveur pour rester gratuit sur Render
app = Flask('')
@app.route('/')
def home(): return "Empire Scanner 3% Online"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def scan_empire():
    url = "https://api.dexscreener.com/latest/dex/search?q=USDT"
    while True:
        try:
            data = requests.get(url).json()
            pairs = data.get('pairs', [])
            for pair in pairs[:30]:
                m5_change = pair.get('priceChange', {}).get('m5', 0)
                # Alerte déclenchée à 3% ou plus
                if abs(m5_change) >= 1.15:
                    symbol = pair['baseToken']['symbol']
                    msg = f"🚀 **ALERTE EMPIRE (3%+)**\n\n💎 Jeton: {symbol}\n📈 Var: {m5_change}%\n🔗 [Lien]({pair['url']})"
                    bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        except: pass
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=run_web).start()
    scan_empire()
