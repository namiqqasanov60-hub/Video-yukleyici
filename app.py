from flask import Flask, render_template_string, request, Response, send_file
import requests
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
history = []
visits = []

# HTML: Ana Səhifə (Seçim ekranı)
HOME_HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <title>7X HD Services</title>
    <style>
        body { font-family: sans-serif; background: #001f3f; color: white; text-align: center; padding: 50px; }
        .card { background: #003366; padding: 30px; border-radius: 20px; display: inline-block; margin: 10px; width: 250px; }
        button { padding: 15px 25px; background: #00e5ff; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; color: #001f3f; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>7X HD Services</h1>
    <div class="card">
        <h3>📥 Downloader</h3>
        <p>TikTok video yükləyici</p>
        <button onclick="location.href='/downloader'">Başla</button>
    </div>
    <div class="card">
        <h3>✨ Quality Enhancer</h3>
        <p>1080p 60FPS çevirici</p>
        <button onclick="location.href='/enhancer'">Başla</button>
    </div>
</body>
</html>
"""

# 1. Ana Səhifə (Seçim ekranı)
@app.route('/')
def index():
    return render_template_string(HOME_HTML)

# 2. Downloader Səhifəsi (Sənin köhnə kodun)
@app.route('/downloader', methods=['GET', 'POST'])
def downloader():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
        except: pass
    
    # Sənin əvvəlki HTML-ini bura qoydum
    return render_template_string("""
        <body style='background:#001f3f; color:white; text-align:center; padding:20px;'>
            <h1>Video Downloader</h1>
            <form method='POST'><input type='text' name='url' required><button type='submit'>Yüklə</button></form>
            {% if result %}<a href='/download?url={{ result }}'>Video Faylı (Yüklə)</a>{% endif %}
            <br><br><a href='/'>Geri</a>
        </body>""", result=result)

@app.route('/download')
def download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

# 3. Quality Enhancer Səhifəsi (Yeni)
@app.route('/enhancer', methods=['GET', 'POST'])
def enhancer():
    if request.method == 'POST':
        file = request.files['video']
        file.save('input.mp4')
        # FFmpeg ilə keyfiyyəti 1080p 60FPS-ə çevir
        subprocess.run(['ffmpeg', '-i', 'input.mp4', '-vf', 'scale=1080:1920', '-r', '60', '-b:v', '8M', 'output.mp4'])
        return send_file('output.mp4', as_attachment=True)
    
    return render_template_string("""
        <body style='background:#001f3f; color:white; text-align:center; padding:20px;'>
            <h1>Video Quality Enhancer</h1>
            <form method='POST' enctype='multipart/form-data'>
                <input type='file' name='video' required><br><br>
                <button type='submit'>Yüklə və Keyfiyyəti Artır</button>
            </form>
            <br><a href='/'>Geri</a>
        </body>""")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
