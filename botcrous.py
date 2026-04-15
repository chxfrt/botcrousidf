import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search"

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

    params = {
        "bounds": "48.1207_1.4472_49.2415_3.5592",
        "page": 1,
        "pageSize": 20
    }

    r = requests.get(API_URL, params=params)
    log(f"HTTP: {r.status_code}")

    data = r.json()
    logements = data.get("results", [])

    log(f"{len(logements)} logements trouvés")

    if not logements:
        log("⚠️ Aucun logement trouvé")
        return

    for logement in logements[:3]:
        titre = logement.get("title", "Sans titre")
        ville = logement.get("city", "Ville inconnue")

        log(f"ENVOI: {titre}")
        send_telegram(f"🏠 {titre}\n📍 {ville}")

# 🚀 Lancement
log("🚀 BOT LANCÉ")

if TOKEN and CHAT_ID:
    send_telegram("✅ Bot CROUS actif (API)")
    check_crous()
else:
    log("❌ TOKEN ou CHAT_ID manquant")