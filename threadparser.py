import queue
import threading
from model import Recipe
from foodparser import scrape_recipe_data

q = queue.Queue()


for r in Recipe.select():
    if r.title is None:
        q.put(r)

def worker():
    while True:
        try:
            recipe = q.get(block=True, timeout=1)
            scrape_recipe_data(recipe.url, recipe)
            q.task_done()
        except queue.Empty:
            return
        except Exception as e:
            print(e)
            return

workers = []
for _ in range(100):
    worker2 = threading.Thread(target=worker)
    worker2.start()
    workers.append(worker2)
q.join()
for w in workers:
    w.join()


