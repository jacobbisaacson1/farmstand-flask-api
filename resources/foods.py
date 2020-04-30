import models
from flask import Blueprint, request

foods = Blueprint('foods', 'foods')

# GET /api/v1/foods
# SHOW / INDESX
@foods.route('/', methods=['GET'])
def foods_index():
	return "foods resource working"

# POST /api/v1/foods/ (dont forget the slash)
# CREATE
@foods.route('/', methods=['POST'])
def create_food():
  payload = request.get_json()
  print(payload)
  new_food = models.Food.create(
    name=payload['name'],
    price=payload['price'],
    farmer=payload['farmer']
  )
  return "check terminal -- should be actually creating food"