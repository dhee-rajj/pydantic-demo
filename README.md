# User Management Script

This project is a user management script that allows you to add users, list users, and plot the hours spent by a user over the last 7 days. The script uses DearPyGui for graphical plotting.

## Features

- Add a user in JSON format
- List all users
- Plot hours spent graph for a user

## Requirements

- Python 3.x
- pydantic
- DearPyGui
- argparse
- json

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/dhee-rajj/pydantic-demo.git
    cd pydantic-demo
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
## Usage

### Add a User

To add a user, use the `--add-user` argument followed by the user data in JSON format:
```sh
python main.py --add-user '{"name": "Robbin", "email": "robbin@example.com", "password": "securepassword", "address": "123 Main St", "mobileno": "1234567890", "account_type": "free", "hours_spent": [1, 2, 3, 4, 5, 6, 7]}'

### List All Users

pyhton main.py --list-users

### Plot User Hours Spend

python main.py --plot-graph "username"

### For GUI
python main.py

