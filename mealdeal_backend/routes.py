from typing import List
from flask import Flask, jsonify, Response, request
from mealdeal_backend.schema import Meal, MealEvent
from .db import Database
import pyodbc

app = Flask(__name__)

@app.post("/auth")
def authenticate() -> Response:
    # TODO
    return jsonify({"auth": True})

@app.get("/foods")
def get_foods() -> Response:
    foods = []
    with Database() as db:
        foods = db.get_foods()
    return jsonify(foods)

@app.get("/meals")
def get_meals() -> Response:
    meals = []
    with Database() as db:
        meals = db.get_meals()
    return jsonify(meals)

@app.get("/types")
def get_types() -> Response:
    types = []
    with Database() as db:
        types = db.get_types()
    return jsonify(types)

@app.post("/create")
def create_meal() -> Response:
    meal = Meal(
        meal_id = request.json["mealId"],
        name = request.json["name"],
        description = request.json["description"],
        type = request.json["type"],
    )

    meal_events: List[tuple] = []
    for entry in request.json["events"]:
        event = MealEvent(
            meal_id = meal.meal_id,
            food_id = entry["foodId"],
            amount = entry["amount"],
        )
        meal_events.append(event.tuplify())

    with Database() as db:
        try:
            db.create_meal(meal, meal_events)
        except pyodbc.ProgrammingError as e:
            print(e)
            return {"message": "Error"}, 500
        
    return {"message": "Accepted"}, 200