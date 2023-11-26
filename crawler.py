import scrapy
from peewee import SqliteDatabase, Model, TextField
import time
from model import Recipe

# SQLite database setup
db = SqliteDatabase('recipe.db')


# Spider definition
class FoodSpider(scrapy.Spider):
    name = 'food'
    start_page = 1
    base_url = 'https://www.food.com/recipe/all/trending?pn={}'
    start_urls = [base_url.format(start_page)]

    def parse(self, response):
        # Extract URLs using CSS selector
        urls = response.xpath('//body').re('https://www.food.com/recipe/[^"/]*-[0-9]*')
        ##with open("sample.html","w") as f:
           ## f.write(response.text)

        print("-------------------------------------------------- LOGGING")
        ##print(urls)
        for url in set(urls):
            print(url)
            Recipe.create(url=url, column_5=url)  # Assuming you want to store the URL in column_5 as well
        print("-------------------------------------------------- LOGGING")
        # Increment page number and follow the next page link
        self.start_page += 1
        next_page = self.base_url.format(self.start_page)
        time.sleep(1)
        yield scrapy.Request(next_page, callback=self.parse)

    def closed(self, reason):
        # Close the SQLite database connection when the spider is closed
        db.close()
