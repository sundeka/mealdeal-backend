import sqlite3
from flask import g
from typing import List
from .schema import Food, Meal

class Database:
    def __init__(self):
        self.db = getattr(g, '_database', None)
        if self.db is None:
            self.db = g._database = sqlite3.connect("mealdeal.db")
        self.cursor = self.db.cursor()
        self.table_foods = "foods"
        self.table_meals = "meals"

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.db.close()

    def get_foods(self) -> List[Food]:
        foods = []
        self.cursor.execute(f'SELECT * FROM {self.table_foods}')
        self.db.commit()
        for row in self.cursor.fetchall():
            foods.append(
                    Food(
                        id = row[0],
                        food_id = row[1],
                        name = row[2],
                        calories = row[3],
                        protein = row[4],
                        carbs = row[5]
                    )
                )
        return foods
    
    def get_meals(self) -> List[Meal]:
        meals = []
        self.cursor.execute(f'SELECT * FROM {self.table_meals}')
        self.db.commit()
        for row in self.cursor.fetchall():
            meals.append(
                Meal(
                    id = row[0],
                    meal_id = row[1],
                    name = row[2],
                    description = row[3],
                    type = row[4]
                )
            )
        return meals