from flask import Flask, render_template_string, request, redirect
from datetime import datetime

# Flask tətbiqini yaradırıq
app = Flask(__name__)

# Yükləmə tarixçəsini saxlamaq üçün boş bir siyahı yaradırıq
download_history = []

# HTML_HOME: İstifadəçilərin gördüyü ana səhifə
HTML_HOME = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <style>
        body { 
            background: #0f0f0f; 
            color: #ffffff; 
            font-family: 'Segoe UI', sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
        }
        .main-box { 
            background: #1c1c1c; 
            padding: 50px; 
            border-radius: 25px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.5); 
            text-align: center; 
            width: 450px; 
        }
        h1 { color: #ff0050; margin-bottom: 20px; }
        input { 
            width: 100%; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 10px; 
            border: 1px solid #333; 
            background: #2a2a2a; 
            color: white; 
        }
        button { 
            background: #ff0050; 
            border: none; 
            padding: 15px 30px; 
            color: white; 
            border-radius: 10px; 
            cursor: pointer; 
            font-weight: bold; 
            width: 100%; 
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="main-box">
        <h1>TikTok Yükləyici</h1>
        <form method="POST" action="/yukle_prosesi">
            <input type="text" name="url" placeholder="Video linkini bura yapışdırın..." required>
            <button type="submit">Yükləməyə Başla</button>
        </form>
    </div>
</body>
</html>
"""

# HTML_ADMIN: Sənin gizli admin panelin
HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; padding: 40px; }
        .log-container { border: 2px solid #00ff41; padding: 25px; border-radius: 15px; }
    </style>
</head>
<body>
    <h1>ADMIN PANELİ</h1>
    <div class="log-container">
        <h3>İstifadəçi Yükləmələri:</h3>
        <ul>
            {% for item in history %}
                <li>{{ item }}</li>
            {% endfor %}
        </ul>
    </div>
    <br><a href="/" style="color: white;">Ana səhifəyə qayıt</a>
</body>
</html>
"""

# Əsas marşrut (Main Route)
@app.route('/')
def ana_sehife():
    # Şifrə yoxlanışı
    if request.args.get('login') == 'hasan5500':
        return render_template_string(HTML_ADMIN, history=download_history[-20:])
    return render_template_string(HTML_HOME)

# Video yükləmə funksiyası
@app.route('/yukle_prosesi', methods=['POST'])
def yukle_prosesi():
    video_url = request.form.get('url')
    # Tarixi qeyd edirik
    zaman = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_mesaji = f"[{zaman}] - Yeni link: {video_url}"
    download_history.append(log_mesaji)
    return "<h1>Uğurlu!</h1><p>Video bazaya əlavə edildi.</p><a href='/'>Geri qayıt</a>"

# Serveri işə salırıq
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
