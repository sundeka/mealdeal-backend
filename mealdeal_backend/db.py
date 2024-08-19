import pyodbc
import bcrypt
from typing import List
from .exceptions import DatabaseAuthException
from .schema import Food, Meal, MealEvent, MealType, Plan, PlanEvent, TimelinePlanEvent, UserMetadata

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
        self.table_users = "users"
        self.table_plans = "plans"
        self.table_plan_events = "plan_events"
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
    
    def get_meals(self, user_id: str) -> List[Meal]:
        meals = []
        self.cursor.execute(f'SELECT * FROM {self.table_meals} WHERE user_id = ?', (user_id))
        self.db.commit()
        for row in self.cursor.fetchall():
            meals.append(
                Meal(
                    meal_id = row[1],
                    user_id = row[2],
                    name = row[3],
                    description = row[4],
                    type = row[5]
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
        self.cursor.execute(f'INSERT INTO {self.table_meals} (meal_id, user_id, name, description, type) VALUES (?, ?, ?, ?, ?)', meal.tuplify())
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
    
    def delete_meal(self, meal_id: str, user_id: str) -> None:
        self.cursor.execute(f'DELETE FROM {self.table_meal_events} WHERE meal_id = ?', (meal_id))
        self.cursor.execute(f'DELETE FROM {self.table_meals} WHERE meal_id = ? AND user_id = ?', (meal_id, user_id))
        self.db.commit()

    def update_meal(self, user_id: str, meal_id: str, meal_events: List[MealEvent]):
        self.cursor.execute(f'SELECT * from {self.table_meals} where meal_id = ? AND user_id = ?', (meal_id, user_id))
        self.db.commit()
        if self.cursor.fetchone():
            self.cursor.execute(f'DELETE FROM {self.table_meal_events} WHERE meal_id = ?', (meal_id))
            self.cursor.executemany(f'INSERT INTO {self.table_meal_events} (meal_id, food_id, amount) VALUES (?, ?, ?)', meal_events)
            self.db.commit()
        else:
            raise DatabaseAuthException(f"No match: user_id={user_id} meal_id={meal_id}")

    def get_user_id(self, username: str, password: str) -> str | None:
        """
        Check if the user exists in the database.
        Check given password against hash.
        Return user_id (str) if exists, otherwise None.
        """
        self.cursor.execute(f'SELECT user_id, password FROM {self.table_users} WHERE username = ?', (username))
        self.db.commit()
        match = self.cursor.fetchone()
        if match:
            user_id = match[0]
            hashed = match[1]
            if bcrypt.checkpw(bytes(password, "utf-8"), bytes(hashed, "utf-8")):
                return user_id
        return None
    
    def get_metadata_for_user_id(self, id: str) -> UserMetadata:
        metadata = UserMetadata(
            username=None, 
            account_created=None, 
            meals_created=None, 
            plans_created=None
        )
        self.cursor.execute(f'SELECT username, created_at FROM {self.table_users} WHERE user_id = ?', (id))
        self.db.commit()
        match = self.cursor.fetchone()
        if match:
            metadata.username = match[0]
            metadata.account_created = match[1]
            if (metadata.account_created):
                metadata.account_created = metadata.account_created.isoformat()
        self.cursor.execute(f'SELECT * FROM {self.table_meals} where user_id = ?', (id))
        self.db.commit()
        match = self.cursor.fetchall()
        metadata.meals_created = len(match)
        self.cursor.execute(f'SELECT * FROM {self.table_plans} where user_id = ?', (id))
        self.db.commit()
        match = self.cursor.fetchall()
        metadata.plans_created = len(match)
        return metadata
    
    def create_plan(self, plan: Plan):
        self.cursor.execute(f'INSERT INTO {self.table_plans} (plan_id, name, user_id, description, length, created_at, starting_from, is_continuous) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (plan.tuplify()))
        self.db.commit()

    def get_plans(self, id: str) -> List[Plan]:
        plans: List[Plan] = []
        self.cursor.execute(f'SELECT plan_id, name, description, length, created_at, starting_from, is_continuous FROM {self.table_plans} WHERE user_id = ?', (id))
        self.db.commit()
        for row in self.cursor.fetchall():
            starting_from = row[5]
            if starting_from:
                starting_from = starting_from.isoformat()
            plans.append(
                Plan(
                    plan_id=row[0],
                    name=row[1],
                    user_id=id,
                    description=row[2],
                    length=row[3],
                    created_at=row[4].isoformat(),
                    starting_from=starting_from,
                    is_continuous=True if row[6] == 1 else False
                )
            )
        return plans
    
    def get_events_for_plan(self, id: str, start: str | None, end: str | None) -> List[TimelinePlanEvent]:
        query = f'SELECT plan_event_id, day, time, meal_id FROM {self.table_plan_events} WHERE plan_id = ?'
        if start and end:
            query += " AND time BETWEEN ? AND ?"
            self.cursor.execute(query, (id, start, end))
        else:
            self.cursor.execute(query, (id))
        self.db.commit()
        meal_metadata_for_meal_id = {}
        plan_events: List[TimelinePlanEvent] = []
        for row in self.cursor.fetchall():
            meal_id = row[3]
            if not meal_metadata_for_meal_id.get(meal_id):
                # Only search meal data for a single id ONCE (avoid unnecessary search operations)
                query = f'SELECT name, type FROM {self.table_meals} WHERE meal_id = ?'
                self.cursor.execute(query, (meal_id))
                self.db.commit()
                result = self.cursor.fetchone()
                meal_metadata_for_meal_id[meal_id] = {
                    "meal_name": result[0],
                    "meal_type": result[1],
                    "meal_contents": [] # TODO: join in query
                }
            plan_events.append(
                TimelinePlanEvent(
                    plan_event_id=row[0],
                    day=row[1],
                    meal_id=meal_id,
                    time=row[2],
                    meal_name=meal_metadata_for_meal_id.get(meal_id)["meal_name"],
                    meal_type=meal_metadata_for_meal_id.get(meal_id)["meal_type"],
                    meal_contents=meal_metadata_for_meal_id.get(meal_id)["meal_contents"]
                )
            )
        return plan_events
    
    def add_plan_event(self, plan_event: PlanEvent):
        self.cursor.execute(f"INSERT INTO {self.table_plan_events} (plan_event_id, plan_id, day, meal_id, time) VALUES (?, ?, ?, ?, ?)", plan_event.tuplify())
        self.db.commit()

    def delete_plan_event(self, plan_event_id: str):
        self.cursor.execute(f"DELETE FROM {self.table_plan_events} WHERE plan_event_id = ?", (plan_event_id))
        self.db.commit()