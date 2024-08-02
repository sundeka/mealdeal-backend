import os
import re
import base64
import jwt
from typing import List
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

load_dotenv("./.env")

def generate_token(user_id: str, user_name: str) -> str:
    payload = {
        'user_id': user_id,
        'user_name': user_name,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    return jwt.encode(
        payload=payload, 
        key=os.environ['SECRET'], 
        algorithm=os.environ['ALGORITHM'],
        headers={
            "iss": "MealDeal"
        }
    )

def is_permission(headers: dict) -> bool:
    """
    headers: dict - Contains the Header block of the HTTP request

    Endpoint safeguard. 
    Checks the validity of the JWT token. Returns True if permission exists.
    """
    if headers.get('Authorization'):
        match = re.search(r"Bearer\s+([A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+)", headers['Authorization'])
        if match:
            token = match.group(1)
            try:
                jwt.decode(
                    jwt=token,
                    key=os.environ['SECRET'],
                    algorithms=[os.environ['ALGORITHM']]
                )
                return True
            except (
                jwt.exceptions.DecodeError,
                jwt.ExpiredSignatureError,
                jwt.InvalidTokenError
            ):
                """Returns False"""
                pass
    return False

def parse_b64(encoded_b64: str) -> List[str] | None:
    """encoded_b64: str - Base64 string where the decoded format is <username>:<password>"""
    decoded_b64 = _decode_b64(encoded_b64)
    credentials = decoded_b64.split(":")
    if len(credentials) == 2:
        return credentials
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