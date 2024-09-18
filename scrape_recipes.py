from bs4 import BeautifulSoup
import requests
import json
import random

# Funktion zum Scrapen von Rezepten von einer einzelnen Seite
def scrape_recipes_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_containers = soup.find_all('article', class_='post-summary primary')

    recipes = []
    for container in recipe_containers:
        title_tag = container.find('h2', class_='post-summary__title').find('a')
        link_tag = container.find('a', class_='post-summary__image')
        
        title = title_tag.text if title_tag else 'Kein Titel gefunden'
        link = link_tag['href'] if link_tag else 'Kein Link gefunden'
        
        recipes.append({
            'title': title,
            'link': link
        })

    return recipes

# Funktion zum Sammeln der Rezepte von nur zwei Seiten
def scrape_limited_recipes(base_url, num_pages):
    all_recipes = []
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_number}/"
        print(f"Scraping {url}")
        recipes = scrape_recipes_from_page(url)
        
        if not recipes:
            break
        
        all_recipes.extend(recipes)
    
    return all_recipes

# Basis-URL der Rezeptseite
base_url = 'https://minimalistbaker.com/category/recipes/vegan'

# Anzahl der Seiten, die gescrappt werden sollen
num_pages_to_scrape = 2

# Scrape die Rezepte von den ersten zwei Seiten
limited_recipes = scrape_limited_recipes(base_url, num_pages_to_scrape)

# Speichere die gescrappten Rezepte in einer JSON-Datei
with open('recipes.json', 'w') as f:
    json.dump(limited_recipes, f, indent=4)

print(f"Erfolgreich {len(limited_recipes)} Rezepte gescrappt und in 'recipes.json' gespeichert.")

# Randomizer 2 Rezepte auswählen
def get_random_recipes(recipes, num=2):
    return random.sample(recipes, min(num, len(recipes)))

# Wähle zwei zufällige Rezepte aus
random_recipes = get_random_recipes(limited_recipes)