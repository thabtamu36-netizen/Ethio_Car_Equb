Deploying this app to Render
===========================

Render settings (copy these into the Web Service form):

- Branch: `main`
- Root Directory: leave this blank (use the repository root)
- Runtime: `Python`
- Build Command: `pip install -r requirements.txt gunicorn`
- Start Command (recommended):
  `gunicorn -w 4 -k uvicorn.workers.UvicornWorker dashboard.app:app --bind 0.0.0.0:$PORT`
  
  Alternative (simpler):
  `uvicorn dashboard.app:app --host 0.0.0.0 --port $PORT`

Environment variables to add in Render (Render Dashboard → Environment):

- `DATABASE_URL` (use Render Managed Postgres or external DB; avoid SQLite on ephemeral filesystem)
- `BOT_TOKEN`
- `ADMIN_ID`
- `DASHBOARD_PASSWORD`
- `DASHBOARD_URL` (optional)
- `CBE_ACCOUNT_NAME`, `CBE_ACCOUNT_NUMBER`
- `TELEBIRR_ACCOUNT_NAME`, `TELEBIRR_PHONE`
- `EQUB_AMOUNT`

Database migrations / initialization

After first deploy, open Render Shell for the service and run:

```
python migrate_db.py
# or for a fresh DB
python init_db.py
```

Notes

- Render will auto-deploy on pushes to the selected branch. Use the Logs panel for troubleshooting.
- If you prefer to keep `gunicorn` in `requirements.txt` instead of the build command, add `gunicorn` to the file in this root.
- For the Telegram bot, create a separate Background Worker service (see `render-worker.md`).
