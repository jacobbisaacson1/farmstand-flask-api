import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

farmers = Blueprint('farmers', 'farmers')

@farmers.route('/', methods=['GET'])
def test_farmer_resource():
  return "farmer resource set up!"

# @farmers.route('/', methods=['GET'])
# def farmers_index():
#   farmer_dicts = model_to_dict(farmers)
#   print(farmer_dicts)
#   return jsonify({
#     'data': farmer_dicts,
#     'message': f"successfully FOUND {len(farmer_dicts)} farmers",
#     'status': 201
#   }), 201

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

# ALL FARMERS INDEX -- connect to show page
# test route for creating a food connected to farmer

#  see the /all -- get cors error if gone, but its the right url;


@farmers.route('/all', methods=['GET'])
def farmer_index():
  farmers = models.Farmer.select()
  farmer_dicts = [ model_to_dict(farmer) for farmer in farmers ]

  for farmer_dict in farmer_dicts:
    farmer_dict.pop('password')
  print(farmer_dicts)
  return jsonify({
    'data': farmer_dicts,
    'message': f"successfully FOUND {len(farmer_dicts)} FARMERS",
    'status': 200
  }), 200


# @farmers.route('/all', methods=['GET'])
# def farmer_index():
#   current_user_farmer_dicts = [model_to_dict(farmer) for farmer in current_user.farmers]
#   for farmer_dict in current_user_farmer_dicts:
#     print(current_user_farmer_dicts)
#   return jsonify({
#     'data': current_user_farmer_dicts,
#     'message': f"successfully FOUND {len(current_user_farmer_dicts)} FARMERS",
#     'status': 200
#   }), 200




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















