import os
from pathlib import Path
from urllib.parse import unquote

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)


def resolve_database_url(database_url: str) -> str:
    if not database_url.startswith("sqlite:///"):
        return database_url

    raw_path = unquote(database_url.replace("sqlite:///", "", 1))
    db_path = Path(raw_path)

    if db_path.is_absolute():
        return database_url

    for base_path in [BASE_DIR, *BASE_DIR.parents]:
        candidate = base_path / db_path
        if candidate.exists():
            return f"sqlite:///{candidate.as_posix()}"

    return f"sqlite:///{(BASE_DIR / db_path).as_posix()}"


BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
if not BOT_TOKEN:
    raise RuntimeError("Missing BOT_TOKEN in .env file")

_admin_id_value = (os.getenv("ADMIN_ID") or "").strip()
if not _admin_id_value:
    raise RuntimeError("Missing ADMIN_ID in .env file")

try:
    ADMIN_ID = int(_admin_id_value)
except ValueError as exc:
    raise RuntimeError(
        "ADMIN_ID must be a valid Telegram numeric user ID in .env file"
    ) from exc

if ADMIN_ID <= 0:
    raise RuntimeError("ADMIN_ID must be a positive Telegram user ID")

DATABASE_URL = resolve_database_url(
    os.getenv(
        "DATABASE_URL",
        "sqlite:///ethio_car_equb.db"
    )
)

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "127.0.0.1")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8000"))
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "")
# New: full URL for dashboard links (optional). If not provided, constructed from host/port.
_env_dashboard_url = os.getenv("DASHBOARD_URL", "")
if _env_dashboard_url:
    DASHBOARD_URL = _env_dashboard_url
else:
    _scheme = "https" if DASHBOARD_PORT == 443 else "http"
    _port_part = "" if DASHBOARD_PORT in (80, 443) else f":{DASHBOARD_PORT}"
    DASHBOARD_URL = f"{_scheme}://{DASHBOARD_HOST}{_port_part}"
CBE_ACCOUNT_NAME = os.getenv("CBE_ACCOUNT_NAME")
CBE_ACCOUNT_NUMBER = os.getenv("CBE_ACCOUNT_NUMBER")

TELEBIRR_ACCOUNT_NAME = os.getenv("TELEBIRR_ACCOUNT_NAME")
TELEBIRR_PHONE = os.getenv("TELEBIRR_PHONE")
EQUB_AMOUNT = os.getenv(
    "EQUB_AMOUNT"
)
