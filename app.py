HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <!-- Telefon üçün vacib olan bu meta etiketini əlavə etdim -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; margin: 0; padding: 20px; }
        .container { max-width: 95%; margin: 20px auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        input { padding: 15px; width: 90%; border-radius: 8px; border: none; margin-bottom: 15px; box-sizing: border-box; }
        button { padding: 15px 30px; background: #ff0050; color: white; border: none; border-radius: 8px; cursor: pointer; width: 90%; }
        video { max-width: 100%; height: auto; margin-top: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>TikTok Yükləyici</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <br><button type="submit">Tap və Yüklə</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="{{ result }}" download="video.mp4" style="color: #00e5ff; display: block; margin: 10px;">Faylı Yüklə</a>
                <video controls>
                    <source src="{{ result }}" type="video/mp4">
                </video>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
