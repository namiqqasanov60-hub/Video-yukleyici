from flask import Flask, render_template_string, request, Response
import requests
import os

app = Flask(__name__)

history = []

@app.route('/download')
def download():
    url = request.args.get('url')
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Doğrulama Kodu -->
    <meta name="google-site-verification" content="E3yGcFPsBBQddg8Lphv4Dgd2baI7YnaRYfC8O9m300A" />
    
    <title>TikTok Video Downloader 4K - Fast & Free</title>
    <meta name="description" content="Download TikTok videos in 4K quality, without watermarks. The fastest TikTok video downloader.">
    <meta name="keywords" content="TikTok Video Downloader 4K, download tiktok video, tiktok downloader, no watermark tiktok">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        .signature { color: #888; font-size: 14px; margin-bottom: 20px; }
        input { padding: 15px; width: 85%; border-radius: 10px; border: none; margin-bottom: 15px; }
        button { padding: 15px 30px; background: #ff0050; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; width: 90%; }
        .result { margin-top: 20px; padding: 20px; background: #252525; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TikTok Video Downloader 4K</h1>
        <div class="signature">by Avara Hasan</div>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste TikTok link here..." required>
            <br><button type="submit">Search & Download</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video found!</p>
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
        except: pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
