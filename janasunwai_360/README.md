# Janasunwai Flask app

Quick local setup:

1. Copy `.env.example` to `.env` and fill your Supabase credentials.
2. Create and activate a Python virtualenv.
3. Install deps:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python -m app.app
```

Notes:
- Supabase credentials are required — the app will not run correctly without `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` set in the environment.
- Uploaded images are staged to `app/static/uploads` briefly and then uploaded to the configured Supabase storage bucket.