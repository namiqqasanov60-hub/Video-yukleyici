import os
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # TikWM API-ı çox stabildir
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url, timeout=10)
            data = response.json()
            if data.get('code') == 0:
                result = data['data']['play']
            else:
                result = "Video tapılmadı."
        except Exception as e:
            result = f"Xəta: {e}"
            
    return render_template_string('''
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linki" required>
            <button type="submit">Yüklə</button>
        </form>
        {% if result %}
            <p>Video: <a href="{{ result }}" target="_blank">Video linki</a></p>
        {% endif %}
    ''', result=result)

# Render-in avtomatik portu tapması üçün
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
