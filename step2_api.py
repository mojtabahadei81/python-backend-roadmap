import requests
from pydantic import BaseModel, EmailStr, ValidationError
import json
import logging

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

url = 'https://jsonplaceholder.typicode.com/users'

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

def get_user() -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        User(data['id'], data['name'], data['email'])

        with open('users.json', 'w') as f:
            json.dump(data, f)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Other error occurred: {err}")
    except ValidationError as val_err:
        logger.error(f"Validation error occurred: {err}")

get_user()