from flask import Flask, render_template_string, request

app = Flask(__name__)
history = []

# BÜTÜN DİZAYN BURADADIR (CSS İÇİNDƏ)
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background-color: #121212; color: white; text-align: center; font-family: Arial; padding: 20px; }
        .box { background-color: #1e1e1e; padding: 30px; border-radius: 15px; max-width: 400px; margin: 20px auto; }
        input { width: 90%; padding: 12px; margin-bottom: 10px; border-radius: 5px; border: none; }
        button { background-color: #ff0050; border: none; color: white; padding: 12px 30px; border-radius: 5px; cursor: pointer; }
        a { color: #00ff41; text-decoration: none; }
    </style>
</head>
<body>
    <div class="box">
        <h2>TikTok Downloader</h2>
        <form method="POST" action="/save">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <br>
            <button type="submit">Yüklə</button>
        </form>
    </div>
</body>
</html>
"""

# ADMIN PANELİ
ADMIN_HTML = """
<body style="background:black; color:#0f0; font-family:monospace; padding:20px;">
    <h2>Admin Paneli</h2>
    <ul>{% for i in history %}<li>{{ i }}</li>{% endfor %}</ul>
    <a href="/">Geri Qayıt</a>
</body>
"""

@app.route('/')
def index():
    if request.args.get('login') == 'hasan5500':
        return render_template_string(ADMIN_HTML, history=history)
    return render_template_string(HTML_CODE)

@app.route('/save', methods=['POST'])
def save():
    url = request.form.get('url')
    history.append(url)
    return "<h2>Video qeyd olundu!</h2><a href='/'>Geri qayıt</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
