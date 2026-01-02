# Local Coqui TTS server (no Docker)

This folder contains `tts_server.py` — a small Flask proxy that uses Coqui TTS to synthesize text into WAV audio and return it to the browser. It lets your `story.html` request higher-quality TTS without embedding keys.

Quick steps (Windows):

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (this will install PyTorch and Coqui TTS; it may take time):

```powershell
pip install -r requirements-coqui.txt
```

If PyTorch install fails or you want to customize (CPU vs GPU), follow PyTorch install instructions at https://pytorch.org and then `pip install TTS`.

3. Run the TTS server:

```powershell
python tts_server.py
```

By default the server listens on port `5002` and accepts GET `/tts?file=FILENAME` or `/tts?text=...` and returns `audio/wav`.

4. Serve the static site (if you already use `python -m http.server 8000`, keep it running). Open `index.html` via HTTP and click a story, then click "Play (Coqui)" to request audio from the local server.

Notes:
- Coqui TTS models can be large; initial download may take time and disk space.
- If you see model-related errors, install a compatible PyTorch for your platform first.
