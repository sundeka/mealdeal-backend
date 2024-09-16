from dataclasses import dataclass
from typing import List
from dateutil import parser

@dataclass
class Food:
    id: int
    food_id: str
    name: str
    category: int
    calories: float
    fat: float
    fat_saturated: float
    carbs: float
    fiber: float
    protein: float
    salt: float
    calories_ri: float
    fat_ri: float
    fat_saturated_ri: float
    carbs_ri: float
    protein_ri: float

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
    plans_created: int

@dataclass
class Plan:
    plan_id: str
    name: str
    user_id: str
    description: str | None
    length: int | None
    created_at: str
    starting_from: str | None
    is_continuous: bool

    def tuplify(self):
        return (
            self.plan_id,
            self.name,
            self.user_id,
            self.description,
            self.length,
            parser.parse(self.created_at),
            parser.parse(self.starting_from) if self.starting_from else None,
            self.is_continuous
        )
    
@dataclass
class TimelinePlanEvent:
    # Data needed to properly display the item on the timeline
    plan_event_id: str
    day: int
    meal_id: str
    time: str
    meal_name: str
    meal_type: int
    meal_contents: List[dict[str, int]]

    def jsonify(self):
        # Follows the TypeScript naming convention
        # `day` is omitted on purpose
        return {
            "planEventId": self.plan_event_id,
            "mealId": self.meal_id,
            "time": self.time,
            "mealName": self.meal_name,
            "mealType": self.meal_type,
            "mealContents": self.meal_contents
        }
    
@dataclass
class PlanEvent:
    # Data needed to add a new plan event into plan_events
    plan_event_id: str
    plan_id: str
    day: int
    meal_id: str
    time: str

    def tuplify(self):
        return (self.plan_event_id, self.plan_id, self.day, self.meal_id, self.time)
    
@dataclass
class FoodCategory:
    id: int
    name: str