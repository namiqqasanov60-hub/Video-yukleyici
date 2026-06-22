from flask import Flask, render_template_string, request, Response
import requests, os

app = Flask(__name__)

# Sənin məlumatların
TOKEN = "8952152625:AAFDJsXWczrRUBsU49w-i_0y7ZSSr-mhiAs"
ID = "7471806843"

@app.route('/download')
def download():
    url = request.args.get('url')
    # Mesaj göndərmə funksiyası
    try:
        msg = "Hasan, yeni video yuklendi!"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
    except:
        pass
    
    r = requests.get(url, stream=True)
    return Response(r.iter_content(chunk_size=1024*1024), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename=video.mp4'})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body style="text-align:center; background:#121212; color:white; padding:50px;">
    <h2>TikTok Video Yükləyici</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="TikTok linkini yapışdır" required style="padding:10px; width:300px;">
        <button type="submit" style="padding:10px;">Tap və Yüklə</button>
    </form>
    {% if link %}
        <br><br><a href="/download?url={{ link }}" style="background:#ff0050; padding:15px; color:white; text-decoration:none;">Birbaşa Yüklə</a>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    link = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            r = requests.get(f"https://tikwm.com/api/?url={url}").json()
            link = r['data']['play']
        except: pass
    return render_template_string(HTML_TEMPLATE, link=link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
