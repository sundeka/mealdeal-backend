import os
import re
import base64
import jwt
from datetime import timedelta, datetime, timezone

secret = "381836fe163039ab7bcd0a84bf54dded9fbd4269"
algorithm = "HS256"

def generate_token(user_id: str, user_name: str) -> str:
    #secret = () TODO: hae dotenvistä
    #algorithm = () TODO: hae dotenvistä
    payload = {
        'user_id': user_id,
        'user_name': user_name,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    return jwt.encode(
        payload=payload, 
        key=secret, 
        algorithm=algorithm,
        headers={
            "iss": "MealDeal"
        }
    )

def parse_b64(encoded_b64: str) -> str | None:
    """encoded_b64: str - Base64 string where the decoded format is <username>:<password>"""
    decoded_b64 = _decode_b64(encoded_b64)
    credentials = decoded_b64.split(":")
    if len(credentials) == 2:
        return credentials[0]
    return None

def _decode_b64(encoded_b64: str) -> str:
    """Handles the bytes-string conversion crap"""
    match = re.search(r"^Basic\s+([A-Za-z0-9+/=]+)", encoded_b64)
    if match:
        base64_string = match.group(1)
        try:
            decoded = base64.b64decode(base64_string).decode("utf-8")
            return decoded
        except UnicodeDecodeError:
            pass
    return None