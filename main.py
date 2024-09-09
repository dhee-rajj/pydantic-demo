from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dataclasses import dataclass
import json
import argparse
import dearpygui.dearpygui as dpg
import re

# Enum for account types
class AccountType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"

# Custom exceptions
class UserNotFoundError(Exception):
    pass

def is_all_digits(value: str) -> bool:
    return bool(re.match(r'^\d+$', value))

# Pydantic model for user
class UserModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    address: str = Field(..., min_length=1, max_length=255)
    mobileno: str = Field(..., min_length=10, max_length=15)
    account_type: AccountType = AccountType.FREE

    @field_validator('mobileno')
    def validate_mobileno(cls, value: str) -> str:
        if not is_all_digits(value):
            raise ValueError("Mobile number must contain only digits")
        return value

# Dataclass for user
@dataclass
class User:
    name: str
    email: str
    password: str
    address: str
    mobileno: str
    account_type: AccountType

# List to store users
users: List[User] = []


# Function to add a user
def add_user(user_data: dict):
    try:
        user = User(**user_data)
        users.append(user)
    except ValidationError as e:
        raise UserNotFoundError(e)
    

# Serialize users to JSON
def serialize_users() -> str:
    return json.dumps([user.model_dump() for user in users], indent=4)

# Deserialize users from JSON
def deserialize_users(json_data: str):
    user_list = json.loads(json_data)
    for user_data in user_list:
        add_user(user_data)