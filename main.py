from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field, ValidationError
from dataclasses import dataclass
import json
import argparse
import dearpygui.dearpygui as dpg

# Enum for account types
class AccountType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"

# Custom exceptions
class UserNotFoundError(Exception):
    pass

# Pydantic model for user
class UserModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    address: str = Field(..., min_length=1, max_length=255)
    mobileno: str = Field(..., min_length=10, max_length=15)
    account_type: AccountType = AccountType.FREE

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