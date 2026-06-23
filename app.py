From flask import Flask, render_template_string, request, Response
import requests
import os
from datetime import datetime

app = Flask(__name__)
history = [] # Yüklənən videolar
visits = []  # Sayta daxil olanlar (yalnız vaxt)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url: return "URL tapılmadı", 400
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7X HD Downloader</title>
    <style>
        body { font-family: sans-serif; background: #001f3f; color: white; padding: 20px; text-align: center; margin: 0; }
        .container { max-width: 400px; margin: auto; background: #003366; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .sunar { font-size: 12px; opacity: 0.7; margin-bottom: 10px; }
        .pp { width: 100px; height: 100px; border-radius: 50%; border: 3px solid #00e5ff; margin-bottom: 15px; }
        input { padding: 12px; width: 85%; border-radius: 10px; border: none; margin-bottom: 15px; text-align: center; }
        button { padding: 12px 25px; background: #00e5ff; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; color: #001f3f; }
        .result { margin-top: 20px; padding: 15px; background: #004080; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="sunar">qwsdayi77x sunar:)</div>
        <img src="{{ url_for('static', filename='IMG-20260623-WA0027.jpg') }}" class="pp">
        <h1>7X HD Downloader</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura yapışdır..." required>
            <br><button type="submit">Search & Download</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="/download?url={{ result }}" style="color:#ffffff; font-weight:bold; text-decoration:none;">Download Now</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # Ziyarətçi vaxtını qeydə al (IP-siz)
    visits.insert(0, datetime.now().strftime('%H:%M:%S'))
    if len(visits) > 50: visits.pop()

    if request.args.get('login') == 'hasan5500':
        admin_html = """
        <body style='background:#001f3f; color:#fff; padding:20px; font-family:sans-serif;'>
            <h1>Admin Panel</h1>
            <h3>Son 100 Yükləmə</h3>
            <ul style='font-size:12px;'>{% for i in history %}<li>{{ i }}</li>{% endfor %}</ul>
            <h3>Son 50 Ziyarət (Vaxt)</h3>
            <ul style='font-size:12px;'>{% for i in visits %}<li>{{ i }}</li>{% endfor %}</ul>
            <a href='/' style='color:#00e5ff;'>Geri qayıt</a>
        </body>"""
        return render_template_string(admin_html, history=history, visits=visits)
    
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                history.insert(0, url)
                if len(history) > 100: history.pop()
        except: pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
