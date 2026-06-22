        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="{{ result }}" 
                   onclick="return confirm('Bu videonu yükləmək istəyirsən?');" 
                   download="tiktok_video.mp4" 
                   style="display:inline-block; padding:12px 25px; background:#00e5ff; color:#000; text-decoration:none; border-radius:8px; font-weight:bold;">
                   İndi Yüklə
                </a>
                <br>
                <video controls style="margin-top:20px; width:100%; max-width:400px;">
                    <source src="{{ result }}" type="video/mp4">
                </video>
            </div>
        {% endif %}
                </video>
            </div>
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
        except Exception:
            pass
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
