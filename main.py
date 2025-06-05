from flask import Flask, render_template_string

app = Flask(__name__)

# Szablon HTML z przepięknymi stylami
template = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Przepiękna Strona ✨</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            position: relative;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .floating-shapes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 1;
        }

        .shape {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            width: 120px;
            height: 120px;
            top: 60%;
            right: 15%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            width: 60px;
            height: 60px;
            top: 80%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .main-content {
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
        }

        .hero-title {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradient 3s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .subtitle {
            font-size: 1.5rem;
            margin-bottom: 40px;
            opacity: 0.9;
            animation: fadeInUp 1s ease-out;
        }

        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            max-width: 1200px;
            margin-top: 50px;
        }

        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out;
        }

        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }

        .card h3 {
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: #ffd700;
        }

        .card p {
            line-height: 1.6;
            opacity: 0.9;
        }

        .btn {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            margin-top: 30px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            animation: sparkle 4s linear infinite;
        }

        @keyframes sparkle {
            0% {
                transform: translateY(100vh) scale(0);
                opacity: 1;
            }
            100% {
                transform: translateY(-10px) scale(1);
                opacity: 0;
            }
        }

        .footer {
            position: absolute;
            bottom: 20px;
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .subtitle {
                font-size: 1.2rem;
            }
            
            .cards-container {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="floating-shapes">
            <div class="shape"></div>
            <div class="shape"></div>
            <div class="shape"></div>
        </div>

        <div class="particles" id="particles"></div>

        <div class="main-content">
            <h1 class="hero-title">Witaj w Przyszłości! ✨</h1>
            <p class="subtitle">Przepiękna strona stworzona z Flask i miłością do designu</p>
            
            <div class="cards-container">
                <div class="card">
                    <h3>🚀 Nowoczesny Design</h3>
                    <p>Wykorzystujemy najnowsze trendy w web designie, z przepięknymi gradientami, animacjami i efektami glass morphism.</p>
                </div>
                
                <div class="card">
                    <h3>⚡ Super Szybka</h3>
                    <p>Zoptymalizowana pod kątem wydajności, zapewnia płynne doświadczenie użytkownika na wszystkich urządzeniach.</p>
                </div>
                
                <div class="card">
                    <h3>🎨 Responsywna</h3>
                    <p>Perfekcyjnie dostosowuje się do każdego ekranu - od smartfonów po duże monitory.</p>
                </div>
            </div>

            <button class="btn" onclick="showMessage()">Kliknij mnie! 🎉</button>
        </div>

        <div class="footer">
            <p>Stworzone z ❤️ przy użyciu Flask • Port 3000</p>
        </div>
    </div>

    <script>
        // Tworzenie animowanych cząsteczek
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 4 + 's';
                particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Funkcja dla przycisku
        function showMessage() {
            alert('🎉 Gratulacje! Twoja strona jest naprawdę przepiękna! ✨');
        }

        // Uruchomienie animacji cząsteczek
        createParticles();

        // Dodatkowe efekty przy ładowaniu strony
        window.addEventListener('load', function() {
            document.body.style.opacity = '1';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(template)

@app.route('/api/message')
def api_message():
    return {
        'message': 'Twoja strona działa perfekcyjnie! 🚀',
        'status': 'success',
        'port': 3000
    }

if __name__ == '__main__':
    print("🌟 Uruchamianie przepięknej strony Flask...")
    print("🚀 Strona będzie dostępna na: http://localhost:3000")
    print("✨ Przygotuj się na coś wyjątkowego!")
    
    # Uruchomienie bez debug mode aby uniknąć błędów z watchdogiem
    try:
        app.run(host='0.0.0.0', port=3000, debug=False)
    except Exception as e:
        print(f"❌ Błąd: {e}")
        print("🔄 Próbuję uruchomić na localhost...")
        app.run(host='127.0.0.1', port=3000, debug=False)
