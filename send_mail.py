from mailjet_rest import Client
import random
import json
import os
from datetime import datetime, timedelta
import base64

# Lade die Konfigurationsdaten aus der config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Konfigurationswerte
api_key = config['api_key']
api_secret = config['api_secret']
to_email = config['sendto']
from_email = config['username']

# Lade die Rezepte
with open('recipes.json', 'r') as f:
    recipes = json.load(f)

# Funktion zur Auswahl von zwei zufälligen Rezepten
def get_random_recipes(recipes, num=2):
    return random.sample(recipes, min(num, len(recipes)))

# Funktion zum Erstellen einer ICS-Datei
def create_ics_file(recipe):
    event_name = f"Zutaten für {recipe['title']}"
    event_date = (datetime.now() + timedelta(days=1)).strftime('%Y%m%dT090000')  # Für den nächsten Tag um 09:00 Uhr
    event_end_date = (datetime.now() + timedelta(days=1, hours=1)).strftime('%Y%m%dT100000')  # 1 Stunde später

    # Zutaten in einen String umwandeln und umbrechen
    ingredients_list = wrap_text("\r\n".join(recipe['ingredients']))
    # Erstelle den ICS-Inhalt
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Company//NONSGML v1.0//EN
BEGIN:VEVENT
UID:{recipe['title']}@yourdomain.com
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{event_date}
DTEND:{event_end_date}
SUMMARY:{event_name}
DESCRIPTION:{ingredients_list}
END:VEVENT
END:VCALENDAR"""

    ics_filename = f"Rezepteinkauf_{recipe['title']}.ics"
    # Schreibe die ICS-Datei
    with open(ics_filename, 'w') as ics_file:
        ics_file.write(ics_content)

    return ics_filename

# wrapfukntion zum zeilenumbrechen für die ics, da nicht alle zeichenanzahl akzeptiert wird
def wrap_text(text, max_length=72):
    """Wrap text to the specified maximum line length without breaking words."""
    words = text.split()
    wrapped_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_length:
            wrapped_lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word

    if current_line:
        wrapped_lines.append(current_line)

    return '\r\n'.join(wrapped_lines)
# Wähle zwei zufällige Rezepte aus
random_recipes = get_random_recipes(recipes)

# Betreff dynamisch mit den Rezeptnamen
subject = f"Rezepte: {random_recipes[0]['title']} & {random_recipes[1]['title']}"

# HTML-Datei lesen und Platzhalter ersetzen
with open('email_template.html', 'r') as f:
    email_body = f.read()

# Ersetze die Platzhalter im HTML mit den Rezeptdaten
email_body = email_body.replace('{{ recipe_1_title }}', random_recipes[0]['title'])
email_body = email_body.replace('{{ recipe_1_link }}', random_recipes[0]['link'])
email_body = email_body.replace('{{ recipe_2_title }}', random_recipes[1]['title'])
email_body = email_body.replace('{{ recipe_2_link }}', random_recipes[1]['link'])
email_body = email_body.replace('{{ recipe_1_image }}', random_recipes[0]['image_url'])  # Bild für Rezept 1
email_body = email_body.replace('{{ recipe_2_image }}', random_recipes[1]['image_url'])  # Bild für Rezept 2

# Funktion zur Konvertierung der ICS-Datei in Base64
def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return base64.b64encode(file_content).decode('utf-8')

# E-Mail senden mit ICS-Anhängen
def send_email(subject, body, to_email, from_email):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Erstelle ICS-Datei für das erste Rezept und konvertiere sie in Base64
    ics_filename = create_ics_file(random_recipes[0])
    base64_content = encode_file_to_base64(ics_filename)

    attachments = [{
        'ContentType': 'application/ics',
        'Filename': f'Rezepteinkauf_{random_recipes[0]["title"]}.ics',
        'Base64Content': base64_content
    }]

    # Daten für die Mailjet API
    data = {
        'Messages': [
            {
                'From': {'Email': from_email},
                'To': [{'Email': to_email}],
                'Subject': subject,
                'HTMLPart': body,
                'Attachments': attachments
            }
        ]
    }
    
    result = mailjet.send.create(data=data)
    
    if result.status_code == 200:
        print("E-Mail erfolgreich gesendet.")
    else:
        print(f"Fehler beim Senden der E-Mail: {result.text}")

# E-Mail senden
send_email(subject, email_body, to_email, from_email)

# Entferne die temporäre ICS-Datei nach dem Senden
os.remove(f"Rezepteinkauf_{random_recipes[0]['title']}.ics")
