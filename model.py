import scrapy
from peewee import SqliteDatabase, Model, TextField, AutoField
import json


# SQLite database setup
db = SqliteDatabase('recipe.db')


# Peewee ORM model
class Recipe(Model):
    id = AutoField()
    title = TextField()
    ingredients = TextField()
    instructions = TextField()
    url = TextField(unique=True)


    class Meta:
        database = db

    @classmethod
    def get_by_id(cls, pk):
        return Recipe.get(Recipe.id == pk)

    @classmethod
    def find_by_ingredients(cls, ingredients):
        result = []
        for recipe in Recipe.select():
            has_all_ingredients = True
            recipe_ingredients = json.loads(recipe.ingredients)
            for ingredient in ingredients:
                has_one_ingredient = False

                for recipe_ingredient in recipe_ingredients:
                    if ingredient in recipe_ingredient:
                        has_one_ingredient = True

                if not has_one_ingredient:
                    has_all_ingredients = False
            if has_all_ingredients:
                result.append(recipe)
        return result


