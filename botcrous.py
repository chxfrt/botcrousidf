import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/42"

SEEN_FILE = "seen.txt"

def log(msg):
    print(f"[{datetime.now()}] {msg}")

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        for item in seen:
            f.write(item + "\n")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def check_crous():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "idTool": 42,
        "need_aggregation": True,
        "page": 1,
        "pageSize": 24,
        "location": [
            {"lon": 1.4462445, "lat": 49.241431},
            {"lon": 3.5592208, "lat": 48.1201456}
        ],
        "precision": 4,
        "price": {"max": 10000000},
        "area": {"min": 0},
        "adaptedPmr": False,
        "toolMechanism": "flow"
    }

    r = requests.post(API_URL, json=payload, headers=headers)

    if r.status_code != 200:
        log("Erreur API")
        return

    data = r.json()
    logements = data.get("results", {}).get("items", [])

    seen = load_seen()
    new_seen = set(seen)

    for logement in logements:
        logement_id = str(logement.get("id"))

        if logement_id in seen:
            continue

        message = "🏠 CROUS\n📍 Île-de-France"
        send_telegram(message)

        new_seen.add(logement_id)

    save_seen(new_seen)

    # 🔥 push automatique sur GitHub
    os.system("git config --global user.email 'bot@github.com'")
    os.system("git config --global user.name 'github-bot'")
    os.system("git add seen.txt")
    os.system("git commit -m 'update seen'")
    os.system("git push")

# 🚀 lancement
if TOKEN and CHAT_ID:
    check_crous()