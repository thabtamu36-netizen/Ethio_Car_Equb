Render Background Worker (Telegram bot)
=====================================

Create a Background Worker service in Render to run the Telegram bot as a long-running process.

Settings:

- Branch: `main`
- Root Directory: leave this blank (use the repository root)
- Runtime: `Python`
- Start Command: `python bot.py`

Environment variables required:

- `BOT_TOKEN`
- `ADMIN_ID`
- `DATABASE_URL`
- Any other vars from `config.py`

Notes:

- Background Workers are intended for long-running processes. Use Render's Instance Type according to desired uptime and cost.
- If your bot uses long polling it will run continuously; webhook-based bots can be hosted on the web service instead.
