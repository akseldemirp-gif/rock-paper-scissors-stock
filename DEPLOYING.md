# Deploying to Render

Use [New Blueprint](https://dashboard.render.com/blueprints/new) and connect this repository on the `main` branch. Render reads `render.yaml` and provisions a free web service with a generated Flask secret.

For manual setup, select **New → Web Service** in [Render](https://dashboard.render.com/), connect this repository, and use these settings.

| Setting | Value |
| --- | --- |
| Branch | `main` |
| Runtime | Python |
| Instance | Free |
| Build command | `python -m pip install -r requirements.txt` |
| Start command | `gunicorn --bind 0.0.0.0:$PORT 'web_app:create_app()'` |

For manual setup, add `SECRET_KEY` in Render's Environment settings. Generate a random value locally with `python -c 'import secrets; print(secrets.token_hex(32))'`. To enable current stock lookups, add `ALPHAVANTAGE_API_KEY` in the same settings. Keep both values out of Git.

After the deploy succeeds, open the service URL. Play a round of Rock Paper Scissors, look up AAPL, and confirm an invalid ticker returns you to the lookup form with a message.

[Render's Flask deployment guide](https://render.com/docs/deploy-flask)
