from flask import Flask, render_template_string, request, Response
import requests
import os

app = Flask(__name__)

# Yükləmə tarixçəsini yadda saxlamaq üçün siyahı
history = []

@app.route('/download')
def download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        .signature { color: #888; font-size: 14px; margin-bottom: 15px; }
        input { padding: 12px; width: 80%; border-radius: 8px; border: none; margin-bottom: 10px; }
        button { padding: 12px 25px; background: #ff0050; color: white; border: none; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>TikTok Yükləyici</h2>
        <div class="signature">by Avara Hasan</div>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <br><button type="submit">Tap və Yüklə</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="/download?url={{ result }}" style="background:#00e5ff; padding:12px; text-decoration:none; color:black; border-radius:8px; font-weight:bold;">Birbaşa Yüklə</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # GİZLİ ADMIN GİRİŞİ: Linkin sonuna ?login=hasan5500 yazanda bura düşür
    if request.args.get('login') == 'hasan5500':
        return render_template_string("<body style='background:black; color:#0f0; font-family:monospace; padding:20px;'><h1>Admin Paneli</h1><ul>{% for i in history %}<li>{{i}}</li>{% endfor %}</ul><a href='/'>Geri qayıt</a></body>", history=history)
    
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                history.append(url) # Linki tarixçəyə əlavə edirik
        except: pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
