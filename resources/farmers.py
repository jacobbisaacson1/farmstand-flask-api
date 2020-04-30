import models
from flask import Blueprint, request
from flask_bcrypt import generate_password_hash

farmers = Blueprint('farmers', 'farmers')

@farmers.route('/', methods=['GET'])
def test_farmer_resource():
	return "farmer resource set up!"


@farmers.route('/register', methods=['POST'])
def register():
  payload = request.get_json()
  payload['name'] = payload['name'].lower()
  payload['username'] = payload['username'].lower()
  print(payload)
  try:
    models.Farmer.get(models.Farmer.username == payload['username'])
  except models.DoesNotExist:
    pw_hash = generate_password_hash(payload['password'])
    created_farmer = models.Farmer.create(
      username=payload['username'],
      name=payload['name'],
      password=pw_hash
    )
    print(created_farmer)

  return "check terminal for register json stuff"





