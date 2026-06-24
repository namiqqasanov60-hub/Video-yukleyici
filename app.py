from flask import Flask, render_template_string, request, Response
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #001f3f; color: white; text-align: center; padding: 20px; }
        .container { max-width: 400px; margin: auto; background: #003366; padding: 25px; border-radius: 20px; }
        .pp { width: 100px; height: 100px; border-radius: 50%; border: 3px solid #00e5ff; }
        input { padding: 12px; width: 85%; margin-bottom: 10px; border-radius: 10px; border: none; text-align: center; }
        button { padding: 12px 25px; background: #00e5ff; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; color: #001f3f; }
        .result { margin-top: 20px; padding: 15px; background: #004080; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://i.imgur.com/Q6XzY6n.png" class="pp">
        <h1>7X HD Services</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok link..." required>
            <br><button type="submit">Download</button>
        </form>
        {% if result %}
            <div class="result">
                <a href="/download?url={{ result }}" style="color:#ffffff; font-weight:bold; text-decoration:none;">Click to Download</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # API sorğusu
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0: 
                result = data['data']['play']
        except: 
            pass
    return render_template_string(HTML_TEMPLATE, result=result)

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url: return "URL tapılmadı", 400
    try:
        r = requests.get(url, stream=True)
        return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})
    except:
        return "Yükləmə xətası", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
