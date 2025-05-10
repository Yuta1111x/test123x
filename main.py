#!/usr/bin/env python3
import subprocess
import sys
import os

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], stdout=subprocess.DEVNULL)

# Upewnij się, że Flask jest zainstalowany
try:
    from flask import Flask, render_template_string
except ImportError:
    print("Flask nie znaleziony – instaluję…")
    install("flask")
    from flask import Flask, render_template_string

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    # Pobierz port z env (Render.com ustawia zmienną PORT), domyślnie 5000
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
