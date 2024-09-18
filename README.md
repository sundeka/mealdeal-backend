# MealDeal API

This repository contains the code for MealDeal's REST API. It is written in Python and runs on the Flask framework.

## Endpoints

### POST /login

Credentials are passed in the `Authorization` header in Base64 format.

If the credentials can be validated, the following JSON response is returned:

* token: str
* user_id: str

```yaml
{
    "token": "<a JSON web token>",
    "user_id": "<UUID>"
}
```

### GET /metadata/{id}

Based on the user's unique ID, return the following information about the user:

* username: str
* account_created: str
* meals_created: int
* plans_created: int

```yaml
{
    "username": "<username>",
    "account_created": "<date in ISO-format>",
    "meals_created": 0,
    "plans_created": 0,
}
```

### GET /foods

Returns all the available foods from the database.

* id: int
* food_id: str
* name: str
* category: int
* calories: float
* fat: float
* fat_saturated: float
* carbs: float
* fiber: float
* protein: float
* salt: float
* calories_ri: float
* fat_ri: float
* fat_saturated_ri: float
* carbs_ri: float
* protein_ri: float

```yaml
[
    {
        "id": 0,
        "food_id": "foo-bar-xyz",
        ...
    },
    {
        ...
    }
]
```

### GET /types

Return all meal types.

* id: int
* name: str

```yaml
[
    {
        "id": "0",
        "name": "<id of food>",
    },
    {
        ...
    }
]
```

### GET /meals/{user_id}

Return all meals for a single user ID.

* meal_id: str
* user_id: str
* name: str
* description: str
* type: int

```yaml
[
    {
        "meal_id": "meal-foo-bar-xyz",
        "user_id": "user-foo-bar-xyz",
        ...
    },
    {
        ...
    }
]
```

### GET /categories

Return all food categories.

* id: int
* name: str

```yaml
[
    {
        "id": 1,
        "name": "Berries",
    },
    {
        ...
    }
]
```

<h3 align="left">POST /create</h3>

<h3 align="left">PUT /meals/(id)</h3>

<h3 align="left">DELETE /meals/(id)</h3>


<h3 align="left">POST /plans</h3>

<h3 align="left">GET /plans/(id)</h3>

<h3 align="left">DELETE /plans/(id)</h3>


<h3 align="left">GET /events/meals/(id)</h3>

<h3 align="left">GET /events/plans/(id)</h3>

<h3 align="left">POST /events/plans/(id)</h3>

<h3 align="left">DELETE /events/plans/(id)</h3>
