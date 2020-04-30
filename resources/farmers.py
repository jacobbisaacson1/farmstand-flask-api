import models
from flask import Blueprint

farmers = Blueprint('farmers', 'farmers')

@farmers.route('/', methods=['GET'])
def test_farmer_resource():
	return "farmer resource set up!"