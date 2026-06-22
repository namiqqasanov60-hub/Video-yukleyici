from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .container { max-width: 500px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        input { padding: 12px; width: 80%; border-radius: 8px; border: none; margin-bottom: 10px; }
        button { padding: 12px 25px; background: #ff0050; color: white; border: none; border-radius: 8px; cursor: pointer; }
        video { max-width: 100%; height: auto; margin-top: 20px; border-radius: 10px; }
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
            <div class="result">
                <p>Video tapıldı!</p>
                <!-- Avtomatik yükləmə üçün download atributu əlavə olundu -->
                <a href="{{ result }}" download="video.mp4" style="color: #00e5ff;">Faylı Yüklə</a>
                <br>
                <video controls>
                    <source src="{{ result }}" type="video/mp4">
                </video>
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
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url, timeout=10)
            data = response.json()
            if data.get('code') == 0:
                result = data['data']['play']
        except Exception:
            pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
