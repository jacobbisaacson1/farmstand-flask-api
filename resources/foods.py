import models
from flask import Blueprint

foods = Blueprint('foods', 'foods')

@foods.route('/')
def foods_index():
	return "foods resource working"