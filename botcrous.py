import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.getenv("8657413634:AAFmpdcJrXnhxWHjxwJvjSFoPoVj2bf_JjI")
CHAT_ID = os.getenv("8286941156")

# URL CROUS Île-de-France
URL = "https://trouverunlogement.lescrous.fr/tools/37/search?bounds=48.1207_1.4472_49.2415_3.5592"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def check_crous():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    logements = soup.find_all("article")

    if not logements:
        print("Aucun logement trouvé")
        return

    for logement in logements[:3]:  # limite pour éviter spam
        titre = logement.get_text(strip=True)[:100]
        send_telegram(f"🏠 Nouveau logement CROUS IDF:\n{titre}")

# 🔥 IMPORTANT : UNE SEULE EXÉCUTION
send_telegram("✅ Bot CROUS actif (GitHub Actions)")
check_crous()
#update