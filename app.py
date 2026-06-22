from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def get_video():
    url = request.json.get('url')
    # SSL xətası verməyən stabil API
    api_url = f"https://tikwm.com/api/?url={url}"
    try:
        data = requests.get(api_url).json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
