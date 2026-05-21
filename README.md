# TroopTrack Scripts

Utilities for fetching data from TroopTrack.

## Setup

```
pip install requests beautifulsoup4
```

## Authentication

Run this once before any other script. It logs in and saves your session cookies to `troop_track_session.pkl`.

```
python troop_track_auth.py
```

**Credentials via environment variables (recommended):**

Set these before running so you are not prompted each time:

```
# Windows (PowerShell)
$env:TROOPTRACK_USERNAME = "your_username"
$env:TROOPTRACK_PASSWORD = "your_password"

# Windows (cmd)
set TROOPTRACK_USERNAME=your_username
set TROOPTRACK_PASSWORD=your_password

# macOS / Linux
export TROOPTRACK_USERNAME=your_username
export TROOPTRACK_PASSWORD=your_password
```

If the variables are not set, the script falls back to prompting interactively.

Sessions expire after some time — re-run `troop_track_auth.py` if other scripts start returning errors.

## Scripts

| Script | Description |
|---|---|
| `troop_track_auth.py` | Authenticate and save session |
| `troop_track_medbook.py` | Fetch and display the medical book |

## Writing new scripts

Load the saved session with:

```python
import pickle, requests

with open("troop_track_session.pkl", "rb") as f:
    cookies = pickle.load(f)

session = requests.Session()
session.cookies.update(cookies)
```

Then use `session.get(...)` / `session.post(...)` as normal.
