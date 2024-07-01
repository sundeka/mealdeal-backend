from dataclasses import dataclass

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
    id: int
    meal_id: str
    name: str
    description: str
    type: int