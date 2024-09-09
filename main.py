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
class InvalidUserDataError(Exception):
    def __init__(self, message="Invalid user data provided"):
        self.message = message
        super().__init__(self.message)

# checking mobile number
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
    hours_spent: List[int] = Field(..., min_items=7, max_items=7)

    @field_validator('mobileno')
    def validate_mobileno(cls, value: str) -> str:
        if not is_all_digits(value):
            raise InvalidUserDataError(
                "Mobile number must contain only digits")
        return value

# Dataclass for user , this dataclass type is used for storing
@dataclass
class User:
    name: str
    email: str
    password: str
    address: str
    mobileno: str
    account_type: AccountType
    hours_spent: List[int]


# List to store users
users: List[User] = []


# Function to add a user
def add_user(user_data: dict):
    try:
        user_model = UserModel(**user_data)
        user = User(
            name=user_model.name,
            email=user_model.email,
            password=user_model.password,
            address=user_model.address,
            mobileno=user_model.mobileno,
            account_type=user_model.account_type,
            hours_spent=user_model.hours_spent
        )
        users.append(user)
        save_users_to_file()
    except ValidationError as e:
        raise InvalidUserDataError(e)

# Functions to plot hours spent bar chart
def get_user_hours_spent(user_name):
    for user in users:
        if user.name == user_name:
            return user.hours_spent
    return []


def plot_hours_spent(hours_spent):
    with dpg.window(label="Plot Window", autosize=True):
        with dpg.plot(label="Hours Spent Over the Last 7 Days", height=400, width=600):
            dpg.add_plot_legend()

            # X-axis
            with dpg.plot_axis(dpg.mvXAxis, label="Days"):
                pass

            # Y-axis
            with dpg.plot_axis(dpg.mvYAxis, label="Hours Spent") as y_axis:
                dpg.add_line_series(
                    [0, 1, 2, 3, 4, 5, 6], hours_spent, label="Hours Spent", parent=y_axis)


# Serialize users to JSON
def serialize_users() -> str:
    return json.dumps([user.__dict__ for user in users], indent=4)

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

# Submit call back function for gui
def submit_callback(sender, app_data, user_data):
    name = dpg.get_value("name_input")
    email = dpg.get_value("email_input")
    password = dpg.get_value("password_input")
    address = dpg.get_value("address_input")
    mobileno = dpg.get_value("mobileno_input")
    account_type = dpg.get_value("account_type_input")
    hours_spent_str = dpg.get_value("hours_spent_input")

    try:
        hours_spent = [int(x.strip())
                       for x in hours_spent_str.split(',') if x.strip()]
    except ValueError:
        dpg.set_value(
            "output_text", "Input should be valid integers separated by commas.")
        return

    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "address": address,
        "mobileno": mobileno,
        "account_type": account_type,
        "hours_spent": hours_spent,
    }
    try:
        add_user(user_data)
        dpg.set_value("output_text", "User added successfully!")
    except InvalidUserDataError as e:
        dpg.set_value("output_text", f"Validation Error: {e}")

# Callback function for the display button
def display_users_callback(sender, app_data, user_data):
    all_users_data = serialize_users()
    dpg.set_value("output_text", all_users_data)


if __name__ == "__main__":

    # CLI IMPLEMENTATION
    load_users_from_file()
    parser = argparse.ArgumentParser(description="User management script")
    parser.add_argument('--add-user', type=str,
                        help='Add a user in JSON format')
    parser.add_argument('--list-users', action='store_true',
                        help='List all users')

    args = parser.parse_args()

    if args.add_user:
        user_data = json.loads(args.add_user)
        add_user(user_data)
        print("User added successfully.")
    elif args.list_users:
        print(serialize_users())



    # Create DearPyGui context
    dpg.create_context()

    # Create the main window
    with dpg.window(label="User Registration", width=900, height=900):
        dpg.add_text("Enter your details")
        dpg.add_input_text(label="Name", tag="name_input")
        dpg.add_input_text(label="Email", tag="email_input")
        dpg.add_input_text(
            label="Password", tag="password_input", password=True)
        dpg.add_input_text(label="Address", tag="address_input")
        dpg.add_input_text(label="Mobile No", tag="mobileno_input")
        dpg.add_combo(label="Account Type", items=[
                      account_type.value for account_type in AccountType], tag="account_type_input")
        dpg.add_input_text(label="Hours Spent (comma-separated)",
                           tag="hours_spent_input", multiline=True)
        
        #Adding Buttons
        dpg.add_button(label="Submit", callback=submit_callback)
        dpg.add_button(label="Display All Users",
                       callback=display_users_callback)
        
        #For Plotting hours spent
        dpg.add_combo(label="Select User", items=[
                      user.name for user in users], tag="user_select_combo")
        dpg.add_button(label="Plot Hours Spent",
                       callback=lambda:  plot_hours_spent(get_user_hours_spent(dpg.get_value("user_select_combo"))))
        dpg.add_text("", tag="output_text")

    # Create DearPyGui viewport
    dpg.create_viewport(title='User Information', width=900, height=600)
    dpg.setup_dearpygui()

    # Set viewport to maximized
    dpg.maximize_viewport()

    # Apply global font scale
    dpg.set_global_font_scale(1.25)

    # Apply the theme globally
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()