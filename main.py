from model import Recipe

def main_loop():
    while True:
        ingredients = input('Please enter ingredients, separated by commas\n')
        ingredients = ingredients.split(',')
        ingredients = [i.strip() for i in ingredients]
        recipes = Recipe.find_by_ingredients(ingredients)
        print('INGREDIENTS = ', ingredients)
        for recipe in recipes:
            print(recipe.title, '\nURL: ', recipe.url)



if __name__ == '__main__':
    main_loop()