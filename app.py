from flask import Flask, render_template_string, request, redirect
import yt_dlp

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
    
    # TikTok blokunu keçmək üçün xüsusi aldadıcı ayarlar
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            return redirect(direct_link)
    except Exception as e:
        return f"Xəta baş verdi. Linki yoxlayın və ya bir az sonra yenidən cəhd edin. Detal: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
