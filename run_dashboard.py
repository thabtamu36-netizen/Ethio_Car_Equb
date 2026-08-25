"""
Start the Ethio Car Equb admin dashboard.
Run: python run_dashboard.py
"""

import uvicorn

from config import DASHBOARD_HOST, DASHBOARD_PORT, DASHBOARD_URL

if __name__ == "__main__":
    # Show the configured dashboard URL for operator visibility
    print(f"Admin dashboard URL: {DASHBOARD_URL}")

    uvicorn.run(
        "dashboard.app:app",
        host=DASHBOARD_HOST,
        port=DASHBOARD_PORT,
        reload=False,
    )
