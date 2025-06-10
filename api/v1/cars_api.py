from flask import Blueprint, jsonify, request
from data import db_session
from data.cars import Cars

blueprint = Blueprint('cars_api', __name__, template_folder='../templates')


@blueprint.route('/api/v1/cars')
def get_cars():
    cars = db_session.create_session().query(Cars)
    return jsonify(
        {'cars': [car.to_dict(only=('id', 'brand', 'model', 'year', 'is_taken', 'place_id')) for car in cars]}
    )


@blueprint.route('/api/v1/cars/<int:car_id>', methods=['GET'])
def get_one_car(car_id):
    car = db_session.create_session().query(Cars).get(car_id)
    if not car:
        return jsonify({'error': 'car not found'})
    return jsonify(
        {'cars': [car.to_dict(only=('id', 'brand', 'model', 'year', 'is_taken', 'place_id'))]}
    )


@blueprint.route('/api/v1/cars', methods=['POST'])
def create_car():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(
            key in request.json for key in ['brand', 'model', 'year', 'place_id']):
        return jsonify({'error': 'not enough arguments in request'})

    car = Cars(
        brand=request.json['brand'],
        model=request.json['model'],
        year=request.json['year'],
        place_id=request.json['place_id']
    )
    if 'image' in request.json:
        car.image = request.json['image']
    session.add(car)
    session.commit()
    return jsonify({'success': 'car added'})


@blueprint.route('/api/v1/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    session = db_session.create_session()
    car = session.query(Cars).get(car_id)
    if not car:
        return jsonify({'error': 'car not found'})
    session.delete(car)
    session.commit()
    return jsonify({'success': 'car was deleted'})


@blueprint.route('/api/v1/cars/<int:car_id>', methods=['PUT'])
def edit_car(car_id):
    if not request.json:
        return jsonify({'error': 'empty request'})
    elif 'id' in request.json:
        return jsonify({'error': 'id in request'})
    elif not all(
            key in request.json for key in ['brand', 'model', 'year', 'place_id', 'is_taken']):
        return jsonify({'error': 'not enough arguments in request'})
    session = db_session.create_session()
    car = session.query(Cars).get(car_id)
    if not car:
        return jsonify({'error': 'car not found'})
    car.brand = request.json['brand']
    car.model = request.json['model']
    car.year = request.json['year']
    car.place_id = request.json['place_id']
    car.is_taken = request.json['is_taken']
    if 'image' in request.json:
        car.image = request.json['image']
    session.commit()
    return jsonify({'success': 'car edited'})
