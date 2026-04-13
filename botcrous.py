import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 🔐 Mets ton TOKEN et CHAT_ID dans GitHub (Settings > Secrets)
TOKEN = os.getenv("8657413634:AAFmpdcJrXnhxWHjxwJvjSFoPoVj2bf_JjI")
CHAT_ID = os.getenv("8286941156")

# ✅ URL corrigée
URL = "https://trouverunlogement.lescrous.fr/classic/residence"

def log(msg):
    print(f"[{datetime.now()}] {msg}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=data)
        log(f"TELEGRAM STATUS: {r.status_code}")
        log(f"TELEGRAM RESPONSE: {r.text}")
    except Exception as e:
        log(f"ERREUR TELEGRAM: {e}")

def check_crous():
    log("------ NOUVEAU SCAN ------")

    try:
        response = requests.get(URL)
        log(f"STATUS HTTP: {response.status_code}")
    except Exception as e:
        log(f"ERREUR REQUEST: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    logements = soup.find_all("article")
    log(f"{len(logements)} logements trouvés")

    if not logements:
        log("⚠️ Aucun logement trouvé → site probablement en JavaScript")
        send_telegram("⚠️ Bot: aucun logement détecté (site dynamique)")
        return

    # DEBUG
    log(f"EXEMPLE: {logements[0].get_text(strip=True)[:200]}")

    for logement in logements[:3]:
        titre = logement.get_text(strip=True)[:100]
        log(f"ENVOI: {titre}")
        send_telegram(f"🏠 Nouveau logement CROUS:\n{titre}")

# 🚀 Lancement
log("🚀 SCRIPT LANCÉ")

if not TOKEN or not CHAT_ID:
    log("❌ TOKEN ou CHAT_ID manquant")
else:
    send_telegram("✅ Bot CROUS actif")
    check_crous()