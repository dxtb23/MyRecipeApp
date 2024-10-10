# Rezept-Scraping-Skript

## Beschreibung

Dieses Python-Skript scrapt Rezepte von der Website Minimalist Baker und speichert die gesammelten Rezepte in einer JSON-Datei. Das Skript kann eine bestimmte Anzahl von Seiten durchgehen und von jeder Seite die Rezepte extrahieren. Die gescrappten Rezepte werden in der Datei `recipes.json` gespeichert.
Anschließend werden random 2 Rezepte aus dem Catalog in der `send_mail.py` gepickt. Die Rezepteliste werden in 2 .ics-Dateien angehangen, die am nächsten Tag um 09.00 Uhr ringen. 
Die Zugänge zu den Rezeptelisten werden in der Mail angezeigt. Hierfür gibts dann auch die `email_template.html` Datei. Diese definiert das Layout.
Die `app.py` ist eine Flask-app auf der ursprünglich mal die Idee war eine Website zu bauen, in der sich User für den Mailverteiler anmelden können. 2-Faktor-Authent. ist noch nicht integriert. Daten werden in eine einfach per SQL-Query zu befragende `subscribers.db` geschrieben. Der Code ist funktional. 
Was noch fehlt: die Infos der Subcriber an die `send_mail.py` übergeben, um die Mails zu versenden. 
 
## Funktionen:

- **Scraping von Rezepten**: Holt Rezepte von den angegebenen Seiten der Minimalist Baker-Website.
- **Speichern von Rezepten**: Speichert die gesammelten Rezepte in einer `recipes.json`-Datei.
- **Versenden der Rezepte**: Versendet 2 Random Rezepte aus der `recipes.json`-Datei als ics-Kalenderdateien.
- **Web-App/Website für das Subscriben**: Subscriben auf den Newsletter darf natürlich nicht fehlen. Das übernimmt die `app.py`.


## Anforderungen

- Python 3.x
- BeautifulSoup4
- Requests

## Installation