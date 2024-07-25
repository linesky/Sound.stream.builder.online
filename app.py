
#pip install Flask
#pip install numpy

from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import wave
import os
import io

app = Flask(__name__)

# Diretório onde os arquivos .wav serão salvos
FILES_DIR = 'files'
os.makedirs(FILES_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            frequency = int(request.form['frequencia'])
            duration = int(request.form['segundos'])

            # Create the WAV file in memory
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
            audio_data = (audio_data * 32767).astype(np.int16)

            filename = f"{frequency}.wav"
            filepath = os.path.join(FILES_DIR, filename)

            # Save the WAV file to the file system
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())

            # Redirect to the stream page
            return redirect(url_for('stream', filename=filename))
        except Exception as e:
            return str(e), 400

    return render_template('index.html')

@app.route('/stream/<filename>')
def stream(filename):
    return render_template('stream.html', filename=filename)

@app.route('/files/<filename>')
def serve_file(filename):
    return send_file(os.path.join(FILES_DIR, filename), mimetype='audio/wav')



print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

