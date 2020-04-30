import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

foods = Blueprint('foods', 'foods')

# GET /api/v1/foods
# SHOW / INDEX
@foods.route('/', methods=['GET'])
def foods_index():
  result = models.Food.select()
  print(result)
  food_dicts = [model_to_dict(food) for food in result]
  print(food_dicts)
  return jsonify({
    'data': food_dicts,
    'message': f"successfully FOUND {len(food_dicts)} foods",
    'status': 200
  }), 200

# POST /api/v1/foods/ (dont forget the slash)
# CREATE
@foods.route('/', methods=['POST'])
def create_food():
  payload = request.get_json()
  print(payload)
  new_food = models.Food.create(
    name=payload['name'],
    price=payload['price'],
    farmer=payload['farmer']
  )
  print(new_food.__dict__)
  food_dict = model_to_dict(new_food)
  return jsonify(
    data=food_dict,
    message="successfully CREATED food!",
    status=201
  ), 201


# DELETE /api/v1/foods/id
@foods.route('/<id>', methods=['DELETE'])
def delete_food(id):
  delete_query = models.Food.delete().where(models.Food.id == id)
  num_of_rows_deleted = delete_query.execute()
  print(num_of_rows_deleted)
  return jsonify(
    data={},
    message=f"successfully DELETED {food.name} food with id {id}",
    status=200
  ), 200


# UPDATE /api/v1/foods/id
@foods.route('/<id>', methods=['PUT'])
def update_food(id):
  payload = request.get_json()

  update_query = models.Food.update(
    name=payload['name'],
    price=payload['price'],
    farmer=payload['farmer']
  ).where(models.Food.id == id)

  num_of_rows_modified = update_query.execute()

  updated_food = models.Food.get_by_id(id) 
  updated_food_dict = model_to_dict(updated_food)

  return jsonify(
      data=updated_food_dict,
      message=f"Successfully updated food with id {id}",
      status=200
    ), 200


















