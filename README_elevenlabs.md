# ElevenLabs client-only integration

This project includes a client-side integration for ElevenLabs TTS in `story.html`.

How it works
- You paste your ElevenLabs API key into the input on the story viewer page. The key is kept only in your browser memory (not sent to this repo or any server).
- Click `Fetch Voices` to retrieve available voices for your account (requires your key).
- Select a voice and click `Play (ElevenLabs)` to synthesize the current story and play it in the browser.

Security and limits
- Embedding an API key in client-side code is not safe for public sites. This approach assumes you are running the site locally or understand the exposure: anyone who has the key in the page can use it.
- For production, prefer a small server proxy that holds the key and issues short-lived tokens or proxies requests.
- ElevenLabs usage may incur charges; check your account limits and billing.

Troubleshooting
- If `Fetch Voices` fails: ensure your API key is valid and you have network access to `api.elevenlabs.io`.
- If audio fails to play: check browser console for CORS errors. ElevenLabs generally allows direct browser calls, but if your environment blocks cross-origin requests, use a server proxy.
