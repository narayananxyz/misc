import requests
import csv
import io
from bs4 import BeautifulSoup

BASE  = "https://trooptrack.com"
TROOP = "https://t222.trooptrack.com"

username = input("Username: ")
password = input("Password: ")

print(f"\nLogging in as '{username}'...")

session = requests.Session()

# ── Step 1: Get CSRF token ────────────────────────────────────────────────────
r = session.get(f"{BASE}/user_account_session/new")
soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("meta", {"name": "csrf-token"})["content"]
print(f"Got CSRF token: {csrf[:20]}...")

# ── Step 2: Login ─────────────────────────────────────────────────────────────
r = session.post(f"{BASE}/user_account_session", data={
    "_method":                           "put",
    "authenticity_token":                csrf,
    "user_account_session[login]":       username,
    "user_account_session[password]":    password,
    "user_account_session[remember_me]": "0",
    "commit":                            "Log In"
}, allow_redirects=True)

if "sign_in" in r.url or "session/new" in r.url:
    print("LOGIN FAILED — bad username or password")
    exit(1)

print(f"LOGIN OK — landed on: {r.url}")

# ── Step 3: Fetch medical book (returns CSV) ──────────────────────────────────
print("\nFetching medical book...")
r = session.get(f"{TROOP}/manage/medical_book")
print(f"Medical book status: {r.status_code}")

# Parse CSV response
reader = csv.DictReader(io.StringIO(r.text))
members = list(reader)

print(f"\nFound {len(members)} members\n")
print(f"{'Last Name':<20} {'First Name':<15} {'Part A':<12} {'Part B':<12} {'Part C':<12}")
print("-" * 71)
for m in members:
    print(f"{m['Last Name']:<20} {m['First Name']:<15} {m['Part A']:<12} {m['Part B']:<12} {m['Part C']:<12}")