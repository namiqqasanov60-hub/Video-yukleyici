from flask import Flask, render_template_string, request, Response, send_file
import requests
import os
import subprocess
from datetime import datetime

app = Flask(__name__)
history = [] 
visits = [] 

# Tam ekran mobil görünüş üçün yeni CSS
CSS = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #000; color: #fff; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .mobile-card { width: 100%; height: 100vh; background: #0a0a0a; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: none; }
    h1 { color: #00e5ff; font-size: 28px; margin-bottom: 40px; }
    input { width: 85%; padding: 18px; margin: 10px 0; border-radius: 15px; border: 1px solid #333; background: #111; color: white; font-size: 16px; }
    button { width: 90%; padding: 18px; background: #00e5ff; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; color: #000; font-size: 18px; margin: 10px 0; transition: 0.2s; }
    button:active { transform: scale(0.98); }
    a { color: #00e5ff; text-decoration: none; font-weight: bold; font-size: 16px; margin-top: 20px; }
</style>
"""

@app.route('/')
def index():
    visits.insert(0, datetime.now().strftime('%H:%M:%S'))
    return render_template_string(CSS + """
        <div class="mobile-card">
            <h1>7X HD Services</h1>
            <button onclick="location.href='/downloader'">TikTok Downloader</button>
            <button onclick="location.href='/enhancer'">2K 60FPS Enhancer</button>
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
        <div class="mobile-card">
            <h1>TikTok Downloader</h1>
            <form method='POST'><input type='text' name='url' placeholder='Paste link here...' required><button type='submit'>Search & Download</button></form>
            {% if result %}<br><a href='/download?url={{ result }}'>Download Now</a>{% endif %}
            <br><a href='/'>Back to Home</a>
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
        cmd = [
            'ffmpeg', '-y', '-i', 'input.mp4',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-r', '60', '-b:v', '8M', '-c:a', 'aac', 'output.mp4'
        ]
        subprocess.run(cmd)
        return send_file('output.mp4', as_attachment=True, download_name='Enhanced_2K_60FPS.mp4')
    return render_template_string(CSS + """
        <div class="mobile-card">
            <h1>2K 60FPS Quality</h1>
            <form method='POST' enctype='multipart/form-data'>
                <input type='file' name='video' accept='video/*' required>
                <button type='submit'>Process Video</button>
            </form>
            <br><a href='/'>Back to Home</a>
        </div>
    """)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
