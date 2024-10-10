# Rezept-Scraping-Skript

## Beschreibung

Dieses Python-Skript scrapt Rezepte von der Website Minimalist Baker und speichert die gesammelten Rezepte in einer JSON-Datei. Das Skript kann eine bestimmte Anzahl von Seiten durchgehen und von jeder Seite die Rezepte extrahieren. Die gescrappten Rezepte werden in der Datei `recipes.json` gespeichert.
Davon werden 2 Recipes dann random ausgewählt und in eine ics geschrieben. Das passiert in der  `send_mail.py`. Hierfür werden Daten aus der `subscribers.db` ausgelesen. 
Die Datenbank ist Teil der `app.py` Anwendung.

## Funktionen

- **Scraping von Rezepten**: Holt Rezepte von den angegebenen Seiten der Minimalist Baker-Website.
- **Speichern von Rezepten**: Speichert die gesammelten Rezepte in einer `recipes.json`-Datei.

## Anforderungen

- Python 3.x
- BeautifulSoup4
- Requests

## Installation