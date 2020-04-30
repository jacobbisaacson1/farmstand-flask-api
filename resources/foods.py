import models
from flask import Blueprint, request

foods = Blueprint('foods', 'foods')

@foods.route('/', methods=['GET'])
def foods_index():
	return "foods resource working"

@foods.route('/', methods=['POST'])
def create_food():
  payload = request.get_json()
  print(payload)
  return "check terminal"