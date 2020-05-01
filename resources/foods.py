import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

foods = Blueprint('foods', 'foods')

# GET /api/v1/foods
# SHOW / INDEX
# NOTE !!! DO I WANT TO require login FOR THIS?!  WANT ROUTE TO 
# SHOW ALL THE FARMERS!  -- all the foods will be on their cards
@foods.route('/', methods=['GET'])
@login_required
def foods_index():
  current_user_food_dicts = [model_to_dict(food) for food in current_user.foods]
  for food_dict in current_user_food_dicts:
    food_dict['farmer'].pop('password')
  print(current_user_food_dicts)
  return jsonify({
    'data': current_user_food_dicts,
    'message': f"successfully FOUND {len(current_user_food_dicts)} foods",
    'status': 200
  }), 200

# POST /api/v1/foods/ (dont forget the slash)
# CREATE
@foods.route('/', methods=['POST'])
@login_required
def create_food():
  payload = request.get_json()
  new_food = models.Food.create(
    name=payload['name'],
    price=payload['price'],
    farmer=current_user.id
  )
  food_dict = model_to_dict(new_food)
  print(food_dict)
  food_dict['farmer'].pop('password')
  return jsonify(
    data=food_dict,
    message="successfully CREATED food!",
    status=201
  ), 201

# change food.name to food_to_delete.name
# DELETE /api/v1/foods/id
@foods.route('/<id>', methods=['DELETE'])
@login_required
def delete_food(id):
  try:
    food_to_delete = models.Food.get_by_id(id)
    if food_to_delete.farmer.id == current_user.id:
      food_to_delete.delete_instance()

      return jsonify(
        data={},
        message=f"successfully DELETED {food_to_delete.name} food with ID {id}",
        status=200
      ), 200

    else:
      return jsonify(
        data={
          'error': '403 Forbidden'
        },
        message="Farmer's ID does not match the food's ID. Farmers can only delete their own foods",
        status=403
      ), 403

  except models.DoesNotExist:
    return jsonify(
      data={
        'error': '404 Not Found'
      },
      message="There is no food with that ID",
      status=404
    ), 404


# UPDATE /api/v1/foods/id
@foods.route('/<id>', methods=['PUT'])
@login_required
def update_food(id):
  payload = request.get_json()
  food_to_update = models.Food.get_by_id(id)
  print(type(food_to_update))
  print(food_to_update)
  print(f"food name", food_to_update.name)
  print(f"food id", food_to_update.id)
  print(f"food's farmer", food_to_update.farmer)
  print(f"food's price", food_to_update.price)

  if food_to_update.farmer.id == current_user.id:
    if 'name' in payload:
      food_to_update.name = payload['name']
    if 'price' in payload:
      food_to_update.price = payload['price']
    food_to_update.save()
    updated_food_dict = model_to_dict(food_to_update)
    updated_food_dict['farmer'].pop('password')

    return jsonify(
        data=updated_food_dict,
        message=f"Successfully updated food with id {id}",
        status=200
      ), 200

  else:
      return jsonify(
        data={
          'error': '403 Forbidden'
        },
        message="Food's Farmer's ID does not match food's id. User can only update their own foods",
        status=403
      ), 403 


# SHOW ROUTE -- GET /api/v1/foods/id
@foods.route('/<id>', methods=['GET'])
def show_food(id):
  food = models.Food.get_by_id(id)
  if not current_user.is_authenticated:
    return jsonify(
      data={
        'name': food.name,
        'price': food.price
      },
      message="Registered Farmers can see more info about this food",
      status=200
    ), 200

  else:
    food_dict = model_to_dict(food)
    food_dict['farmer'].pop('password')

    if food.farmer.id != current_user.id:
      food_dict.pop('created_at')

    return jsonify(
      data=food_dict,
      message=f"Found food with id {id}",
      status=200
    ), 200


















