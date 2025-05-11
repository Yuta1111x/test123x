#!/usr/bin/env python3
import subprocess
import sys
import threading
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

HTML = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Animacja Siema!</title>
    <style>
        body { display:flex; justify-content:center; align-items:center;
               height:100vh; margin:0; background:#222; }
        h1 { font-family:'Arial',sans-serif; font-size:5rem;
             color:#fff; text-transform:uppercase;
             animation: glow 1.5s ease-in-out infinite alternate,
                        scale 1.5s ease-in-out infinite alternate; }
        @keyframes glow {
            from { text-shadow:0 0 10px #0f0; }
            to   { text-shadow:0 0 20px #0f0, 0 0 30px #0f0; }
        }
        @keyframes scale {
            from { transform:scale(1); }
            to   { transform:scale(1.1); }
        }
    </style>
</head>
<body>
    <h1>Siema!</h1>
</body>
</html>
"""

def send_embed(url, count, total):
    payload = {
        "embeds": [{
            "title": f"Wizyta #{count}/{total}",
            "description": f"Strona: {url}",
            "color": 4838850
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
    send_embed(current_url, count, total)
    threading.Thread(target=trigger_next, args=(count,), daemon=True).start()
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
