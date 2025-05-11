#!/usr/bin/env python3
import subprocess
import sys
import os
import threading

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL)

# Upewnij się, że Flask i requests są zainstalowane
try:
    from flask import Flask, render_template_string, request
except ImportError:
    install("flask")
    from flask import Flask, render_template_string, request

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    install("requests")
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

app = Flask(__name__)

# Konfiguracja z ENV
WEBHOOK_URL  = os.getenv("WEBHOOK_URL", "https://discord.com/api/webhooks/…")  # Twój webhook
TOTAL_SITES  = int(os.getenv("TOTAL_SITES", "30"))   # 30 stron w łańcuchu
NEXT_URL     = os.getenv("NEXT_URL", "").strip()     # URL następnej instancji, np. https://test123x-ejhl.onrender.com

# Sesja requests z retry dla POST i GET
session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["POST", "GET"]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)
session.mount("http://", adapter)

HTML = """
<!DOCTYPE html>
<html lang="pl">
<head><meta charset="UTF-8"><title>Animacja Siema!</title>
<style>
  body { display:flex; justify-content:center; align-items:center;
         height:100vh;margin:0;background:#222; }
  h1 { font-family:'Arial',sans-serif;font-size:5rem;
       color:#fff;text-transform:uppercase;
       animation: glow 1.5s ease-in-out infinite alternate,
                  scale 1.5s ease-in-out infinite alternate; }
  @keyframes glow {
    from { text-shadow:0 0 10px #0f0; }
    to   { text-shadow:0 0 20px #0f0,0 0 30px #0f0; }
  }
  @keyframes scale {
    from { transform:scale(1); }
    to   { transform:scale(1.1); }
  }
</style>
</head>
<body><h1>Dobry Deń</h1></body>
</html>"""

def send_embed(ip_address, visit_number):
    embed = {
        "embeds": [{
            "title": f"Wizyta #{visit_number}/{TOTAL_SITES}",
            "description": f"IP klienta: `{ip_address}`",
            "color": 4838850
        }]
    }
    try:
        resp = session.post(WEBHOOK_URL, json=embed, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        print(f"⚠️ Błąd wysyłki embed: {e}", file=sys.stderr)

def trigger_next(count):
    if not NEXT_URL or count >= TOTAL_SITES:
        return
    nxt_count = count + 1
    next_call = f"{NEXT_URL}?count={nxt_count}"
    try:
        session.get(next_call, timeout=5)
    except Exception as e:
        print(f"⚠️ Błąd chain do {next_call}: {e}", file=sys.stderr)

@app.route("/")
def home():
    # Odczytujemy count z query string: ?count=N
    count = int(request.args.get("count", "1"))
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    # Wyślij webhook z numerem wizyty
    send_embed(ip, count)
    # W tle wyzwól kolejną stronę
    threading.Thread(target=trigger_next, args=(count,), daemon=True).start()
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
