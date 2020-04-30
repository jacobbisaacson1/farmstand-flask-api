import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

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
    return jsonify(
      data={},
      message="Farmer's USERNAME already exists",
      status=401
    ), 401
  except models.DoesNotExist:
    pw_hash = generate_password_hash(payload['password'])
    created_farmer = models.Farmer.create(
      username=payload['username'],
      name=payload['name'],
      password=pw_hash
    )
    print(created_farmer)
    created_farmer_dict = model_to_dict(created_farmer)
    print(created_farmer_dict)
    created_farmer_dict.pop('password')

  return jsonify(
    data=created_farmer_dict,
    message="Sucessfully REGISTERED farmer",
    status=201
  ), 201





