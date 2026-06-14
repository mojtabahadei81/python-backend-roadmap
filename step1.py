from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, Field
import logging
from pydantic import ValidationError

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

def process_text(text: str, max_length: int=100) -> dict[str, int|str]:
    if not isinstance(text, str):
        raise TypeError(f'text parameter should be str... you insert {type(text)}')
    
    if len(text) < max_length:
        return {
            "text": text,
            "length": len(text)
            }
    else:
        return {
            "text": text[:max_length],
            "length": max_length
            }
    
output = process_text('salam salam salam', max_length=16)
print(output)
print(type(output))

@dataclass
class ModelConfig:
    model_name: str
    temprature: float = 0.7
    max_token: int=1024

class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(le=120, ge=18, description='your age must be greater than 18 and less than 120')


try:
    user2 = {
        'username': 'javad',
        'email': 'malsdjf',
        'age': 19
    }
    user = UserRegistration(**user2)
    logger.info('user created succesfully!')
except ValidationError as error:
    logger.error(error)

try:
    user3 = {
        'username': 'javad',
        'email': 'm.hadei.1381@gmail.com',
        'age': 18
    }
    user = UserRegistration(**user3)
    logger.info('user created succesfully!')
except ValueError as error:
    logger.error(error)

