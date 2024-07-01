from flask import Flask, jsonify
from .db import Database

app = Flask(__name__)

@app.post("/auth")
def authenticate():
    # TODO
    return jsonify({"auth": True})

@app.get("/foods")
def get_foods():
    foods = []
    with Database() as db:
        foods = db.get_foods()
    return jsonify(foods)

@app.get("/meals")
def get_meals():
    meals = []
    with Database() as db:
        meals = db.get_meals()
    return meals