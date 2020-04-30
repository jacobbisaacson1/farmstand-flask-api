import models
from flask import Blueprint, request

farmers = Blueprint('farmers', 'farmers')

@farmers.route('/', methods=['GET'])
def test_farmer_resource():
	return "farmer resource set up!"


@farmers.route('/register', methods=['POST'])
def register():
  print(request.get_json())
  return "check terminal for register json stuff"





  