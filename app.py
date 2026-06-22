from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Yükləyici</title>
</head>
<body>
    <div class="container">
        <h2>Video Yükləyici</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura yapışdır" required>
            <button type="submit">Yüklə</button>
        </form>
        {% if video_url %}
            <br>
            <a href="{{ video_url }}" download>Videonur yüklə</a>
        {% endif %}
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
        try:
            # SSL xətasını aradan qaldıran hissə buradır:
            response = requests.get(api_url, verify=False)
            data = response.json()
            if data['status'] == 'success':
                video_url = data['video']
            else:
                error = "Video tapılmadı."
        except Exception as e:
            error = f"Xəta baş verdi: {e}"
    return render_template_string(HTML_TEMPLATE, video_url=video_url, error=error)

if __name__ == '__main__':
    app.run(debug=True)
