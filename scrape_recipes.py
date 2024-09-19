from mailjet_rest import Client
import random
import json

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

def send_email(subject, body, to_email, from_email):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    data = {
        'Messages': [
            {
                'From': {'Email': from_email},
                'To': [{'Email': to_email}],
                'Subject': subject,
                'HTMLPart': body
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
