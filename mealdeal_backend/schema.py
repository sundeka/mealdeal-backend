from dataclasses import dataclass
from datetime import datetime

@dataclass
class Food:
    id: int
    food_id: str
    name: str
    calories: int
    protein: int
    carbs: int

@dataclass
class Meal:
    meal_id: str
    user_id: str
    name: str
    description: str
    type: int

    def tuplify(self):
        return (self.meal_id, self.user_id, self.name, self.description, self.type)

@dataclass
class MealType:
    id: int
    name: str

@dataclass
class MealEvent:
    meal_id: str
    food_id: str
    amount: int

    def tuplify(self):
        return (self.meal_id, self.food_id, self.amount)
    
@dataclass
class UserMetadata:
    username: str
    account_created: str
    meals_created: int