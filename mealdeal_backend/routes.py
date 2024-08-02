from typing import List
from flask import Flask, jsonify, Response, request
from mealdeal_backend.schema import Meal, MealEvent
from .db import Database
from .auth import generate_token, parse_b64, is_permission
import pyodbc

app = Flask(__name__)

@app.post("/login")
def login() -> Response:
    if not request.headers.get('Authorization'):
        return {"message": "Unauthorized"}, 401
    credentials = parse_b64(request.headers.get('Authorization'))
    if credentials:
        user_id = None
        user_name = credentials[0]
        password = credentials[1]
        with Database() as db:
            user_id = db.get_user_id(user_name, password)
        if user_id:
            jwt = generate_token(user_id, user_name)
            return {"token": jwt}, 200
    return {"message": "Invalid username or password."}, 401

@app.get("/foods")
def get_foods() -> Response:
    if is_permission(request.headers):
        foods = []
        with Database() as db:
            foods = db.get_foods()
        return jsonify(foods)
    return {"message": "Unauthorized"}, 401 

@app.get("/meals")
def get_meals() -> Response:
    if is_permission(request.headers):
        meals = []
        with Database() as db:
            meals = db.get_meals()
        return jsonify(meals)
    return {"message": "Unauthorized"}, 401 

@app.get("/types")
def get_types() -> Response:
    if is_permission(request.headers):
        types = []
        with Database() as db:
            types = db.get_types()
        return jsonify(types)
    return {"message": "Unauthorized"}, 401 

@app.post("/create")
def create_meal() -> Response:
    if is_permission(request.headers):
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
    return {"message": "Unauthorized"}, 401 

@app.get("/events/meals/<id>")
def get_meal_contents(id: str) -> Response:
    if is_permission(request.headers):
        meal = {}
        with Database() as db:
            meal_events_for_id = db.get_meal_events_by_id(id)
            for food in meal_events_for_id:
                name = db.get_food_name_by_food_id(food.food_id)
                meal[food.food_id] = {
                    "foodId": food.food_id,
                    "name": name,
                    "amount": food.amount
                }
        return jsonify(meal)
    return {"message": "Unauthorized"}, 401 

@app.delete("/meals/<id>")
def delete_meal(id: str) -> Response:
    if is_permission(request.headers):
        with Database() as db:
            try:
                db.delete_meal(id)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
        return {"message": "Accepted"}, 200
    return {"message": "Unauthorized"}, 401 

@app.put("/meals/<id>")
def update_meal(id: str) -> Response:
    if is_permission(request.headers):
        meal_events: List[tuple] = []
        for entry in request.json:
            event = MealEvent(
                meal_id = id,
                food_id = entry["foodId"],
                amount = entry["amount"],
            )
            meal_events.append(event.tuplify())
        with Database() as db:
            try:
                db.update_meal(id, meal_events)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
        return {"message": "Accepted"}, 200
    return {"message": "Unauthorized"}, 401 

if __name__ == "__main__":
    app.run(ssl_context='adhoc')