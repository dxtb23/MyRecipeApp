import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json

# Funktion zum Versenden der E-Mail
def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, username, password, attachment_path=None):
    # Erstelle die E-Mail-Nachricht
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Füge den E-Mail-Text hinzu
    msg.attach(MIMEText(body, 'plain'))

    # Füge ein Attachment hinzu, falls vorhanden
    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name='recipes.json')
            part['Content-Disposition'] = f'attachment; filename="recipes.json"'
            msg.attach(part)

    # Verbinde zum SMTP-Server und sende die E-Mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Verbindung verschlüsseln
        server.login(username, password)
        server.send_message(msg)

    print(f"Email erfolgreich an {to_email} gesendet.")

# Lade die Rezepte aus der JSON-Datei
with open('recipes.json', 'r') as f:
    recipes = json.load(f)

# Erstelle den E-Mail-Text
email_body = "Hier sind die Rezepte:\n\n"
for recipe in recipes:
    email_body += f"Title: {recipe['title']}\nLink: {recipe['link']}\n\n"

# E-Mail-Konfiguration
subject = 'Ihre gescrappten Rezepte'
to_email = 'trialbusiness@fn.de'
from_email = 'd_sein_mailgedoens@freenet.de'
smtp_server = 'mx.freenet.de'
smtp_port = 587  # Typischerweise 587 für TLS
username = 'deineemail@example.com'
password = 'deinpasswort'

# Versende die E-Mail
send_email(subject, email_body, to_email, from_email, smtp_server, smtp_port, username, password, attachment_path='recipes.json')
