from flask import Flask, render_template_string, request, Response
import requests, os

app = Flask(__name__)

# Bunlar sənin botunun məlumatlarıdır
BOT_TOKEN = "8952152625:AAFDJsXWczrRUBsU49w-i_0y7ZSSr-mhiAs"
CHAT_ID = "7471806843"

@app.route('/download')
def download():
    url = request.args.get('url')
    # Yükləmə düyməsinə basılan kimi Telegram-a mesaj gedir
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Hasan,%20yeni%20video%20yükləndi!")
    except:
        pass
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        input { padding: 12px; width: 80%; border-radius: 8px; border: none; margin-bottom: 10px; }
        button { padding: 12px 25px; background: #ff0050; color: white; border: none; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>TikTok Yükləyici</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <br><button type="submit">Tap və Yüklə</button>
        </form>
        {% if result %}
            <br><a href="/download?url={{ result }}" style="background:#00e5ff; padding:12px; text-decoration:none; color:black; border-radius:8px; font-weight:bold;">Birbaşa Yüklə</a>
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
            # TikTok-dan videonu tapırıq
            data = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if data.get('code') == 0:
                result = data['data']['play']
        except:
            pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
