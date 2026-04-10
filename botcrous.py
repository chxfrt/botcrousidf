import requests
import time
import json
from bs4 import BeautifulSoup

TOKEN = os.getenv("8657413634:AAFmpdcJrXnhxWHjxwJvjSFoPoVj2bf_JjI")
CHAT_ID = os.getenv("8286941156")

URL = "https://trouverunlogement.lescrous.fr/tools/41/search?region=11"

SEEN_FILE = "seen.json"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def get_logements():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    logements = []
    cards = soup.find_all("div", class_="fr-card")

    for card in cards:
        link_tag = card.find("a")
        if not link_tag:
            continue

        link = "https://trouverunlogement.lescrous.fr" + link_tag["href"]
        title = card.get_text(strip=True)

        logements.append({
            "id": link,
            "title": title,
            "link": link
        })

    return logements

def main():
    seen = load_seen()

    send_telegram("✅ Bot CROUS lancé !")

    while True:
        try:
            logements = get_logements()

            for logement in logements:
                if logement["id"] not in seen:
                    message = f"🏠 Nouveau logement CROUS IDF\n\n{logement['title']}\n{logement['link']}"
                    send_telegram(message)
                    seen.add(logement["id"])

            save_seen(seen)

            time.sleep(120)

        except Exception as e:
            print("Erreur:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()