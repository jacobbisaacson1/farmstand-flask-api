import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

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

    if(password_is_good):
      # print(f"{current_user.username} is current_user.username in POST login")
      print(model_to_dict(farmer))
      login_user(farmer)
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


# test route for creating a food connected to farmer
@farmers.route('/all', methods=['GET'])
def farmer_index():
  farmers = models.Farmer.select()
  farmer_dicts = [ model_to_dict(farmer) for farmer in farmers ]

  for farmer_dict in farmer_dicts:
    farmer_dict.pop('password')
  print(farmer_dicts)
  return jsonify(
    farmer_dicts
  ), 200

# test route no.2 to access current farmer
@farmers.route('/logged_in_farmer', methods=['GET'])
def get_logged_in_farmer():
  if not current_user.is_authenticated:
    return jsonify(
      data={},
      message="No farmer is currently logged in",
      status=401,
    ), 401

  else:
    farmer_dict = model_to_dict(current_user)
    farmer_dict.pop('password')

    return jsonify(
      data=farmer_dict,
      message=f"Currently logged in as {farmer_dict['username']}.",
      status=200
    ), 200

@farmers.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    data={},
    message="successfully LOGGED OUT",
    status=200
  ), 200















