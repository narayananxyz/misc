import os
import requests
import pickle
from bs4 import BeautifulSoup

BASE         = "https://trooptrack.com"
COOKIES_FILE = "troop_track_session.pkl"

username = os.environ.get("TROOPTRACK_USERNAME") or input("Username: ")
password = os.environ.get("TROOPTRACK_PASSWORD") or input("Password: ")

print(f"\nLogging in as '{username}'...")

session = requests.Session()

r    = session.get(f"{BASE}/user_account_session/new")
soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("meta", {"name": "csrf-token"})["content"]
print(f"Got CSRF token: {csrf[:20]}...")

r = session.post(f"{BASE}/user_account_session", data={
    "_method":                           "put",
    "authenticity_token":                csrf,
    "user_account_session[login]":       username,
    "user_account_session[password]":    password,
    "user_account_session[remember_me]": "0",
    "commit":                            "Log In"
}, allow_redirects=True)

resp_soup = BeautifulSoup(r.text, "html.parser")

# Login form still present → credentials were rejected
if resp_soup.find("input", {"name": "user_account_session[login]"}):
    error_el = resp_soup.find(class_=lambda c: c and any(x in c for x in ["error", "alert", "flash"]))
    reason = error_el.get_text(strip=True) if error_el else "bad username or password"
    print(f"LOGIN FAILED — {reason}")
    exit(1)

# Fallback: URL-based check for redirect back to login
if "sign_in" in r.url or "session/new" in r.url:
    print("LOGIN FAILED — redirected back to login page")
    exit(1)

print(f"LOGIN OK — landed on: {r.url}")

from urllib.parse import urlparse
parsed   = urlparse(r.url)
troop_base = f"{parsed.scheme}://{parsed.netloc}"

with open(COOKIES_FILE, "wb") as f:
    pickle.dump({"cookies": session.cookies, "troop_base": troop_base}, f)

print(f"Troop base URL: {troop_base}")
print(f"Session saved to '{COOKIES_FILE}' — run other scripts now.")
