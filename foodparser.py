import requests
from bs4 import BeautifulSoup
from model import Recipe
import json
import time



def scrape_recipe_data(url, recipe):
    response = requests.get(url)
    title = None
    ingredients = []
    instructions = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract recipe title
        title_element = soup.find('h1')
        title = title_element.text.strip() if title_element else "No title found"

        print(title)

        # Extract recipe URL
        print("URL:", url)

        # Extract ingredients with quantity
        ingredient_elements = soup.find_all('li', {'style': 'display: contents'})
        for ingredient_element in ingredient_elements:
            quantity_element = ingredient_element.find('span', {'class': 'ingredient-quantity'})
            text_element = ingredient_element.find('span', {'class': 'ingredient-text'})

            if quantity_element and text_element:
                quantity = quantity_element.text.strip()
                ingredient = text_element.text.strip()
                ingredients.append(f"{quantity} {ingredient}")

        ##print("\nIngredients:")
        ##for ingredient in ingredients:
            ##print(ingredient)

        # Extract instructions
        instructions = []
        instruction_elements = soup.find('ul', {'class': 'direction-list'}).find_all('li', {'class': 'direction'})
        for instruction_element in instruction_elements:
            instructions.append(instruction_element.text.strip())

        ##print("\nInstructions:")
        ##for step in instructions:
            ##print(step)

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
    recipe.title = title
    recipe.ingredients = json.dumps(ingredients, ensure_ascii=False)
    recipe.instructions = json.dumps(instructions, ensure_ascii=False)
    recipe.save()
    return title, ingredients, instructions





# Example usage
def parse_all_urls():
    for recipe in Recipe.select():
        title, ingredients, instructions = scrape_recipe_data(recipe.url)
        recipe.title = title
        recipe.ingredients = json.dumps(ingredients, ensure_ascii=False)
        recipe.instructions = json.dumps(instructions, ensure_ascii=False)
        recipe.save()

