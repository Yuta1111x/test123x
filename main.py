#!/usr/bin/env python3
import subprocess
import sys
import threading
import random
from flask import Flask, render_template_string, request
import requests

# Upewnij się, że requests jest zainstalowane
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1340672206266568765/12pQ2cmefEuykpwQwSUed-YIsloEO6fRbpn4FXpAYjk19MqXtHCK-y69yRGZqrut2Clr"

URLS = [
    "https://test123x.onrender.com",
    "https://test123x-ejhl.onrender.com",
    "https://test123x-qng3.onrender.com",
    "https://test123x-td7x.onrender.com",
    "https://test123x-whm5.onrender.com",
    "https://test123x-fhsv.onrender.com",
    "https://test123x-5hkm.onrender.com",
    "https://test123x-13j4.onrender.com",
    "https://test123x-tfni.onrender.com",
    "https://test123x-h0wm.onrender.com",
    "https://test123x-4mqg.onrender.com",
    "https://test123x-f1v7.onrender.com",
    "https://test123x-1n2w.onrender.com",
    "https://test123x-tybd.onrender.com",
    "https://test123x-6phh.onrender.com",
    "https://test123x-7t0f.onrender.com",
    "https://test123x-zk4e.onrender.com",
    "https://test123x-8my4.onrender.com",
    "https://test123x-a3ad.onrender.com",
    "https://test123x-51ov.onrender.com",
    "https://test123x-n5zn.onrender.com",
    "https://test123x-mce0.onrender.com",
    "https://test123x-uqt3.onrender.com",
    "https://test123x-u1jd.onrender.com",
    "https://test123x-ipkq.onrender.com",
    "https://test123x-vgir.onrender.com",
    "https://test123x-lwz6.onrender.com",
    "https://test123x-svqr.onrender.com",
    "https://test123x-24jy.onrender.com",
    "https://test123x-j75y.onrender.com",
]

# 100 losowych powitań
GREETINGS = [
    "Witaj, podróżniku!",
    "Hejka!",
    "Siemanko!",
    "Dzień dobry!",
    "Szczęść Boże!",
    "Czołem!",
    "Pozdrawiam!",
    "Hej ho!",
    "Yo!",
    "Hola!",
    "Salam!",
    "Serwus!",
    "Hej!",
    "Witam serdecznie!",
    "Hej, jak tam?",
    "Siema!",
    "Co słychać?",
    "Wszystkiego dobrego!",
    "Cześć!",
    "Dobrego dnia!",
    "Miłego dnia!",
    "Udanego dnia!",
    "Wspaniałego dnia!",
    "Radosnego dnia!",
    "Ciepłego powitania!",
    "Wesołych wędrówek!",
    "Pozdrawiam ciepło!",
    "Zdrów bądź!",
    "Moc pozdrowień!",
    "Hejka, hejka!",
    "Hej, hej!",
    "Witaj!",
    "Hej, hej, hej!",
    "Czołem, czołem!",
    "Yo, yo!",
    "Salute!",
    "Salut!",
    "Grüß dich!",
    "Buongiorno!",
    "Bonjour!",
    "Good day!",
    "Good morning!",
    "Guten Tag!",
    "Buonasera!",
    "Bonsoir!",
    "Buena día!",
    "Halo!",
    "Hej, ho!",
    "Witam!",
    "Witajcie!",
    "Czołgiem!",
    "Dzień dobry wszystkim!",
    "Witam wszystkich!",
    "Hello!",
    "Hej, witaj!",
    "Pozdrowienia!",
    "Miło cię widzieć!",
    "Fajnie, że jesteś!",
    "Cześć, cześć!",
    "Słońca na drodze!",
    "Siema, ziomek!",
    "Siema, siema!",
    "Hej, jak leci?",
    "Co tam?",
    "Hej, hej, hej!",
    "Hej, co słychać?",
    "Pozdrawiam serdecznie!",
    "Witaj w sieci!",
    "Witaj w necie!",
    "Witaj w cyfrowym świecie!",
    "Cześć wirtualnie!",
    "Cześć online!",
    "Siema w sieci!",
    "Yo, welcome!",
    "Yo, witaj!",
    "Yo, pozdro!",
    "Yo, cześć!",
    "What’s up!",
    "Howdy!",
    "G’day!",
    "Sup!",
    "Halo, halo!",
    "Witaj w mojej aplikacji!",
    "Witam w moim świecie!",
    "Pozdrowienia z serwera!",
    "Serwer pozdrawia!",
    "Masz dziś szczęście!",
    "Dzień dobry z serwera!",
    "Hej z serwera!",
    "Cześć z serwera!",
    "Witaj ponownie!",
    "Miło znowu cię widzieć!",
    "Znowu z tobą!",
    "Znowu tu jesteś!",
    "Znowu my się widzimy!",
    "Hola, amigo!",
    "Hola, amiga!",
    "Saludos!",
    "Hej, dawno nie było!",
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Animacja</title>
    <style>
        body {{ display:flex; justify-content:center; align-items:center;
               height:100vh; margin:0; background:#222; }}
        h1 {{ font-family:'Arial',sans-serif;font-size:4rem;
             color:#fff;text-transform:uppercase;
             animation: glow 1.5s ease-in-out infinite alternate,
                        scale 1.5s ease-in-out infinite alternate; }}
        @keyframes glow {{
            from {{ text-shadow:0 0 10px #0f0; }}
            to   {{ text-shadow:0 0 20px #0f0,0 0 30px #0f0; }}
        }}
        @keyframes scale {{
            from {{ transform:scale(1); }}
            to   {{ transform:scale(1.1); }}
        }}
    </style>
</head>
<body>
    <h1>{{ greeting }}</h1>
</body>
</html>
"""

def send_embed(url, count, total, greeting):
    payload = {
        "embeds": [{
            "title":       f"Wizyta #{count}/{total}",
            "description": f"Strona: {url}\nPowitanie: {greeting}",
            "color":       4838850
        }]
    }
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"⚠️ Błąd wysyłki embed: {e}", file=sys.stderr)

def trigger_next(count):
    total = len(URLS)
    if count >= total:
        return
    next_count = count + 1
    next_url = URLS[next_count - 1]
    try:
        requests.get(f"{next_url}/?count={next_count}", timeout=5)
    except Exception as e:
        print(f"⚠️ Błąd wywołania {next_url}: {e}", file=sys.stderr)

@app.route("/")
def home():
    count = int(request.args.get("count", "1"))
    total = len(URLS)
    current_url = URLS[count - 1]
    greeting = random.choice(GREETINGS)
    send_embed(current_url, count, total, greeting)
    threading.Thread(target=trigger_next, args=(count,), daemon=True).start()
    return render_template_string(HTML_TEMPLATE, greeting=greeting)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
