# MealDeal API

This repository contains the code for MealDeal's REST API. It is written in Python and runs on the Flask framework.

## Endpoints

### POST /login

Credentials are passed in the `Authorization` header in Base64 format.

If the credentials can be validated, the following JSON response is returned:

* token (string)
* user_id (string)

```yaml
{
    "token": "<a JSON web token>",
    "user_id": "<UUID>"
}
```

### GET /metadata/{id}

Based on the user's unique ID, return the following information about the user:

* username (string)
* account_created (string)
* meals_created (integer)
* plans_created (integer)

```yaml
{
    "username": "<username>",
    "account_created": "<date in ISO-format>",
    "meals_created": "<# of meals created by user>",
    "plans_created": "<# of plans created by user>",
}
```

<h3 align="left">GET /foods</h3>

###

<p>TBD</p>

<h3 align="left">GET /meals</h3>

###

<p>TBD</p>

<h3 align="left">POST /plans</h3>

###

<p>TBD</p>

<h3 align="left">GET /plans/(id)</h3>

###

<p>TBD</p>

<h3 align="left">DELETE /plans/(id)</h3>

###

<p>TBD</p>

<h3 align="left">DELETE /meals/(id)</h3>

###

<p>TBD</p>

<h3 align="left">PUT /meals/(id)</h3>

###

<p>TBD</p>

<h3 align="left">GET /types</h3>

###

<p>TBD</p>

<h3 align="left">POST /create</h3>

###

<p>TBD</p>

<h3 align="left">GET /events/meals/(id)</h3>

###

<p>TBD</p>

<h3 align="left">GET /events/plans/(id)</h3>

###

<p>TBD</p>

<h3 align="left">POST /events/plans/(id)</h3>

###

<p>TBD</p>

<h3 align="left">DELETE /events/plans/(id)</h3>

###

<p>TBD</p>

<h3 align="left">GET /categories</h3>

###

<p>TBD</p>