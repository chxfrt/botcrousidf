import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/42"

def log(msg):
    print(f"[{datetime.now()}] {msg}")

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

        for logement in logements[:3]:
            titre = logement.get("title", "Crous")
            ville = logement.get("city", "Ile-de-france")

            message = f"🏠 {titre}\n📍 {ville}"
            log(f"ENVOI: {titre}")
            send_telegram(message)

    except Exception as e:
        log(f"❌ ERREUR: {e}")

# 🚀 Lancement
log("🚀 BOT LANCÉ")

if TOKEN and CHAT_ID:
    send_telegram("✅ Bot CROUS actif")
    check_crous()
else:
    log("❌ TOKEN ou CHAT_ID manquant")