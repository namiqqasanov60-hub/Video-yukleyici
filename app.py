from flask import Flask, render_template_string, request, Response
import requests
from datetime import datetime

app = Flask(__name__)

# Məlumatları yadda saxlamaq üçün (server restart olunanda bunlar silinəcək)
history = [] 
visits = [] 

# CSS və HTML bir yerdə: Mobil üçün optimallaşdırılmış "App" görünüşü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>7X HD Services</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #050505; color: #fff; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .app-container { width: 100%; max-width: 400px; background: #111; padding: 30px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #222; }
        .pp { width: 110px; height: 110px; border-radius: 25px; border: 4px solid #00e5ff; margin-bottom: 20px; object-fit: cover; }
        h1 { font-size: 24px; margin-bottom: 25px; color: #00e5ff; }
        input { width: 100%; padding: 18px; box-sizing: border-box; border-radius: 15px; border: none; background: #222; color: white; font-size: 16px; margin-bottom: 15px; text-align: center; }
        button { width: 100%; padding: 18px; background: #00e5ff; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; color: #000; font-size: 16px; transition: 0.3s; }
        button:active { transform: scale(0.98); }
        .result-box { margin-top: 25px; padding: 20px; background: #1a1a1a; border-radius: 15px; border: 1px solid #333; }
        a { color: #00e5ff; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="app-container" style="text-align: center;">
        <img src="https://i.imgur.com/Q6XzY6n.png" class="pp">
        <h1>7X HD Services</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste TikTok Link..." required>
            <button type="submit">Download Video</button>
        </form>
        {% if result %}
            <div class="result-box">
                <p style="color: #ccc;">Video Found!</p>
                <a href="/download?url={{ result }}" style="font-size: 18px;">Download Now</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # Ziyarətçi qeydi
    visits.insert(0, datetime.now().strftime('%H:%M:%S'))
    if len(visits) > 50: visits.pop()

    # Admin Panel (linkin sonuna ?login=hasan5500 yaz)
    if request.args.get('login') == 'hasan5500':
        return render_template_string("""
        <body style='background:#000; color:#fff; padding:20px; font-family:sans-serif;'>
            <h2>Admin Panel</h2>
            <h3>History (Last 50)</h3>
            <ul>{% for i in history %}<li>{{ i }}</li>{% endfor %}</ul>
            <a href='/'>Back to Home</a>
        </body>""", history=history)

    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                history.insert(0, url)
                if len(history) > 50: history.pop()
        except: pass
    return render_template_string(HTML_TEMPLATE, result=result)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url: return "URL Error", 400
    try:
        r = requests.get(url, stream=True)
        return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})
    except: return "Download failed", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
