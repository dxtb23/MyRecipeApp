from mailjet_rest import Client
import random
import json
import os
from datetime import datetime, timedelta
import base64
from icalendar import Calendar, Event

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

# Funktion zum Erstellen einer ICS-Datei mit dem icalendar Package
def create_ics_file(recipe):
    event_name = f"Zutaten für {recipe['title']}"
    event_date = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    event_end_date = event_date + timedelta(hours=1)  # Endet 1 Stunde später um 10:00 Uhr

    
    # Erstelle ein iCalendar-Event
    cal = Calendar()
    event = Event()
    
    event.add('uid', recipe['title'])
    event.add('summary', event_name)
    event.add('dtstart', event_date)
    event.add('dtend', event_end_date)
    
    #Zutatenliste in die Description als einfacher Text einfügen
    ingredients = "\n".join([f"- {ingredient}" for ingredient in recipe['ingredients']])
    event.add('description', f"Zutaten für das Rezept:\n{ingredients}")

    
    cal.add_component(event)
    
    # Speichere die ICS-Datei
    ics_filename = f"Rezepteinkauf_{recipe['title']}.ics"
    with open(ics_filename, 'wb') as ics_file:
        ics_file.write(cal.to_ical())
    
    return ics_filename

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

# Zutatenliste als HTML-Liste für das erste Rezept erstellen
ingredients_1 = "<ul>\n" + "\n".join([f"<li>{ingredient}</li>" for ingredient in random_recipes[0]['ingredients']]) + "\n</ul>"
# Zutatenliste als HTML-Liste für das zweite Rezept erstellen
ingredients_2 = "<ul>\n" + "\n".join([f"<li>{ingredient}</li>" for ingredient in random_recipes[1]['ingredients']]) + "\n</ul>"

# Füge die Zutatenlisten in das HTML-Template ein
email_body = email_body.replace('{{ recipe_1_ingredients }}', ingredients_1)
email_body = email_body.replace('{{ recipe_2_ingredients }}', ingredients_2)

# Funktion zur Konvertierung der ICS-Datei in Base64
def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return base64.b64encode(file_content).decode('utf-8')

# E-Mail senden mit ICS-Anhängen
def send_email(subject, body, to_email, from_email):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    attachments = []
    
    # Erstelle ICS-Dateien für beide Rezepte und konvertiere sie in Base64
    for recipe in random_recipes:
        ics_filename = create_ics_file(recipe)
        base64_content = encode_file_to_base64(ics_filename)
        attachments.append({
            'ContentType': 'application/ics',
            'Filename': f'Rezepteinkauf_{recipe["title"]}.ics',
            'Base64Content': base64_content  # Hier den Base64-Inhalt hinzufügen
            
        })

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

# Entferne die temporären ICS-Dateien nach dem Senden
for recipe in random_recipes:
    os.remove(f"Rezepteinkauf_{recipe['title']}.ics")
