from typing import List
from flask import Flask, jsonify, Response, request
from mealdeal_backend.schema import Meal, MealEvent, Plan, PlanEvent
from mealdeal_backend.db import Database
from mealdeal_backend.auth import generate_token, parse_b64, is_permission, parse_user_id_from_token
import pyodbc

app = Flask(__name__)

@app.get("/")
def default() -> Response:
    return {"message": "MealDeal backend successfully deployed!"}, 200

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
            return {
                "token": jwt,
                "user_id": user_id,
                }, 200
    return {"message": "Invalid username or password."}, 401

@app.get("/metadata/<id>")
def get_metadata(id: str) -> Response:
    if (is_permission(request.headers)):
        with Database() as db:
            metadata = db.get_metadata_for_user_id(id)
            return {
                "username": metadata.username,
                "account_created": metadata.account_created,
                "meals_created": metadata.meals_created,
                "plans_created": metadata.plans_created
            }, 200
    return {"message": "Unauthorized"}, 401

@app.get("/foods")
def get_foods() -> Response:
    if is_permission(request.headers):
        foods = []
        with Database() as db:
            foods = db.get_foods()
        return jsonify(foods)
    return {"message": "Unauthorized"}, 401 

@app.get("/meals/<user_id>")
def get_meals(user_id: str) -> Response:
    if is_permission(request.headers):
        meals = []
        with Database() as db:
            meals = db.get_meals(user_id)
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
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        meal = Meal(
            meal_id = request.json["mealId"],
            user_id = request.json["userId"],
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

@app.delete("/meals/<meal_id>")
def delete_meal(meal_id: str) -> Response:
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        user_id = parse_user_id_from_token(request.headers['Authorization'])
        with Database() as db:
            try:
                db.delete_meal(meal_id, user_id)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
        return {"message": "Accepted"}, 200
    return {"message": "Unauthorized"}, 401 

@app.put("/meals/<meal_id>")
def update_meal(meal_id: str) -> Response:
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        user_id = parse_user_id_from_token(request.headers['Authorization'])
        meal_events: List[tuple] = []
        for entry in request.json:
            event = MealEvent(
                meal_id = meal_id,
                food_id = entry["foodId"],
                amount = entry["amount"],
            )
            meal_events.append(event.tuplify())
        with Database() as db:
            try:
                db.update_meal(user_id, meal_id, meal_events)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
        return {"message": "Accepted"}, 200
    return {"message": "Unauthorized"}, 401 

@app.post("/plans")
def create_plan() -> Response:
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        user_id = parse_user_id_from_token(request.headers['Authorization'])
        payload = request.json
        plan = Plan(
            plan_id=payload["planId"],
            name=payload["name"],
            user_id=user_id,
            description=payload["description"],
            length=payload["length"],
            created_at=payload["createdAt"],
            starting_from=payload["startingFrom"],
            is_continuous=payload["isContinuous"]
        )
        with Database() as db:
            try:
                db.create_plan(plan)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
        return {"name": payload["name"]}, 200
    return {"message": "Unauthorized"}, 401

@app.delete("/plans/<id>")
def delete_plan(id: str) -> Response:
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        with Database() as db:
            db.delete_plan(id)
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

@app.get("/plans/<id>")
def get_plans(id: str) -> Response:
    if is_permission(request.headers):
        plans = []
        with Database() as db:
            try:
                plans_for_user_id = db.get_plans(id)
            except pyodbc.ProgrammingError as e:
                print(e)
                return {"message": "Error"}, 500
            for plan in plans_for_user_id:
                plan_json = {
                    "planId": plan.plan_id,
                    "name": plan.name,
                    "description": plan.description,
                    "length": plan.length,
                    "createdAt": plan.created_at,
                    "startingFrom": plan.starting_from,
                    "isContinuous": plan.is_continuous
                }
                plans.append(plan_json)
        return jsonify(plans)
    return {"message": "Unauthorized"}, 401 

@app.get("/events/plans/<id>")
def get_plan_events(id: str) -> Response:
    if is_permission(request.headers):
        week_buckets = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            0: [],
        }
        with Database() as db:
            events = db.get_events_for_plan(
                id,
                request.args.get('startDate'),
                request.args.get('endDate') 
            )
            for event in events:
                week_buckets[event.day].append(event.jsonify())
        return jsonify(week_buckets)
    return {"message": "Unauthorized"}, 401 

@app.post("/events/plans/<id>")
def add_plan_event(id: str) -> Response:
    # id = plan_id (not plan_event_id, which is provided in the payload)
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        payload = request.json
        plan_event = PlanEvent(
            plan_event_id=payload["planEventId"],
            plan_id=id,
            day=payload["day"],
            meal_id=payload["mealId"],
            time=payload["time"],
        )
        with Database() as db:
            db.add_plan_event(plan_event)
        return {"message": "OK"}, 200
    return {"message": "Unauthorized"}, 401 

@app.delete("/events/plans/<id>")
def delete_plan_event(id: str) -> Response:
    # id = plan_id (not plan_event_id, which is provided in the payload)
    if is_permission(request.headers):
        return {"message": "POST, PUT and DELETE operations are not allowed in the demo version!"}, 401
        with Database() as db:
            db.delete_plan_event(request.args.get("planEventId"))
        return {"message": "OK"}, 200
    return {"message": "Unauthorized"}, 401 

@app.get("/categories")
def get_food_categories() -> Response:
    if is_permission(request.headers):
        with Database() as db:
            return jsonify(db.get_food_categories())
    return {"message": "Unauthorized"}, 401

if __name__ == "__main__":
    app.run(ssl_context='adhoc')