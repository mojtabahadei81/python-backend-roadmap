import os
import requests
from pydantic import BaseModel, EmailStr, ValidationError
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

def get_user(url:str) -> None:
    verificated_users = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.json()
        for user in users:
            try:
                data = User(**user)
                verificated_users.append(data.model_dump())
            except ValidationError as val_err:
                logger.error(f"Validation error occurred: {val_err}")

        with open('users.json', 'w') as f:
            json.dump(verificated_users, f, indent=4)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Other error occurred: {err}")

try:
    url = os.environ['API_URL']
except KeyError as e:
    logger.error(f'ERROR: key error occured: {e}')
else:    
    get_user(url)