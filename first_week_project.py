from pydantic import ValidationError, BaseModel
import json
import requests
import logging

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

url= 'https://fakestoreapi.com/products'

class Product(BaseModel):
    id: int
    title: str
    price: float
    category: str


def get_products() -> None:    
 
    try:
        response = requests.get(url)
        response.raise_for_status()
        verificated_products = []
        expencive_products = []

        data = response.json()
        
        for d in data:
            try:
                product = Product(**d)
                if product.price > 50:
                    expencive_products.append(product.model_dump())
                    logger.info(f'product number {product.id} is expencive product.')
                else:
                    verificated_products.append(product.model_dump())
                    logger.info(f'product number {product.id} is created.')
            except ValidationError as val_err:
                logger.error(f'validation error occurred: {val_err}')

        with open('expencive_products.json', 'w') as f:
            json.dump(expencive_products, f, indent=4)

        
        with open('products_with_approprite_price.json', 'w') as f:
            json.dump(verificated_products, f, indent=4)

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Other error occurred: {err}")

get_products()