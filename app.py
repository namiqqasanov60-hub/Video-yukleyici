HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 10px; margin: 0; }
        .container { max-width: 100%; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        h2 { margin: 10px 0; color: #ff0050; }
        .sig { font-size: 12px; color: #777; margin-bottom: 20px; }
        input { padding: 15px; width: 90%; border-radius: 8px; border: none; margin-bottom: 15px; box-sizing: border-box; }
        button { padding: 15px; width: 90%; background: #ff0050; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        video { max-width: 100%; height: auto; margin-top: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>TikTok Yükləyici</h2>
        <div class="sig">by Avara Hasan</div>
        <form method="POST">
            <input type="text" name="url" placeholder="Link-i bura yapışdır..." required>
            <br><button type="submit">Tap və Yüklə</button>
        </form>
        {% if result %}
            <div class="result">
                <p>Video tapıldı!</p>
                <a href="{{ result }}" download="video.mp4" style="color: #00e5ff; font-weight: bold;">Faylı Yüklə</a>
                <br>
                <video controls>
                    <source src="{{ result }}" type="video/mp4">
                </video>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""
