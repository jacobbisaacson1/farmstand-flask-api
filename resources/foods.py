import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

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
  print(new_food.__dict__)
  food_dict = model_to_dict(new_food)
  return jsonify(
    data=food_dict,
    message="successfully CREATED food!",
    status=201
  ), 201