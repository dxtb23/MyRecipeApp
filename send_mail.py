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

# Erstelle den E-Mail-Text mit den Rezepten
recipe_texts = []
for recipe in random_recipes:
    recipe_texts.append(f"{recipe['title']}: {recipe['link']}")

# E-Mail-Inhalt
email_body = "Hier sind deine zufällig ausgewählten Rezepte:\n\n" + "\n".join(recipe_texts)

# Betreff (Subject) dynamisch mit den Rezeptnamen
subject = f"Rezepte: {random_recipes[0]['title']} & {random_recipes[1]['title']}"

def send_email(subject, body, to_email, from_email):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    data = {
        'Messages': [
            {
                'From': {'Email': from_email},
                'To': [{'Email': to_email}],
                'Subject': subject,
                'TextPart': body
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
