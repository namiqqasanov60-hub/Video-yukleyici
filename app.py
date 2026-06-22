from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        url = request.form.get('url')
        # Daha stabil API ünvanı
        api_url = f"https://api.cobalt.tools/api/json"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        payload = {"url": url}
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            result = response.json()
        except Exception as e:
            result = f"Xəta: {e}"
            
    return render_template_string('''
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura yapışdır" required>
            <button type="submit">Yüklə</button>
        </form>
        <pre>{{ result }}</pre>
    ''', result=result)

if __name__ == '__main__':
    app.run()
