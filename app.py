from flask import Flask, render_template_string, request
from datetime import datetime

# Flask tətbiqini yaradırıq
app = Flask(__name__)

# Yükləmə tarixçəsini saxlayırıq
history = []

# Dizaynlı ana səhifə (HTML + CSS)
HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #121212; color: white; text-align: center; font-family: Arial; padding-top: 50px; }
        .box { background: #1e1e1e; padding: 40px; border-radius: 20px; display: inline-block; width: 85%; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        input { width: 90%; padding: 15px; margin-bottom: 20px; border-radius: 10px; border: none; }
        button { background: #ff0050; border: none; color: white; padding: 15px 30px; border-radius: 10px; cursor: pointer; width: 100%; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h2>TikTok Downloader</h2>
        <form method="POST" action="/yukle">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <button type="submit">İndi Yüklə</button>
        </form>
    </div>
</body>
</html>
"""

# Admin Paneli (Yaşıl Matrix stili)
HTML_ADMIN = """
<body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
    <h1>Admin Paneli</h1>
    <ul>{% for item in history %}<li>{{ item }}</li>{% endfor %}</ul>
    <a href="/" style="color:white;">Ana səhifəyə qayıt</a>
</body>
"""

@app.route('/')
def index():
    # Admin girişini yoxlayırıq
    if request.args.get('login') == 'hasan5500':
        return render_template_string(HTML_ADMIN, history=history)
    return render_template_string(HTML_HOME)

@app.route('/yukle', methods=['POST'])
def yukle():
    url = request.form.get('url')
    zaman = datetime.now().strftime("%H:%M:%S")
    history.append(f"[{zaman}] - {url}")
    return "<h1>Uğurlu!</h1><a href='/'>Geri qayıt</a>"

if __name__ == '__main__':
    # Serveri render üçün port 10000-də başladırıq
    app.run(host='0.0.0.0', port=10000)
