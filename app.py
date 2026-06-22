from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
    <h2>Video Yükləyici</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Link-i bura yapışdır" required>
        <button type="submit">Yüklə</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
        try:
            # Burda verify=False əlavə olunub
            response = requests.get(api_url, verify=False, timeout=15)
            return str(response.json())
        except Exception as e:
            return f"Xəta: {e}"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()
