from flask import Flask, request, send_file, jsonify, abort
from flask_cors import CORS
import os
import tempfile
import json

try:
    from TTS.api import TTS
except Exception as e:
    TTS = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORIES_DIR = os.path.join(BASE_DIR, 'stories')
STORIES_INDEX = os.path.join(BASE_DIR, 'stories.json')

app = Flask(__name__)
CORS(app)

tts_model = None

def load_tts_model():
    global tts_model
    if tts_model is None:
        if TTS is None:
            raise RuntimeError('TTS package is not installed. Install with `pip install TTS`')
        # Choose a default Coqui model. Change as needed.
        tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    return tts_model

def allowed_filename(fname):
    # prevent path traversal and allow only filenames listed in stories.json (if present)
    if '/' in fname or '\\' in fname:
        return False
    if os.path.isabs(fname):
        return False
    if os.path.exists(STORIES_INDEX):
        try:
            with open(STORIES_INDEX, 'r', encoding='utf-8') as f:
                allowed = json.load(f)
            return fname in allowed
        except Exception:
            return False
    # fallback: ensure file exists in stories dir
    return os.path.exists(os.path.join(STORIES_DIR, fname))

@app.route('/tts')
def tts_endpoint():
    fname = request.args.get('file')
    text = request.args.get('text')
    if not fname and not text:
        return jsonify({'error':'provide file=<filename> or text=<text>'}), 400

    if fname:
        if not allowed_filename(fname):
            return jsonify({'error':'file not allowed'}), 403
        path = os.path.join(STORIES_DIR, fname)
        if not os.path.exists(path):
            return jsonify({'error':'file not found'}), 404
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

    try:
        model = load_tts_model()
    except RuntimeError as e:
        return jsonify({'error':str(e)}), 500

    # synth to temporary wav file
    fd, out_path = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    try:
        model.tts_to_file(text=text, file_path=out_path)
        return send_file(out_path, mimetype='audio/wav')
    finally:
        try:
            os.remove(out_path)
        except Exception:
            pass

@app.route('/voices')
def voices():
    try:
        model = load_tts_model()
    except RuntimeError as e:
        return jsonify({'error':str(e)}), 500
    # Coqui TTS does not expose system voices like browsers; return model info
    return jsonify({'model': getattr(model, 'model_name', str(model))})

if __name__ == '__main__':
    print('Starting Coqui TTS proxy server on http://0.0.0.0:5002')
    app.run(host='0.0.0.0', port=5002)
