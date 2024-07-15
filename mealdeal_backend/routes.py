from flask import Flask, jsonify, Response
from .db import Database

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