from flask import Flask, render_template_string, request

# Flask tətbiqini yaradırıq
app = Flask(__name__)

# Yükləmələri saxlamaq üçün siyahımız
yuleme_tarixcesi = []

# ADMIN PANELİ SƏHİFƏSİ (Gizli)
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background-color: #000; color: #0f0; font-family: monospace; padding: 20px;">
    <h1>Admin Paneli - Yükləmələr</h1>
    <hr>
    <ul>
        {% for url in history %}
            <li>{{ url }}</li>
        {% endfor %}
    </ul>
    <br>
    <a href="/" style="color: #fff;">Ana Səhifəyə Qayıt</a>
</body>
</html>
"""

# ANA SƏHİFƏNİN KODU
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #121212; color: white; text-align: center; padding-top: 50px; font-family: Arial; }
        .box { background-color: #1e1e1e; padding: 30px; border-radius: 15px; display: inline-block; width: 90%; max-width: 300px; }
        input { width: 90%; padding: 10px; margin-bottom: 10px; }
        button { background-color: #ff0050; border: none; color: white; padding: 10px 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>TikTok Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura daxil edin..." required>
            <br>
            <button type="submit">Yüklə</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def ana_sehife():
    # ADMIN GİRİŞİ: Linkin sonuna ?login=hasan5500 yazanda bura düşəcək
    if request.args.get('login') == 'hasan5500':
        return render_template_string(ADMIN_HTML, history=yuleme_tarixcesi)
    
    # POST GƏLƏNDƏ: İstifadəçi linki yükləyəndə
    if request.method == 'POST':
        yeni_url = request.form.get('url')
        yuleme_tarixcesi.append(yeni_url)
        return "Video sistemə uğurla qeyd olundu! <br><a href='/'>Geri qayıt</a>"
    
    # NORMAL GİRİŞ: Əsas səhifəni göstər
    return render_template_string(HOME_HTML)

# SERVERİ BAŞLADIRIQ
if __name__ == '__main__':
    # Render üçün port nömrəsi
    app.run(host='0.0.0.0', port=10000)
