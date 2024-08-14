from flask import Flask, jsonify, send_from_directory, request
from gtts import gTTS
import os
import subprocess
import sys

app = Flask(__name__, static_folder='D:/Hackathon/level 7/frontend')
audio_folder = 'frontend/audio'

if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

# Serve static files (HTML, CSS, JS)
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Start inspection route
@app.route('/start-inspection', methods=['GET'])
def start_inspection():
    try:
        # Replace with your actual inspection function
        results = ["Inspection started..."]  # Placeholder for actual results
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Restart application route
@app.route('/restart-app', methods=['GET'])
def restart_app():
    subprocess.Popen([sys.executable, sys.argv[0]])
    return jsonify({'status': 'Restarting application...'})

# Exit application route
@app.route('/exit-app', methods=['GET'])
def exit_app():
    sys.exit()
    return jsonify({'status': 'Exiting application...'})

# Text-to-speech route
@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '')
    if text:
        tts = gTTS(text)
        audio_file = os.path.join(audio_folder, 'output.mp3')
        tts.save(audio_file)
        return jsonify({'audio_url': '/audio/output.mp3'})
    return jsonify({'error': 'No text provided'}), 400

# Serve audio files
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(audio_folder, filename)

if __name__ == '__main__':
    app.run(port=5000)
