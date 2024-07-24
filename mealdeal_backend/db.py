import pyodbc
from typing import List
from .schema import Food, Meal, MealEvent, MealType

driver = server = port = user = password = database = None

with open('conninfo.txt', 'r') as f:
    lines = f.readlines()

if len(lines) >= 6:
    driver = lines[0].strip()
    server = lines[1].strip()
    port = lines[2].strip()
    user = lines[3].strip()
    password = lines[4].strip()
    database = lines[5].strip()

connection_string = f'DRIVER={driver};SERVER={server};PORT={port};UID={user};PWD={password};DATABASE={database}'

class Database:
    def __init__(self):
        self.table_foods = "foods"
        self.table_meals = "meals"
        self.table_types = "meal_types"
        self.table_meal_events = "meal_events"
        self.db = pyodbc.connect(connection_string)
        self.cursor = self.db.cursor()

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
                    meal_id = row[1],
                    name = row[2],
                    description = row[3],
                    type = row[4]
                )
            )
        return meals
    
    def get_types(self) -> List[MealType]:
        meal_types = []
        self.cursor.execute(f'SELECT * FROM {self.table_types}')
        self.db.commit()
        for row in self.cursor.fetchall():
            meal_types.append(
                MealType(
                    id = row[0],
                    name = row[1]
                )
            )
        return meal_types
    
    def create_meal(self, meal: Meal, meal_events: List[MealEvent]):
        self.cursor.execute(f'INSERT INTO {self.table_meals} (meal_id, name, description, type) VALUES (?, ?, ?, ?)', meal.tuplify())
        self.cursor.executemany(f'INSERT INTO {self.table_meal_events} (meal_id, food_id, amount) VALUES (?, ?, ?)', meal_events)
        self.db.commit()

    def get_meal_events_by_id(self, id: str) -> List[MealEvent]:
        meal_events = []
        self.cursor.execute(f'SELECT * FROM {self.table_meal_events} WHERE meal_id = ?', (id))
        self.db.commit()
        for row in self.cursor.fetchall():
            meal_events.append(
                MealEvent(
                    meal_id=row[1],
                    food_id=row[2],
                    amount=row[3]
                )
            )
        return meal_events
    
    def get_food_name_by_food_id(self, id: str) -> str | None:
        self.cursor.execute(f'SELECT (name) FROM {self.table_foods} WHERE food_id = ?', (id))
        self.db.commit()
        return self.cursor.fetchone()[0]
    
    def delete_meal(self, id: str) -> None:
        self.cursor.execute(f'DELETE FROM {self.table_meal_events} WHERE meal_id = ?', (id))
        self.cursor.execute(f'DELETE FROM {self.table_meals} WHERE meal_id = ?', (id))
        self.db.commit()