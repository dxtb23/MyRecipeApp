from mailjet_rest import Client
import json

# Lade die Konfigurationsdaten aus der config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Konfigurationswerte
api_key = config['api_key']
api_secret = config['api_secret']
to_email = config['sendto']
from_email = config['username']

subject = "Dein Rezept"
email_body = "Hier ist dein zufällig ausgewähltes Rezept!"

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
