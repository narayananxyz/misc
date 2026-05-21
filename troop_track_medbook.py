import requests
import pickle
import csv
import io

COOKIES_FILE = "troop_track_session.pkl"

try:
    with open(COOKIES_FILE, "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    print("No session found. Run troop_track_auth.py first.")
    exit(1)

TROOP = data["troop_base"]
session = requests.Session()
session.cookies.update(data["cookies"])

print("Fetching medical book...")
r = session.get(f"{TROOP}/manage/medical_book")
print(f"Status: {r.status_code}")

reader  = csv.DictReader(io.StringIO(r.text))
members = list(reader)

print(f"\nFound {len(members)} members\n")
print(f"{'Last Name':<20} {'First Name':<15} {'Part A':<12} {'Part B':<12} {'Part C':<12}")
print("-" * 71)
for m in members:
    print(f"{m['Last Name']:<20} {m['First Name']:<15} {m['Part A']:<12} {m['Part B']:<12} {m['Part C']:<12}")
