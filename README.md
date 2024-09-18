# MealDeal API

This repository contains the code for MealDeal's REST API. It is written in Python and runs on the Flask framework.

## Endpoints

**NOTE:** without a valid JSON Web Token in the request header, all endpoints except `/login` return a `401 Unauthorized` HTTP response!
 
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

### POST /create

Create a new meal.

Expects the following payload:

* mealId: str
* userId: str
* name: str
* description: str (optional, can be an empty string)
* type: int
* events: List

```yaml
{
    "mealId": "meal-uuid-foo-bar",
    "userId": "user-uuid-foo-bar",
    "name": "my meal",
    "description": "",
    "type": 2,
    "events": [
        {
            "mealId": "meal-uuid-foo-bar",
            "foodId": "food-uuid-foo-bar",
            "amount": 150
        },
        {
            ...
        }  
    ]
}
```

### PUT /meals/{id}

Updates an existing meal by deleting all pre-existing meal items and replacing them with new ones. 

Expects the user's ID in the `Authorization` header, while the meal ID is provided in the URI.

Expects the following items provided in a JSON array:

* mealId: str
* foodId: str
* amount: int

```yaml
{
    [
        {
            "mealId": "meal-uuid-foo-bar",
            "foodId": "food-uuid-foo-bar",
            "amount": 150
        },
        {
            ...
        }
    ]
}
```

### DELETE /meals/{meal_id}

Delete a meal based on its ID.

Expects user ID to be provided in the `Authorization` header.

### POST /plans

Create a new meal plan.

Expects user ID to be provided in the `Authorization` header.

In addition, expects the following payload:

* planId: str
* name: str
* description: str (optional, can be an empty string)
* length: int | None (continous plans don't have a length)
* createdAt: str
* startingFrom: str
* isContinuous: bool

```yaml
{
    "planId": "plan-uuid-foo-bar",
    "name": "My plan",
    "description": "My new plan.",
    "length": 0,
    "createdAt": "<ISOFormat date>",
    "startingFrom": "<ISOFormat date>",
    "isContinous": true
}
```

### GET /plans/{id}

Returns all plans for a given user ID as a JSON array.

* planId: str
* name: str
* description: str (optional, can be an empty string)
* length: int | None (continous plans don't have a length)
* createdAt: str
* startingFrom: str
* isContinuous: bool

```yaml
[
    {
        "planId": "plan-uuid-foo-bar",
        "name": "My plan",
        "description": "My new plan.",
        "length": 0,
        "createdAt": "<ISOFormat date>",
        "startingFrom": "<ISOFormat date>",
        "isContinous": true
    },
    {
        ...
    }
]
```

### DELETE /plans/{id}

Delete a meal plan by plan ID.

### GET /events/meals/{id}

Given a meal ID, return the individual foods that comprise it.

Returns all food data in a JSON array.

* foodId: str
* name: str
* amount: int

```yaml
[
    {
        "foodId": "food-uuid-foo-bar",
        "name": "Blueberry",
        "amount": 150
    },
    {
        ...
    }
]
```

### GET /events/plans/{id}

Given a plan ID and start/end date, return all individual meal events for said plan and timespan.

Expects a start date and an end date to be provided in the request parameters in ISO format as in:

`/events/plans/<planId>?startDate=1970-01-01T00:00:00+00:00&endDate=1970-01-06T23:59:00+00:00`

Returns all events for the provided 7-day span as a JSON object:

An individual entry has the following structure:

* plan_event_id: str
* plan_id: str
* day: int
* meal_id: str
* time: str

The actual response has the following format **without** the keys:

```yaml
1: [
    {
        "plan_event_uuid-foo-bar",
        "plan_uuid-foo-bar",
        1,
        "meal-uuid-foo-bar",
        "1970-01-01T06:00:00+00:00"
    },
    {
        ...
    }
],
2: [
    ...
]
...
6: [
    ...
]
0: [
    ...
]
```

### POST /events/plans/{id}

Insert a new meal event into a plan, given the plan ID.

Expects the following payload:

* plan_event_id: str (any randomly generated UUID)
* plan_id: str
* day: int
* meal_id: str
* time: str (in ISOFormat)

### DELETE /events/plans/{id}

Delete a meal event from a plan, given the plan ID.

Expects `planEventId` to be provided in the request parameters.