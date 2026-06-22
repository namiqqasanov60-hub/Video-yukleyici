from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Yükləyici</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); display: inline-block; max-width: 90%; }
        input[type="text"] { width: 85%; padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        button { background-color: #28a745; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #218838; }
        .footer { margin-top: 20px; color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📥 Video Yükləyici</h2>
        <p>TikTok və ya Instagram linkini yapışdırın:</p>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="https://..." required>
            <br>
            <button type="submit">Videonu Tap və Yüklə</button>
        </form>
        <div class="footer">7/24 Aktiv Xidmət</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    
    # TikTok blokunu aşmaq üçün açıq API xidməti
    api_url = f"https://api.tiklydown.eu.org/api/download?url={video_url}"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # API-dən gələn birbaşa video linkini götürürük
            direct_link = data.get('result', {}).get('video', {}).get('noWatermark') or data.get('result', {}).get('video', {}).get('url_list', [None])[0]
            
            if direct_link:
                return redirect(direct_link)
            else:
                return "Video linki tapılmadı. Zəhmət olmasa linkin düzgünlüyünü yoxlayın."
        else:
            return "Xidmət müvəqqəti olaraq cavab vermir, bir az sonra yenidən cəhd edin."
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
