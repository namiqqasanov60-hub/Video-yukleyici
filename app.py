from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# CSS daxil edilmiş gözəl dizayn
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #121212; color: white; padding: 50px; }
        input { padding: 15px; width: 300px; border-radius: 10px; border: none; }
        button { padding: 15px 30px; background: #ff0050; color: white; border: none; border-radius: 10px; cursor: pointer; }
        .result { margin-top: 20px; font-size: 18px; }
        a { color: #00e5ff; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1>TikTok 4K Yükləyici</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="TikTok linkini bura yapışdır..." required>
        <button type="submit">Yüklə</button>
    </form>
    <div class="result">
        {% if result %}
            <p>Video tapıldı: <a href="{{ result }}" target="_blank">İndi Yüklə</a></p>
        {% elif result == 'Video tapılmadı.' %}
            <p style="color:red;">{{ result }}</p>
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
            else:
                result = "Video tapılmadı."
        except Exception:
            result = "Xəta baş verdi."
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

