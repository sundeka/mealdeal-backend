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
    meal_id: str
    name: str
    description: str
    type: int

    def tuplify(self):
        return (self.meal_id, self.name, self.description, self.type)

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