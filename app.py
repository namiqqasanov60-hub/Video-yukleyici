from flask import Flask, render_template_string, request
import requests
import urllib3

# SSL xəbərdarlıqlarını tamamilə söndürür
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
        try:
            # Burda verify=False qoyuruq və bu dəfə işləməlidir
            response = requests.get(api_url, verify=False, timeout=10)
            return str(response.json())
        except Exception as e:
            return f"Xəta: {e}"
    return '''<form method="POST"><input name="url"><button>Yüklə</button></form>'''

if __name__ == '__main__':
    app.run()
