from flask import Flask, render_template_string, request, Response, send_file
import requests
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
history = [] 
visits = [] 

# Sənin orijinal dizaynın (heç nəyi dəyişmədim, sadəcə menyu əlavə etdim)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>7X HD Services</title>
    <style>
        body { font-family: sans-serif; background: #001f3f; color: white; padding: 20px; text-align: center; margin: 0; }
        .container { max-width: 400px; margin: auto; background: #003366; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .pp { width: 100px; height: 100px; border-radius: 50%; border: 3px solid #00e5ff; margin-bottom: 15px; }
        input { padding: 12px; width: 85%; border-radius: 10px; border: none; margin-bottom: 15px; text-align: center; }
        button { padding: 12px 25px; background: #00e5ff; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; color: #001f3f; margin: 5px; }
        .result { margin-top: 20px; padding: 15px; background: #004080; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://i.imgur.com/your-image-link-here.jpg" class="pp">
        <h1>7X HD Services</h1>
        {% if page == 'home' %}
            <button onclick="location.href='/downloader'">TikTok Downloader</button><br>
            <button onclick="location.href='/enhancer'">2K 60FPS Enhancer</button>
        {% elif page == 'downloader' %}
            <form method="POST">
                <input type="text" name="url" placeholder="Paste TikTok link here..." required>
                <br><button type="submit">Search & Download</button>
            </form>
            {% if result %}<div class="result"><a href="/download?url={{ result }}" style="color:white; font-weight:bold;">Download Now</a></div>{% endif %}
            <br><a href="/" style="color:#00e5ff;">Back to Home</a>
        {% elif page == 'enhancer' %}
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="video" accept="video/*" required>
                <br><button type="submit">Process Video</button>
            </form>
            <br><a href="/" style="color:#00e5ff;">Back to Home</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, page='home')

@app.route('/downloader', methods=['GET', 'POST'])
def downloader():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: result = data['data']['play']
        except: pass
    return render_template_string(HTML_TEMPLATE, page='downloader', result=result)

@app.route('/enhancer', methods=['GET', 'POST'])
def enhancer():
    if request.method == 'POST':
        file = request.files['video']
        file.save('input.mp4')
        cmd = ['ffmpeg', '-y', '-i', 'input.mp4', '-vf', 'scale=1080:1920', '-c:v', 'libx264', '-crf', '18', '-r', '60', '-b:v', '8M', 'output.mp4']
        subprocess.run(cmd)
        return send_file('output.mp4', as_attachment=True, download_name='Enhanced_2K_60FPS.mp4')
    return render_template_string(HTML_TEMPLATE, page='enhancer')

@app.route('/download')
def download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
