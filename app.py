from flask import Flask, render_template_string, request, Response, url_for
import requests
import os

app = Flask(__name__)

# TikTok video yükləmə tarixi
history = []

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return "URL tapılmadı", 400
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="E3yGcFPsBBQddg8Lphv4Dgd2baI7YnaRYfC8O9m300A" />
    
    <title>7X HD TikTok Video Downloader</title>
    <meta name="description" content="Download TikTok videos in 4K quality, without watermarks.">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        .signature { color: #ffcc00; font-size: 16px; margin-bottom: 20px; font-weight: bold; }
        input { padding: 15px; width: 85%; border-radius: 10px; border: none; margin-bottom: 15px; }
        button { padding: 15px 30px; background: #ffcc00; color: black; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; width: 90%; }
        .result { margin-top: 20px; padding: 20px; background: #252525; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>7X HD Downloader</h1>
        <div class="signature">by Hasan_7X_Pro</div>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura yapışdır..." required>
            <br><button type="submit">Search & Download</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="/download?url={{ result }}" style="background:#00e5ff; padding:15px; text-decoration:none; color:black; border-radius:10px; font-weight:bold; display:block; margin-top:10px;">Download Now</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.args.get('login') == 'hasan5500':
        return render_template_string("<body style='background:black; color:#0f0; font-family:monospace; padding:20px;'><h1>Admin Panel</h1><ul>{% for i in history %}<li>{{i}}</li>{% endfor %}</ul><a href='/'>Back Home</a></body>", history=history)
    
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
                history.append(url)
        except: 
            pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
