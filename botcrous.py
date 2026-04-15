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
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })
    log(f"TELEGRAM: {r.status_code}")

def check_crous():
    log("------ SCAN API CROUS ------")

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://trouverunlogement.lescrous.fr",
        "Referer": "https://trouverunlogement.lescrous.fr/"
    }

    payload = {
        "idTool": 42,
        "need_aggregation": True,
        "page": 1,
        "pageSize": 24,
        "sector": None,
        "occupationModes": [],
        "location": [
            {"lon": 1.4462445, "lat": 49.241431},
            {"lon": 3.5592208, "lat": 48.1201456}
        ],
        "residence": None,
        "precision": 4,
        "equipment": [],
        "price": {"max": 10000000},
        "area": {"min": 0},
        "adaptedPmr": False,
        "toolMechanism": "flow"
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        log(f"HTTP: {r.status_code}")

        if r.status_code != 200:
            log("❌ Erreur API")
            log(r.text[:300])
            return

        data = r.json()
        logements = data.get("results", {}).get("items", [])

        log(f"{len(logements)} logements trouvés")

        if not logements:
            log("⚠️ Aucun logement trouvé")
            return

        seen = load_seen()
        new_seen = set(seen)

        for logement in logements:
            logement_id = str(logement.get("id"))

            # 👉 skip si déjà vu
            if logement_id in seen:
                continue

            titre = logement.get("title") or "CROUS"
            ville = logement.get("city") or "Île-de-France"

            message = f"🏠 {titre}\n📍 {ville}"
            log(f"NOUVEAU: {logement_id}")
            send_telegram(message)

            new_seen.add(logement_id)

        save_seen(new_seen)

    except Exception as e:
        log(f"❌ ERREUR: {e}")

# 🚀 Lancement
log("🚀 BOT LANCÉ")

if TOKEN and CHAT_ID:
    check_crous()
else:
    log("❌ TOKEN ou CHAT_ID manquant")