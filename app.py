from flask import Flask, render_template_string, request, Response, send_file
import requests
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
history = [] 
visits = [] 

# İndi CSS ekranı tam doldurur və SnapTik kimi professional görünür
CSS = """
<style>
    body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0; display: flex; justify-content: center; min-height: 100vh; }
    .container { width: 100%; max-width: 500px; background: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    .header { background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px; margin-bottom: 20px; }
    h1 { margin: 0; font-size: 22px; }
    input { width: 100%; padding: 15px; box-sizing: border-box; border: 2px solid #ddd; border-radius: 5px; margin-bottom: 10px; font-size: 16px; }
    button { width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 5px; font-size: 18px; font-weight: bold; cursor: pointer; }
    .card { background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 15px; }
    a { color: #007bff; text-decoration: none; font-weight: bold; }
</style>
"""

@app.route('/')
def index():
    visits.insert(0, datetime.now().strftime('%H:%M:%S'))
    return render_template_string(CSS + """
        <div class="container">
            <div class="header"><h1>7X HD Services</h1></div>
            <div class="card">
                <button onclick="location.href='/downloader'">TikTok Downloader</button>
            </div>
            <div class="card">
                <button style="background:#007bff;" onclick="location.href='/enhancer'">2K 60FPS Enhancer</button>
            </div>
        </div>
    """)

@app.route('/downloader', methods=['GET', 'POST'])
def downloader():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                history.insert(0, url)
        except: pass
    return render_template_string(CSS + """
        <div class="container">
            <div class="header"><h1>TikTok Video Downloader</h1></div>
            <form method='POST'><input type='text' name='url' placeholder='Paste TikTok link here...' required><button type='submit'>Download</button></form>
            {% if result %}<div class="card"><a href='/download?url={{ result }}'>Click to Download Now</a></div>{% endif %}
            <a href='/'>← Back to Home</a>
        </div>
    """, result=result)

@app.route('/download')
def download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

@app.route('/enhancer', methods=['GET', 'POST'])
def enhancer():
    if request.method == 'POST':
        file = request.files['video']
        file.save('input.mp4')
        cmd = ['ffmpeg', '-y', '-i', 'input.mp4', '-vf', 'scale=1080:1920', '-c:v', 'libx264', '-crf', '18', '-r', '60', '-b:v', '8M', '-c:a', 'aac', 'output.mp4']
        subprocess.run(cmd)
        return send_file('output.mp4', as_attachment=True, download_name='Enhanced_2K_60FPS.mp4')
    return render_template_string(CSS + """
        <div class="container">
            <div class="header"><h1>2K 60FPS Enhancer</h1></div>
            <form method='POST' enctype='multipart/form-data'><input type='file' name='video' accept='video/*' required><button type='submit'>Process & Enhance</button></form>
            <a href='/'>← Back to Home</a>
        </div>
    """)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
