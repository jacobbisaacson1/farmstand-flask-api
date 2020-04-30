import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user

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
      message=f"Farmer's USERNAME: '{payload['username']}' already exists",
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
    login_user(created_farmer)
    # does the above line need to be created_user?
    created_farmer_dict = model_to_dict(created_farmer)

    print(created_farmer_dict)
    created_farmer_dict.pop('password')

  return jsonify(
    data=created_farmer_dict,
    message=f"Sucessfully REGISTERED: '{created_farmer_dict['username']}'",
    status=201
  ), 201


@farmers.route('/login', methods=['POST'])
def login():
  payload = request.get_json()
  # payload['name'] = payload['name'].lower()
  payload['username'] = payload['username'].lower()
  try: 
    farmer = models.Farmer.get(models.Farmer.username == payload['username'])
    farmer_dict = model_to_dict(farmer)
    password_is_good = check_password_hash(farmer_dict['password'], payload['password'])
    # if pw is good
    if(password_is_good):
      # LOG THE USER IN!!!!! using Flask-Login!
      login_user(farmer) # in express we did this manually by setting stuff in session
      # respond -- all good -- remove the pw first
      farmer_dict.pop('password')
      return jsonify(
        data=farmer_dict,
        message=f"Successfully LOGGED IN {farmer_dict['username']}",
        status=200
      ), 200

    else:
      return jsonify(
        data={},
        message="Username or password is incorrect",
        status=401
      ), 401

  except models.DoesNotExist: 
    return jsonify(
      data={},
      message="Username or password is incorrect",
      status=401
    ), 401





