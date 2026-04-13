import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = os.getenv("8657413634:AAFmpdcJrXnhxWHjxwJvjSFoPoVj2bf_JjI")
CHAT_ID = os.getenv("8286941156")

URL = "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=48.1207_1.4472_49.2415_3.5592"

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
    except Exception as e:
        log(f"ERREUR TELEGRAM: {e}")

def check_crous():
    log("------ NOUVEAU SCAN ------")

    response = requests.get(URL)
    log(f"STATUS HTTP: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    logements = soup.find_all("article")
    log(f"{len(logements)} logements trouvés")

    if not logements:
        log("⚠️ Aucun logement trouvé → problème scraping probable")
        return

    # DEBUG : voir un exemple brut
    log(f"EXEMPLE: {logements[0].get_text(strip=True)[:200]}")

    for logement in logements[:3]:
        titre = logement.get_text(strip=True)[:100]
        log(f"ENVOI: {titre}")
        send_telegram(f"🏠 Nouveau logement CROUS IDF:\n{titre}")

# TEST
send_telegram("✅ Bot CROUS actif (test)")
check_crous()