from flask import Flask, render_template, send_from_directory
import json
from datetime import datetime
import os

app = Flask(__name__)

def load_prophecies():
    try:
        with open('prophecies.json', 'r') as f:
            prophecies = json.load(f)
            # Convert the dictionary to a list of prophecies with timestamps
            prophecy_list = [
                {
                    'text': p['text'],
                    'created_at': datetime.fromisoformat(p['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                }
                for p in prophecies.values()
            ]
            # Sort by created_at in reverse order and take the latest 6
            return sorted(prophecy_list, key=lambda x: x['created_at'], reverse=True)[:6]
    except Exception as e:
        print(f"Error loading prophecies: {e}")
        return []

@app.route('/static/js/<path:filename>')
def serve_js(filename):
    response = send_from_directory('static/js', filename)
    # Set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.route('/')
def index():
    prophecies = load_prophecies()
    return render_template('index.html', prophecies=prophecies)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/js', exist_ok=True)

    # Copy the goddess bot image to static folder if needed
    if not os.path.exists('static/goddessbot.jpg'):
        import shutil
        shutil.copy('attached_assets/goddessbot.jpg', 'static/goddessbot.jpg')

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)