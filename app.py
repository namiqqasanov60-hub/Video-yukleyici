from flask import Flask, render_template_string, request, Response
import requests
import os

app = Flask(__name__)

# TikTok video yükləmə tarixi (son 10 link)
history = []

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
    <title>7X HD TikTok Video Downloader</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; padding: 10px; margin: 0; }
        .container { max-width: 400px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        input { padding: 12px; width: 90%; border-radius: 8px; border: none; margin-bottom: 10px; }
        button { padding: 12px; background: #ffcc00; border: none; border-radius: 8px; width: 100%; font-weight: bold; }
        .result { margin-top: 20px; padding: 15px; background: #252525; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>7X HD Downloader</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura yapışdır..." required>
            <button type="submit">Search & Download</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="/download?url={{ result }}" style="color:#00e5ff; font-weight:bold;">Download Now</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # Admin Panel: Mobilə uyğun dizayn
    if request.args.get('login') == 'hasan5500':
        admin_html = """
        <body style='background:black; color:#0f0; padding:20px; font-family:sans-serif;'>
            <h1>Son 10 Yüklənən Link</h1>
            <ul style='word-break: break-all;'>
                {% for i in history %}<li>{{ i }}</li>{% endfor %}
            </ul>
            <a href='/' style='color:white;'>Geri qayıt</a>
        </body>"""
        return render_template_string(admin_html, history=history)
    
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                # Linki siyahıya əlavə et və 10-dan çoxdursa köhnəni sil
                history.insert(0, url)
                if len(history) > 10: history.pop()
        except: pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
