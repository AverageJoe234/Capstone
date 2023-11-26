import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests

def scrape_recipe_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract recipe title
        title_element = soup.find('h1')
        title = title_element.text.strip() if title_element else "No title found"

        # Extract ingredients with quantity
        ingredients = []
        ingredient_elements = soup.find_all('li', {'style': 'display: contents'})
        for ingredient_element in ingredient_elements:
            quantity_element = ingredient_element.find('span', {'class': 'ingredient-quantity'})
            text_element = ingredient_element.find('span', {'class': 'ingredient-text'})

            if quantity_element and text_element:
                quantity = quantity_element.text.strip()
                ingredient = text_element.text.strip()
                ingredients.append(f"{quantity} {ingredient}")

        # Extract instructions
        instructions = []
        instruction_elements = soup.find('ul', {'class': 'direction-list'}).find_all('li', {'class': 'direction'})
        for instruction_element in instruction_elements:
            instructions.append(instruction_element.text.strip())

        # Display the recipe information
        recipe_info = (
            "Title: {}\n\n"
            "URL: {}\n\n"
            "Ingredients:\n{}\n\n"
            "Instructions:\n{}"
        ).format(title, url, ', '.join(ingredients), '\n'.join(instructions))
        messagebox.showinfo("Recipe Information", recipe_info)

    else:
        messagebox.showerror("Error", "Failed to retrieve the page. Status code: {}".format(response.status_code))

def on_submit():
    url = entry.get()
    scrape_recipe_data(url)

# Create the main window
root = tk.Tk()
root.title("Recipe Scraper")
root.geometry("600x400")  # Set the initial size of the window

# Create and pack widgets
label = tk.Label(root, text="Enter Recipe URL:")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
