from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator
from dataclasses import dataclass
import json
import argparse
import dearpygui.dearpygui as dpg
import re
import os


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
users: List[UserModel] = []


# Function to add a user
def add_user(user_data: dict):
    try:
        user = UserModel(**user_data)
        users.append(user)
        save_users_to_file()
    except ValidationError as e:
        raise UserNotFoundError(e)
    

# Serialize users to JSON
def serialize_users() -> str:
    return json.dumps([user.model_dump() for user in users], indent=4)

# Deserialize users from JSON
def deserialize_users(json_data: str):
    user_list = json.loads(json_data)
    for user_data in user_list:
        users.append(UserModel(**user_data))


# Load users from file
def load_users_from_file():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            json_data = file.read()
            deserialize_users(json_data)

# save users to a file
def save_users_to_file():
    with open('users.json', 'w') as file:
        file.write(serialize_users())


# CLI implementation
def main():
    load_users_from_file()
    parser = argparse.ArgumentParser(description="User management script")
    parser.add_argument('--add-user', type=str, help='Add a user in JSON format')
    parser.add_argument('--list-users', action='store_true', help='List all users')

    args = parser.parse_args()

    if args.add_user:
        user_data = json.loads(args.add_user)
        add_user(user_data)
        print("User added successfully.")
    elif args.list_users:
        print(serialize_users())

if __name__ == "__main__":
    main()

